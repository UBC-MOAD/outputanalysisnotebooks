from netCDF4 import Dataset
import numpy as np
import pandas as pd
import canyon_tools.readout_tools as rout
#from MITgcmutils import rdmds # cant make it work

CGrid = '/data/kramosmu/results/TracerExperiments/CNTDIFF/run38/gridGlob.nc' # Smallest volume grid, closed bdy, no canyon.
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

MaskExpand = np.expand_dims(MaskC[:,:,0:360],0) 
maskExp = MaskExpand + np.zeros((nt,nz,ny,nx))    
    
bathy = rout.getField(CGrid, 'Depth')

# STATIONS
ys = [261]#[262,220,262,227,100,245,245,262,220]
xs = [200]#[60,60,180,180,180,160,200,300,300]

stations = ['UwH']#'UpSh','UpSl','CH','CM','CO','UpC','DnC','DnSh','DnSl']

tracers = ['Tr1']

#All experiments in CNT and 3D including no canyon one (run07)
expList = [#'/data/kramosmu/results/TracerExperiments/CNTDIFF/run36',
           #'/data/kramosmu/results/TracerExperiments/CNTDIFF/run37',
           #'/data/kramosmu/results/TracerExperiments/CNTDIFF/run38',
           #'/data/kramosmu/results/TracerExperiments/CNTDIFF/run45',
           #'/data/kramosmu/results/TracerExperiments/CNTDIFF/run51',
           #'/data/kramosmu/results/TracerExperiments/CNTDIFF/run67',
           #'/data/kramosmu/results/TracerExperiments/CNTDIFF/run68',
           #'/data/kramosmu/results/TracerExperiments/CNTDIFF/run69',
           #'/data/kramosmu/results/TracerExperiments/CNTDIFF/run70',
           #'/data/kramosmu/results/TracerExperiments/CNTDIFF/run71',
           #'/data/kramosmu/results/TracerExperiments/CNTDIFF/run72', 
           #'/data/kramosmu/results/TracerExperiments/CNTDIFF/run73',
           '/data/kramosmu/results/TracerExperiments/CNTDIFF/run75',
           '/data/kramosmu/results/TracerExperiments/CNTDIFF/run76', 
           #'/data/kramosmu/results/TracerExperiments/CNTDIFF/run79',
           #'/data/kramosmu/results/TracerExperiments/LOW_BF/run01',
           #'/data/kramosmu/results/TracerExperiments/LOWER_BF/run01',
           #'/data/kramosmu/results/TracerExperiments/LOWEST_BF/run01',
           #'/data/kramosmu/results/TracerExperiments/LOWEST_BF/run03',
           #'/data/kramosmu/results/TracerExperiments/LOWEST_BF/run05',
           #'/data/kramosmu/results/TracerExperiments/LOWEST_BF/run07',
           #'/data/kramosmu/results/TracerExperiments/LOWEST_BF/run11',
           ## '/data/kramosmu/results/TracerExperiments/BARKLEY/run01',
           ##'/data/kramosmu/results/TracerExperiments/CNTDIFF_LOW_SR_7Tr/run01',
           ##'/data/kramosmu/results/TracerExperiments/CNTDIFF_EXT_SHELF/run01',
           ]
            
expNames = [#'CNTDIFF_run36',
           #'CNTDIFF_run37',
           #'CNTDIFF_run38',
           #'CNTDIFF_run45',
           #'CNTDIFF_run51',
           #'CNTDIFF_run67',
           #'CNTDIFF_run68',
           #'CNTDIFF_run69',
           #'CNTDIFF_run70',
           #'CNTDIFF_run71', 
           #'CNTDIFF_run72',
           #'CNTDIFF_run73',
           'CNTDIFF_run75', 
           'CNTDIFF_run76',
           #'CNTDIFF_run79',
           #'LOW_BF_run01',
           #'LOWER_BF_run01',
           #'LOWEST_BF_run01',
           #'LOWEST_BF_run03',
           #'LOWEST_BF_run05',
           #'LOWEST_BF_run07',
           #'LOWEST_BF_run11'
##          # 'BARKLEY_run01',
           ##'PARAB_run01',
           ## 'CNTDIFF_Ext2x_run01',
]
           

  
times = [0,2,4,6,8,10,12,14,16,18]


for exp,runs in zip(expList,expNames):
    print(runs)
    CSptracers = ('%s/ptracersGlob.nc' %exp) 
    PTR = Dataset(CSptracers)
            
    print(runs,'done reading')
    trac = 'Tr1'
    for yi,xi,sname in zip(ys,xs,stations): 
        
        Tr1 = np.ma.masked_array(PTR.variables['Tr1'][:,:,:,0:360],mask=maskExp)
        Tr_profile = np.ma.empty((len(times),nz))
        ii = 0
        
        for tt in times:  
             
             #tracer profile at station
            
            Tr_profile[ii,:] = Tr1[tt,:,yi,xi]
            
            ii = ii+1
            
        raw_data = {'drC' : drC[:-1],'Tr_profile_tt00': Tr_profile[0,:],'Tr_profile_tt02': Tr_profile[1,:],'Tr_profile_tt04': Tr_profile[2,:],'Tr_profile_tt06': Tr_profile[3,:],
                    'Tr_profile_tt08': Tr_profile[4,:],'Tr_profile_tt10': Tr_profile[5,:],'Tr_profile_tt12': Tr_profile[6,:],'Tr_profile_tt14': Tr_profile[7,:],'Tr_profile_tt16': Tr_profile[8,:],
                    'Tr_profile_tt18': Tr_profile[9,:]}
        df = pd.DataFrame(raw_data, columns = ['drC', 'Tr_profile_tt00', 'Tr_profile_tt02', 'Tr_profile_tt04', 'Tr_profile_tt06', 'Tr_profile_tt08','Tr_profile_tt10',    
                                               'Tr_profile_tt12','Tr_profile_tt14', 'Tr_profile_tt16','Tr_profile_tt18' ])
        filename1 = ('../results/metricsDataFrames/%s_profile_%s_%s.csv' % (trac,runs,sname))
        df.to_csv(filename1)
        
    
        
 
        


