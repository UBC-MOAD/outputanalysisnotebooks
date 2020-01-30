
# ## Calculate and save HCW and tracer mass on shelf converting from molality to molarity


# Calculate and save HCW and tracer mass on shelf
from netCDF4 import Dataset
import numpy as np
import pandas as pd
import xarray as xr
import canyon_tools.metrics_tools as mtt
import canyon_tools.readout_tools as rout
RhoRef = 999.79998779



def calc_rho(RhoRef,T,S,alpha=2.0E-4, beta=7.4E-4):
    """-----------------------------------------------------------------------------
    calc_rho calculates the density profile using a linear equation of state.

    INPUT:
    state: xarray dataframe
    RhoRef : reference density at the same z as T and S slices. Can be a scalar or a
             vector, depending on the size of T and S.
    T, S   : should be 4D arrays
    alpha = 2.0E-4 # 1/degC, thermal expansion coefficient
    beta = 7.4E-4, haline expansion coefficient
    OUTPUT:
    rho - Density [nz]
    -----------------------------------------------------------------------------"""


    rho = RhoRef*np.ones(np.shape(T)) - alpha*(T[:]) + beta*(S[:])
    return rho

def call_rho(tslice,state,zslice,yslice,xslice):
    T = state.Temp.isel(T=tslice,Z=zslice,X=xslice,Y=yslice)
    S = state.S.isel(T=tslice,Z=zslice,X=xslice,Y=yslice)
    rho = calc_rho(RhoRef,T,S,alpha=2.0E-4, beta=7.4E-4)
    return(rho)


# In[3]:

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
    Tr1Mask=np.ma.array(Tr,mask=maskExp)

    trlim1 = TrMask[0,nzlim,yi,xi]
    trlim2 = TrMask[0,nzlim+1,yi,xi]

    #trlim = (trlim1+trlim2)/2.0
    trlim = (trlim1)

    print('tracer limit concentration is: ',trlim)
    print(trlim1,trlim2)

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

    #Get total mass of tracer on shelf
    Total_Tracer = np.ma.sum(np.ma.sum(np.ma.sum(ShelfVolume_exp*Tr1Mask[:,:zfin,yin:,:],axis = 1),axis=1),axis=1)

    return (MassTrHighConc, Total_Tracer)


# ### Input
# only change vars here

# In[ ]:

# Load grid files
CanyonGrid='/data/kramosmu/results/TracerExperiments/UPW_10TR_BF2_KV3D_AST/04_eps25_kv5E-3/gridGlob.nc'
CanyonGridOut = Dataset(CanyonGrid)

CanyonGridNoC='/data/kramosmu/results/TracerExperiments/UPW_10TR_BF2_AST/02_Ast03_No_Cny/gridGlob.nc'
CanyonGridOutNoC = Dataset(CanyonGridNoC)

CanyonState='/data/kramosmu/results/TracerExperiments/UPW_10TR_BF2_KV3D_AST/04_eps25_kv5E-3/stateGlob.nc'
CanyonStateOut = Dataset(CanyonState)

state =xr.open_dataset(CanyonState)

NoCState='/data/kramosmu/results/TracerExperiments/UPW_10TR_BF2_AST/02_Ast03_No_Cny/stateGlob.nc'
stateNoC =xr.open_dataset(NoCState)

# filenames ptracers canyon and no canyon cases
ptr_file = ('/data/kramosmu/results/TracerExperiments/UPW_10TR_BF2_KV3D_AST/04_eps25_kv5E-3/ptracersGlob.nc' )
ptr_file_NoC = ('/data/kramosmu/results/TracerExperiments/UPW_10TR_BF2_AST/02_Ast03_No_Cny/ptracersGlob.nc' )

# Grid params
nx = 616
ny = 360
nz = 104 # Orig. 90
nt = 19 # t dimension size

# Indices shelf box, etc
xi = 180
yi = 50
nzlim = 29 # Bar:39, Ast:29, Orig:29
zfin = 30 # Bar:40, Ast:30, Orig:30
xfin = 615
yin = 130 # Orig: 225

# Tracer keys
keys = ['Tr03','Tr09','Tr10']
keyAdv = 'Tr01' # tracer used to track water (linear)

# Experiment id
run = 'UPW_10TR_BF2_KV3D_AST_04'
run_NoC = 'UPW_10TR_BF2_AST_02'
exp = 'UPW_10TR_BF2_KV3D_AST'

# Grid variables
xc = rout.getField(CanyonGrid, 'XC') # x coords tracer cells
yc = rout.getField(CanyonGrid, 'YC') # y coords tracer cells
rc = CanyonGridOut.variables['RC']
dxg = rout.getField(CanyonGrid, 'dxG') # x coords tracer cells
dyg = rout.getField(CanyonGrid, 'dyG') # y coords tracer cells

bathy = rout.getField(CanyonGrid, 'Depth')
hFacC = CanyonGridOut.variables['HFacC'][:zfin+1,:,:]
hFacmasked = np.ma.masked_values(hFacC, 0)
MaskC = np.ma.getmask(hFacmasked)

bathyNoC = rout.getField(CanyonGridNoC, 'Depth')
hFacCNoC = CanyonGridOutNoC.variables['HFacC'][:zfin+1,:,:]
hFacmaskedNoC = np.ma.masked_values(hFacCNoC, 0)
MaskCNoC = np.ma.getmask(hFacmaskedNoC)

rA = rout.getField(CanyonGridNoC, 'rA')

z = CanyonStateOut.variables['Z']
drF = CanyonGridOut.variables['drF']
time = CanyonStateOut.variables['T']


# In[ ]:

for key in keys:
    Tr = np.empty((nt,zfin+1,ny,nx))
    for tt in range(nt):
        Tr_M = Dataset(ptr_file).variables[key][tt,:zfin+1,:,:]
        density = call_rho(tt,state,slice(0,zfin+1),slice(0,ny),slice(0,nx))
        Tr[tt,:,:,:] = density*Tr_M/1000
    
    del Tr_M
    del density
    
    TrAdv = Dataset(ptr_file).variables[keyAdv][:,:zfin+1,:,:]

    TrMassHCW, TotTrMass = Tracer_AlongShelf(Tr,TrAdv, MaskCNoC[:zfin+1,:,:], rA, hFacCNoC, drF[:zfin+1],yin,zfin,xi,yi,nzlim)
    HCW = mtt.calc_HCW(TrAdv, MaskCNoC[:zfin+1,:,:], rA, hFacCNoC, drF[:zfin+1],nzlim=nzlim, yin=yin,
                       xin=0, xfin=xfin, zfin=zfin, xi=xi, yi=yi)

    raw_data = {'time' : time,'HCW': HCW,'TrMassHCW': TrMassHCW,'TotTrMass':TotTrMass}
    df = pd.DataFrame(raw_data, columns = ['time' ,'HCW','TrMassHCW','TotTrMass'])

    filename1 = ('/data/kramosmu/results/TracerExperiments/%s/HCW_TrMass_%s_%s_M.csv' %(exp,key,run))
    df.to_csv(filename1)
    print(filename1)


# In[ ]:

#for key in keys:

#    TrNoC = np.empty((nt,zfin+1,ny,nx))
#    for tt in range(nt):
#        TrNoC_M = Dataset(ptr_file_NoC).variables[key][tt,:zfin+1,:,:]
#        density = call_rho(tt,state,slice(0,zfin+1),slice(0,ny),slice(0,nx))
#        TrNoC[tt,:,:,:] = density*TrNoC_M/1000


#    TrNoCAdv = Dataset(ptr_file_NoC).variables[keyAdv][:,:zfin+1,:,:]

#    TrMassHCW, TotTrMass = Tracer_AlongShelf(TrNoC,TrNoCAdv, MaskCNoC, rA, hFacCNoC, drF[:zfin+1],yin,zfin,xi,yi,nzlim)
#    HCW = mtt.calc_HCW(TrNoCAdv, MaskCNoC[:zfin+1,:,:], rA, hFacCNoC, drF[:zfin+1],nzlim=nzlim, yin=yin,
#                       xin=0, xfin=xfin, zfin=zfin, xi=xi, yi=yi)

#    raw_data = {'time' : time,'HCW': HCW,'TrMassHCW': TrMassHCW,'TotTrMass':TotTrMass}
#    df = pd.DataFrame(raw_data, columns = ['time' ,'HCW','TrMassHCW','TotTrMass'])

#    filename2 = ('/data/kramosmu/results/TracerExperiments/%s/HCW_TrMass_%s_%s_M.csv' %(exp,key,run_NoC))
#    df.to_csv(filename2)
#    print(filename2)
