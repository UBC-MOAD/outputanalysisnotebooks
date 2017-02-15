from netCDF4 import Dataset
import numpy as np
import pandas as pd
import canyon_tools.readout_tools as rout
#from MITgcmutils import rdmds # cant make it work

CGrid = '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run38/gridGlob.nc' # Smallest volume grid, closed bdy, no canyon.
phiHyd = '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run38/phiHydGlob.nc'
pout = Dataset(phiHyd)
CGridOut = Dataset(CGrid)

# General input

nx = 360
ny = 360
nz = 90
nt = 19 # t dimension size 

rc = CGridOut.variables['RC']

xc = rout.getField(CGrid, 'XC') # x coords tracer cells
yc = rout.getField(CGrid, 'YC') # y coords tracer cells

drF = CGridOut.variables['drF'] # vertical distance between faces
drC = CGridOut.variables['drC'] # vertical distance between centers

hFacC = rout.getField(CGrid, 'HFacC')
MaskC = rout.getMask(CGrid, 'HFacC')
rA = rout.getField(CGrid, 'rA')

Tp = pout.variables['T']
bathy = rout.getField(CGrid, 'Depth')

# STATIONS
ys = [262,220,262,227,100,245,245,262,220]
xs = [60,60,180,180,180,160,200,300,300]
stations = ['UpSh','UpSl','CH','CM','CO','UpC','DnC','DnSh','DnSl']

#All experiments in CNT and 3D including no canyon one (run07)
expList = ['/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run36',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run37',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run38',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run43',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run44',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run45',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run46',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run51',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run52',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run55',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run56',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run57',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run61',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run62',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run63',
           '/ocean/kramosmu/MITgcm/TracerExperiments/3DVISC/run01',
           '/ocean/kramosmu/MITgcm/TracerExperiments/3DVISC/run02',
           '/ocean/kramosmu/MITgcm/TracerExperiments/3DVISC/run03',
           '/ocean/kramosmu/MITgcm/TracerExperiments/3DVISC/run04',
           '/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run04',
           '/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run05',
           '/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run06',
           '/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run07']
           
expNames = ['CNTDIFF_run36',
           'CNTDIFF_run37',
           'CNTDIFF_run38',
           'CNTDIFF_run43',
           'CNTDIFF_run44',
           'CNTDIFF_run45',
           'CNTDIFF_run46',
           'CNTDIFF_run51',
           'CNTDIFF_run52',
           'CNTDIFF_run55',
           'CNTDIFF_run56',
           'CNTDIFF_run57',
           'CNTDIFF_run61',
           'CNTDIFF_run62',
           'CNTDIFF_run63',
           '3DVISC_run01',
           '3DVISC_run02',
           '3DVISC_run03',
           '3DVISC_run04',
           '3DDIFF_run04',
           '3DDIFF_run05',
           '3DDIFF_run06',
           '3DDIFF_run07']
           

#RhoRef = np.squeeze(rdmds('/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run38/RhoRef')) # I cannot make this function work
RhoRef = 999.79998779 # It is constant throughout my runs

nzlim = 30
zfin = 30
xi = 180
yi = 50
xh1=120
xh2=240
yh1=227
yh2=267
g = 9.81 # ms^-2

alpha = 2.0E-4 # 1/degC
beta = 7.4E-4
  
times = [0,2,4,6,8,10,12,14,16,18]

for exp,runs in zip(expList,expNames):
    print(runs)
    CState = ('%s/stateGlob.nc' %exp) 
        
    Temp = rout.getField(CState,'Temp')
    S = rout.getField(CState,'S')
    P = rout.getField(phiHyd,'phiHyd')
        
    MaskExpand = np.expand_dims(MaskC,0) 
    maskExp = MaskExpand + np.zeros((Temp).shape)    
    
    TempMask=np.ma.array(Temp,mask=maskExp)   
    SMask=np.ma.array(S,mask=maskExp)   
    print(runs,'done reading')
    
    for yi,xi,sname in zip(ys,xs,stations): # station indices
        Rho = np.ma.empty((len(times),nz))
        ii = 0
        
        for tt in times:  
            
            #Linear eq. of state 
            rho = RhoRef*(np.ones(np.shape(TempMask[tt,:,yi,xi])) - alpha*(TempMask[tt,:,yi,xi]) + beta*(SMask[tt,:,yi,xi]))
            Rho[ii,:]= rho
            ii = ii+1
        
        raw_data = {'drC' : drC[:-1],'rho_tt00': Rho[0,:],'rho_tt02': Rho[1,:],'rho_tt04': Rho[2,:],'rho_tt06': Rho[3,:],
                    'rho_tt08': Rho[4,:],'rho_tt10': Rho[5,:],'rho_tt12': Rho[6,:],'rho_tt14': Rho[7,:],'rho_tt16': Rho[8,:],
                    'rho_tt18': Rho[9,:]}
        df = pd.DataFrame(raw_data, columns = ['drC', 'rho_tt00', 'rho_tt02', 'rho_tt04', 'rho_tt06', 'rho_tt08','rho_tt10',    
                                               'rho_tt12','rho_tt14', 'rho_tt16','rho_tt18' ])
        filename1 = ('../results/metricsDataFrames/rho_%s_%s.csv' % (runs,sname))
        df.to_csv(filename1)
        
    
        
 
        

