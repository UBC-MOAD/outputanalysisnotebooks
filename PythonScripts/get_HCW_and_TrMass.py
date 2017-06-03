# Calculate and save HCW and tracer mass on shelf
from netCDF4 import Dataset
import numpy as np
import pandas as pd

import canyon_tools.metrics_tools as mtt 
import canyon_tools.readout_tools as rout

# -------------------------------------------------------------------------------------------------------------------------
def Tracer_AlongShelf(Tr,TrAdv,MaskC,rA,hFacC,drF,yin,zfin,xi,yi,nzlim):
    '''
    INPUT----------------------------------------------------------------------------------------------------------------
    Tr    : Array with concentration values for a tracer. Until this function is more general, size 19x90x360x360
    TrAdv : Array with concentration values for low diffusivity tracer. Until this function is more general, size 19x90x360x360
    MaskC : Land mask for tracer
    nzlim : The nz index under which to look for water properties
    rA    : Area of cell faces at C points (360x360)
    fFacC : Fraction of open cell (90x360x360)
    drF   : Distance between cell faces (90)
    yin   : across-shore index of shelf break
    zfin  : shelf break index + 1 
    xi    : initial profile x index
    yi    : initial profile y index
    
    OUTPUT----------------------------------------------------------------------------------------------------------------
    TrMass =  Array with the mass of tracer over the shelf in HCW [t,360] at every time output.
    Total_Tracer =  Array with the mass of tracer (m^3*[C]*l/m^3) at each x-position over the shelf [t,360] at 
                    every time output. 
    -----------------------------------------------------------------------------------------------------------------------
    '''
    maskExp = mtt.maskExpand(MaskC,TrAdv)

    TrMask=np.ma.array(TrAdv,mask=maskExp)   
    
    trlim = TrMask[0,nzlim,yi,xi]

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

    MassTrHighConc =np.ma.sum(np.ma.sum(np.sum(HighConc_CellVol*TrConc_HCW*1000,axis = 1),axis=1),axis=1)

    #Get total mass of tracer on shelf
    Total_Tracer = np.ma.sum(np.ma.sum(np.sum(ShelfVolume_exp*TrMask[:,:zfin,yin:,:]*1000.0,axis = 1),axis=1),axis=1)
     # 1 m^3 = 1000 l

    return (MassTrHighConc, Total_Tracer)
# -------------------------------------------------------------------------------------------------------------------------
# Load grid files
CanyonGrid='/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run38/gridGlob.nc'
CanyonGridOut = Dataset(CanyonGrid)

CanyonGridNoC='/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run42/gridGlob.nc'
CanyonGridOutNoC = Dataset(CanyonGridNoC)

CanyonState='/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run38/stateGlob.nc'
CanyonStateOut = Dataset(CanyonState)

# Grid variables
nx = 360
ny = 360
nz = 90
nt = 19 # t dimension size 

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

# Load records for each run
import os
import sys
lib_path = os.path.abspath('Paper1Figures/') # Add absolute path to my python scripts
sys.path.append(lib_path)

import canyon_records 
import nocanyon_records

records = canyon_records.main()
recordsNoC = nocanyon_records.main()

# Calculate HCW and TR Mass
for record in records:
    filename=('/ocean/kramosmu/MITgcm/TracerExperiments/%s/%s/ptracersGlob.nc' %(record.exp_code,record.run_num))
    Tr1 = rout.getField(filename,'Tr1') 
    Tr2 = rout.getField(filename,'Tr2') 
     
    TrMass, TotTrMass = Tracer_AlongShelf(Tr1,Tr2, MaskCNoC, rA, hFacCNoC, drF[:], 227, 30,  180, 50,29)
    HCW = mtt.calc_HCW(Tr1, MaskCNoC, rA, hFacCNoC, drF[:],nzlim=29, yin=227, xin=0, xfin=359, zfin=30, xi=180, yi=50)
    
    raw_data = {'time' : time,'HCW': HCW,'TrMass': TrMass}
    df = pd.DataFrame(raw_data, columns = ['time' ,'HCW','TrMass'])
    filename1 = ('/ocean/kramosmu/MITgcm/TracerExperiments/%s/HCW_TrMass_%s%s.csv' %(record.exp_code,record.exp_code,record.run_num))
    df.to_csv(filename1)

for record in recordsNoC:
    filename=('/ocean/kramosmu/MITgcm/TracerExperiments/%s/%s/ptracersGlob.nc' %(record.exp_code,record.run_num))
    Tr1 = rout.getField(filename,'Tr1') 
    Tr2 = rout.getField(filename,'Tr2') 
     
    TrMass, TotTrMass = Tracer_AlongShelf(Tr1,Tr2, MaskCNoC, rA, hFacCNoC, drF[:], 227, 30,  180, 50,29)
    HCW = mtt.calc_HCW(Tr1, MaskCNoC, rA, hFacCNoC, drF[:],nzlim=29, yin=227, xin=0, xfin=359, zfin=30, xi=180, yi=50)
    
    raw_data = {'time' : time,'HCW': HCW,'TrMass': TrMass}
    df = pd.DataFrame(raw_data, columns = ['time' ,'HCW','TrMass'])
    filename1 = ('/ocean/kramosmu/MITgcm/TracerExperiments/%s/HCW_TrMass_%s%s.csv' %(record.exp_code,record.exp_code,record.run_num))
    df.to_csv(filename1)

    
    