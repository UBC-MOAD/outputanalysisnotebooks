from netCDF4 import Dataset
import numpy as np
import pandas as pd
import canyon_tools.readout_tools as rout
#from MITgcmutils import rdmds # cant make it work

CGrid = '/data/kramosmu/results/TracerExperiments/3DVISC_REALISTIC/run01/gridGlob.nc' # Smallest volume grid, closed bdy, no canyon.
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
ys = [262,220,262,227,100,245,245,262,220]
xs = [60,60,180,180,180,160,200,300,300]
stations = ['UpSh','UpSl','CH','CM','CO','UpC','DnC','DnSh','DnSl']

#All experiments in CNT and 3D including no canyon one (run07)
expList = ['/data/kramosmu/results/TracerExperiments/3DVISC_REALISTIC/run01']
           
expNames = ['3DVISC_REALISTIC_run01']
           

  
times = [0,2,4,6,8,10,12,14,16,18]

for exp,runs in zip(expList,expNames):
    print(runs)
    CSptracers = ('%s/ptracersGlob.nc' %exp) 
    PTR = Dataset(CSptracers)     
    Tr1 = np.ma.masked_array(PTR.variables['Tr1'][:,:,:,0:360],mask=maskExp)
            
    print(runs,'done reading')
    
    for yi,xi,sname in zip(ys,xs,stations): # station indices
        profile = np.ma.empty((len(times),nz))
        ii = 0
        
        for tt in times:  
             
             #tracer profile at station
            profile[ii,:] = Tr1[tt,:,yi,xi]
            
            
            ii = ii+1
            
        raw_data = {'rC' : rc[:],'Tr_profile_tt00': profile[0,:],'Tr_profile_tt02': profile[1,:],'Tr_profile_tt04': profile[2,:],'Tr_profile_tt06': profile[3,:],
                    'Tr_profile_tt08': profile[4,:],'Tr_profile_tt10': profile[5,:],'Tr_profile_tt12': profile[6,:],'Tr_profile_tt14': profile[7,:],'Tr_profile_tt16': profile[8,:],
                    'Tr_profile_tt18': profile[9,:]}
        df = pd.DataFrame(raw_data, columns = ['rC', 'Tr_profile_tt00', 'Tr_profile_tt02', 'Tr_profile_tt04', 'Tr_profile_tt06', 'Tr_profile_tt08','Tr_profile_tt10',    
                                               'Tr_profile_tt12','Tr_profile_tt14', 'Tr_profile_tt16','Tr_profile_tt18' ])
        filename1 = ('../results/metricsDataFrames/Tr1_profile_%s_%s.csv' % (runs,sname))
        df.to_csv(filename1)
        
    
        
 
        


