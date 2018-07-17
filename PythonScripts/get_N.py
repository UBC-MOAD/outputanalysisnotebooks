from netCDF4 import Dataset
import numpy as np
import pandas as pd
import canyon_tools.readout_tools as rout
#from MITgcmutils import rdmds # cant make it work

CGrid = '/data/kramosmu/results/TracerExperiments/CNTDIFF/run38/gridGlob.nc' # Smallest volume grid, closed bdy, no canyon.
phiHyd = '/data/kramosmu/results/TracerExperiments/CNTDIFF/run38/phiHydGlob.nc'
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


bathy = rout.getField(CGrid, 'Depth')

# STATIONS
ys = [#262,220,262,227,100,245,
      240,#261,
      #245,262,220,
      ]
xs = [#60,60,180,180,180,160,
      180,#200,
      #200,300,300,
      ]
stations = [#'UpSh','UpSl','CH','CM','CO','UpC',
            'Mid',#'UwH'#'DnC','DnSh','DnSl',
            ]

#All experiments in CNT and 3D including no canyon one (run07)
expList = ['/data/kramosmu/results/TracerExperiments/CNTDIFF/run36',
           '/data/kramosmu/results/TracerExperiments/CNTDIFF/run37',
           '/data/kramosmu/results/TracerExperiments/CNTDIFF/run38',
           '/data/kramosmu/results/TracerExperiments/CNTDIFF/run45',
           '/data/kramosmu/results/TracerExperiments/CNTDIFF/run51',
           '/data/kramosmu/results/TracerExperiments/CNTDIFF/run67',
           '/data/kramosmu/results/TracerExperiments/CNTDIFF/run68',
           #'/data/kramosmu/results/TracerExperiments/CNTDIFF/run69',
           '/data/kramosmu/results/TracerExperiments/CNTDIFF/run70',
           '/data/kramosmu/results/TracerExperiments/CNTDIFF/run71',
           '/data/kramosmu/results/TracerExperiments/CNTDIFF/run72', 
           '/data/kramosmu/results/TracerExperiments/CNTDIFF/run73',
           '/data/kramosmu/results/TracerExperiemnts/CNTDIFF/run75',
           '/data/kramosmu/results/TracerExperiments/CNTDIFF/run81',
           '/data/kramosmu/results/TracerExperiments/CNTDIFF/run82',
           '/data/kramosmu/results/TracerExperiments/CNTDIFF/run79',  
           ###'/data/kramosmu/results/TracerExperiments/FORCING_SPNDN/run01',
           ###'/data/kramosmu/results/TracerExperiments/EW_OBCS/run06',
           '/data/kramosmu/results/TracerExperiments/LOW_BF/run01',
           '/data/kramosmu/results/TracerExperiments/LOWER_BF/run01',
           '/data/kramosmu/results/TracerExperiments/LOWEST_BF/run01',
           '/data/kramosmu/results/TracerExperiments/LOWEST_BF/run03',
           '/data/kramosmu/results/TracerExperiments/LOWEST_BF/run05',
           '/data/kramosmu/results/TracerExperiments/LOWEST_BF/run07',
           '/data/kramosmu/results/TracerExperiments/LOWEST_BF/run11',
           ##'/data/kramosmu/results/TracerExperiments/BARKLEY/run01',
           ##'/data/kramosmu/results/TracerExperiments/CNTDIFF_LOW_SR_7Tr/run01',
           ##'/data/kramosmu/results/TracerExperiments/CNTDIFF_EXT_SHELF/run01',
           ]
           
expNames = ['CNTDIFF_run36',
           'CNTDIFF_run37',
           'CNTDIFF_run38',
           'CNTDIFF_run45',
           'CNTDIFF_run51',
           'CNTDIFF_run67',
           'CNTDIFF_run68',
           #'CNTDIFF_run69',
           'CNTDIFF_run70',
           'CNTDIFF_run71', 
           'CNTDIFF_run72',
           'CNTDIFF_run73',
           'CNTDIFF_run75',
           'CNTDIFF_run81', 
           'CNTDIFF_run82',
           'CNTDIFF_run79', 
            ###'FORCING_SPNDN_run01',
           ###'EW_OBCS_run06',
           'LOW_BF_run01',
           'LOWER_BF_run01',
           'LOWEST_BF_run01',
           'LOWEST_BF_run03',
           'LOWEST_BF_run05',
           'LOWEST_BF_run07',
           'LOWEST_BF_run11',
           #'BARKLEY_run01',
           ##'PARAB_run01',
           ##'CNTDIFF_Ext2x_run01',
]

           

#RhoRef = np.squeeze(rdmds('/data/kramosmu/results/TracerExperiments/CNTDIFF/run38/RhoRef')) # I cannot make this function work
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
    CState = Dataset('%s/stateGlob.nc' %exp) 
    CPhi = Dataset('%s/phiHydGlob.nc' %exp)
    Temp = CState.variables['Temp'][:,:,:,0:360]
    S = CState.variables['S'][:,:,:,0:360]
    P = CPhi.variables['phiHyd'][:,:,:,0:360]
        
    MaskExpand = np.expand_dims(MaskC[:,:,0:360],0) 
    maskExp = MaskExpand + np.zeros((Temp).shape)    
    
    TempMask=np.ma.array(Temp,mask=maskExp)   
    SMask=np.ma.array(S,mask=maskExp)   
    print(runs,'done reading')
    
    for yi,xi,sname in zip(ys,xs,stations): # station indices
        N = np.ma.empty((len(times),nz-2))
        N2 = np.ma.empty((len(times),nz-2))
        ii = 0
        
        for tt in times:  
            
            #Linear eq. of state 
            rho = RhoRef*(np.ones(np.shape(TempMask[tt,:,yi,xi])) - alpha*(TempMask[tt,:,yi,xi]) + beta*(SMask[tt,:,yi,xi]))
            
            # N^2 for each station
            N[ii,:] =  ((-g/RhoRef)*((rho[2:] - rho[:-2])/(-drC[3:]-drC[2:-1])))**(0.5)
            N2[ii,:] = ((-g/RhoRef)*((rho[2:] - rho[:-2])/(-drC[3:]-drC[2:-1])))            
            ii = ii+1
        
        raw_data = {'drC' : drC[2:-1],'N_tt00': N[0,:],'N_tt02': N[1,:],'N_tt04': N[2,:],'N_tt06': N[3,:],
                    'N_tt08': N[4,:],'N_tt10': N[5,:],'N_tt12': N[6,:],'N_tt14': N[7,:],'N_tt16': N[8,:],
                    'N_tt18': N[9,:]}

        raw_data2 = {'drC' : drC[2:-1],'N2_tt00': N2[0,:],'N2_tt02': N2[1,:],'N2_tt04': N2[2,:],'N2_tt06': N2[3,:],
                    'N2_tt08': N2[4,:],'N2_tt10': N2[5,:],'N2_tt12': N2[6,:],'N2_tt14': N2[7,:],'N2_tt16': N2[8,:],
                    'N2_tt18': N2[9,:]}
        df = pd.DataFrame(raw_data, columns = ['drC', 'N_tt00', 'N_tt02', 'N_tt04', 'N_tt06', 'N_tt08','N_tt10',    
                                               'N_tt12','N_tt14', 'N_tt16','N_tt18' ])
        df2 = pd.DataFrame(raw_data2, columns = ['drC', 'N2_tt00', 'N2_tt02', 'N2_tt04', 'N2_tt06', 'N2_tt08','N2_tt10',
                                               'N2_tt12','N2_tt14', 'N2_tt16','N2_tt18' ])          
        filename1 = ('../results/metricsDataFrames/N_%s_%s.csv' % (runs,sname))
        filename2 = ('../results/metricsDataFrames/N2_%s_%s.csv' % (runs,sname))        
        df.to_csv(filename1)
        df2.to_csv(filename2)
        
    
        
 
        


