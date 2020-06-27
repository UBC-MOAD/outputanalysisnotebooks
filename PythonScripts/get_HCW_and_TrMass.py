# =======================================================================================================
# This script calculates and saves the volume of High Concentration Water (HCW) and tracer mass on shelf 
# for all records in the canyon_records and nocanyon_records dictionaries.
# =======================================================================================================
# Imports and modules
from netCDF4 import Dataset
import numpy as np
import pandas as pd

import canyon_tools.metrics_tools as mtt 
import canyon_tools.readout_tools as rout

# Load all records from the "runs" dictionary
import os
import sys
lib_path = os.path.abspath('Paper1Figures/') # Add path to my python scripts
sys.path.append(lib_path)

import canyon_records 
import nocanyon_records

records = canyon_records.main()
recordsNoC = nocanyon_records.main()

# Additional functions
# -------------------------------------------------------------------------------------------------------------------------
def Tracer_AlongShelf(Tr,TrAdv,MaskC,rA,hFacC,drF,yin,zfin,xi,yi,nzlim):
    '''
    INPUT----------------------------------------------------------------------------------------------------------------
    Tr    : Array with concentration values for a tracer. Until this function is more general, size 19x104x360x616
    TrAdv : Array with concentration values for low diffusivity tracer. Until this function is more general, size 19x104x360x616
    MaskC : Land mask for tracer
    nzlim : The nz index below which to look for water properties
    rA    : Area of cell faces at C points (360x616)
    fFacC : Fraction of open cell (104x360x616)
    drF   : Distance between cell faces (104)
    yin   : across-shore index of shelf break
    zfin  : shelf break index + 1 
    xi    : x index of position of initial profile 
    yi    : y index of position of initial profile 
    
    OUTPUT----------------------------------------------------------------------------------------------------------------
    TrMass =  Array with the tracer mass over the shelf contained in HCW [t,nx] at every time output.
    Total_Tracer =  Array with the mass of tracer (m^3*[C]*l/m^3) at each x-position over the shelf at 
                    every time output. 
    -----------------------------------------------------------------------------------------------------------------------
    '''
    maskExp = mtt.maskExpand(MaskC,TrAdv)

    TrMask=np.ma.array(TrAdv,mask=maskExp)   
    Tr1Mask=np.ma.array(Tr,mask=maskExp)   
    
    trlim1 = TrMask[0,nzlim,yi,xi]
    trlim = (trlim1)

    print('tracer limit concentration is: ',trlim)
    
    # mask cells with tracer concentration < trlim on shelf
    HighConc_Masked = np.ma.masked_less(TrMask[:,:zfin,yin:,:], trlim) 
    HighConc_Mask = HighConc_Masked.mask

    #Get volume of water of cells with relatively high concentration
    rA_exp = np.expand_dims(rA[yin:,:],0)
    drF_exp = np.expand_dims(np.expand_dims(drF[:zfin],1),1)
    rA_exp = rA_exp + np.zeros(hFacC[:zfin,yin:,:].shape)
    drF_exp = drF_exp + np.zeros(hFacC[:zfin,yin:,:].shape)

    ShelfVolume = hFacC[:zfin,yin:,:]*drF_exp*rA_exp
    ShelfVolume_exp = np.expand_dims(ShelfVolume,0)
    ShelfVolume_exp = ShelfVolume_exp + np.zeros(HighConc_Mask.shape)
   
    HighConc_CellVol = np.ma.masked_array(ShelfVolume_exp,mask = HighConc_Mask) 
    TrConc_HCW = np.ma.masked_array(Tr[:,:zfin,yin:,:],mask = HighConc_Mask) 

    MassTrHighConc =np.ma.sum(np.ma.sum(np.ma.sum(HighConc_CellVol*TrConc_HCW,axis = 1),axis=1),axis=1)

    # Get total mass of tracer on shelf
    Total_Tracer = np.ma.sum(np.ma.sum(np.ma.sum(ShelfVolume_exp*Tr1Mask[:,:zfin,yin:,:],axis = 1),axis=1),axis=1)
    
    return (MassTrHighConc, Total_Tracer)

# -------------------------------------------------------------------------------------------------------------------------

## HERE WE GO! 
# Load grid files
CanyonGrid='/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run38/gridGlob.nc'
CanyonGridOut = Dataset(CanyonGrid)

CanyonGridNoC='/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run42/gridGlob.nc'
CanyonGridOutNoC = Dataset(CanyonGridNoC)

CanyonState='/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run38/stateGlob.nc'
CanyonStateOut = Dataset(CanyonState)

# Grid dimensions
nx = 616
ny = 360
nz = 104 
nt = 19 # t dimension size 
 
# Indices for the shelf box, etc
xi = 180
yi = 50
nzlim = 29 # Bar:39, Ast:29, Orig:29
zfin = 30 # Bar:40, Ast:30, Orig:30
xfin = 615
yin =130 # Orig: 225

# Grid variables
xc = rout.getField(CanyonGrid, 'XC') # x coords tracer cells
yc = rout.getField(CanyonGrid, 'YC') # y coords tracer cells
rc = CanyonGridOut.variables['RC']
dxg = rout.getField(CanyonGrid, 'dxG') # x coords tracer cells
dyg = rout.getField(CanyonGrid, 'dyG') # y coords tracer cells

bathy = rout.getField(CanyonGrid, 'Depth')
hFacC = rout.getField(CanyonGrid, 'HFacC')
MaskC = rout.getMask(CanyonGrid, 'HFacC')

bathyNoC = rout.getField(CanyonGridNoC, 'Depth')
hFacCNoC = rout.getField(CanyonGridNoC, 'HFacC')
MaskCNoC = rout.getMask(CanyonGridNoC, 'HFacC')

rA = rout.getField(CanyonGrid, 'rA')

z = CanyonStateOut.variables['Z']
drF = CanyonGridOut.variables['drF']
time = CanyonStateOut.variables['T']

# Calculate HCW and TR Mass for all runs in records and recordsNoC
for record in records:
    ptr_file = ('/ocean/kramosmu/MITgcm/TracerExperiments/%s/%s/ptracersGlob.nc' \
                %(record.exp_code,record.run_num))
    Tr = Dataset(ptr_file).variables['Tr01'][:,:zfin+1,:,:] 
    TrAdv = Dataset(ptr_file).variables['Tr02'][:,:zfin+1,:,:] # Low difusivity tracer is Tr02

    TrMassHCW, TotTrMass = Tracer_AlongShelf(Tr,TrAdv, MaskCNoC[:zfin+1,:,:], rA,
                                             hFacCNoC, drF[:zfin+1], yin, zfin, 
                                             xi, yi, nzlim)
    HCW = mtt.calc_HCW(TrAdv, MaskCNoC[:zfin+1,:,:], rA, hFacCNoC, drF[:zfin+1],
                       nzlim=nzlim, yin=yin, xin=0, xfin=xfin, zfin=zfin, xi=xi, yi=yi)
    
    # Save dataframe
    raw_data = {'time' : time,'HCW': HCW,'TrMassHCW': TrMassHCW,'TotTrMass':TotTrMass}
    df = pd.DataFrame(raw_data, columns = ['time' ,'HCW','TrMassHCW','TotTrMass'])
    filename1 = ('/ocean/kramosmu/MITgcm/TracerExperiments/%s/HCW_TrMass_%s%s.csv' \
                 %(record.exp_code,record.exp_code,record.run_num))
    df.to_csv(filename1)

for record in recordsNoC:
    ptr_file = ('/ocean/kramosmu/MITgcm/TracerExperiments/%s/%s/ptracersGlob.nc' \
                %(record.exp_code,record.run_num))
    Tr = Dataset(ptr_file).variables['Tr01'][:,:zfin+1,:,:] 
    TrAdv = Dataset(ptr_file).variables['Tr02'][:,:zfin+1,:,:] 
    
    TrMass, TotTrMass = Tracer_AlongShelf(Tr,TrAdv, MaskCNoC[:zfin+1,:,:], rA, 
                                          hFacCNoC, drF[:zfin+1], yin, zfin,
                                          xi, yi, nzlim)
    HCW = mtt.calc_HCW(TrAdv, MaskCNoC[:zfin+1,:,:], rA, hFacCNoC, drF[:zfin+1],
                       nzlim=nzlim, yin=yin, xin=0, xfin=xfin, zfin=zfin, xi=xi, yi=yi)
    
    # Save dataframe
    raw_data = {'time' : time,'HCW': HCW,'TrMassHCW': TrMassHCW,'TotTrMass':TotTrMass}
    df = pd.DataFrame(raw_data, columns = ['time' ,'HCW','TrMassHCW','TotTrMass'])
    filename2 = ('/ocean/kramosmu/MITgcm/TracerExperiments/%s/HCW_TrMass_%s%s.csv' \
                 %(record.exp_code,record.exp_code,record.run_num))
    df.to_csv(filename2)

    
    
