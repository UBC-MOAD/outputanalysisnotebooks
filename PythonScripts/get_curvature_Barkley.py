from netCDF4 import Dataset
import numpy as np
import pandas as pd
import canyon_tools.readout_tools as rout
#from MITgcmutils import rdmds # cant make it work

CGrid = '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run38/gridGlob.nc' # Smallest volume grid, closed bdy, no canyon.
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

MaskExpand = np.expand_dims(MaskC,0) 
maskExp = MaskExpand + np.zeros((nt,nz,ny,nx))    
    
bathy = rout.getField(CGrid, 'Depth')

# STATIONS
ys = 245 #[262,220,262,227,100,245,245,262,220]
xs = 200 #[60,60,180,180,180,160,200,300,300]

stations = 'DnC'#'UpSh','UpSl','CH','CM','CO','UpC','DnC','DnSh','DnSl']

tracersBar = ['Tr01','Tr02','Tr03','Tr04','Tr05','Tr06','Tr07','Tr08']
tracersPar = ['Tr1','Tr2','Tr3','Tr4','Tr5','Tr6','Tr7']


expList = ['/ocean/kramosmu/MITgcm/TracerExperiments/BARKLEY/run01',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF_LOW_SR_7Tr/run01',
           ]
            
expNames = [ 'BARKLEY_run01','PARAB_run01']
           
times = [0,2,4,6,8,10,12,14,16,18]


for exp,runs,tracersList in zip(expList,expNames,[tracersBar,tracersPar]):
    
    print(runs)
    CSptracers = ('%s/ptracersGlob.nc' %exp) 
        
    print(runs,'done reading')
    
    for trac in tracersList:
        
        print('getting tracer %s' %trac)
        
        data = rout.getField(CSptracers,trac)[:19,:,:,:]  # I need this beacuse parabolic nt is 20 instead of 19      
        Tr1 = np.ma.masked_array(data,mask=maskExp)
        dTr2dz2 = np.ma.empty((len(times),nz-2))
        ii = 0
        
        for tt in times:  
             
            #tracer profile at station
            profile = Tr1[tt,:,ys,xs]
            
            # dTr2/dz2 for each station
            dTr2dz2[ii,:] = (profile[2:] - 2*profile[1:-1] + profile[:-2])/(drC[3:]*drC[2:-1])
            
            ii = ii+1
            
        raw_data = {'dTr2dz2_tt00': dTr2dz2[0,:],'dTr2dz2_tt02': dTr2dz2[1,:],'dTr2dz2_tt04': dTr2dz2[2,:],
                    'dTr2dz2_tt06':dTr2dz2[3,:],'dTr2dz2_tt08': dTr2dz2[4,:],'dTr2dz2_tt10': dTr2dz2[5,:],
                    'dTr2dz2_tt12': dTr2dz2[6,:],'dTr2dz2_tt14': dTr2dz2[7,:],'dTr2dz2_tt16': dTr2dz2[8,:],
                    'dTr2dz2_tt18': dTr2dz2[9,:]}
        df = pd.DataFrame(raw_data, columns = ['dTr2dz2_tt00', 'dTr2dz2_tt02',                  'dTr2dz2_tt04','dTr2dz2_tt06','dTr2dz2_tt08','dTr2dz2_tt10', 'dTr2dz2_tt12','dTr2dz2_tt14', 'dTr2dz2_tt16','dTr2dz2_tt18' ])
        filename1 = ('../results/metricsDataFrames/dTr2dz2_Tr%s_%s_%s.csv' % (trac,runs,stations))
        df.to_csv(filename1)