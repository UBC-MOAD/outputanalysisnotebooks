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
        dTrdz = np.ma.empty((len(times),nz-2))
        ii = 0
        
        for tt in times:  
             
             #tracer profile at station
            profile = Tr1[tt,:,yi,xi]
            
            # dTr/dz for each station
            dTrdz[ii,:] = (profile[2:] - profile[:-2])/(-drC[3:]-drC[2:-1])
            
            ii = ii+1
            
        raw_data = {'drC' : drC[2:-1],'dTrdz_tt00': dTrdz[0,:],'dTrdz_tt02': dTrdz[1,:],'dTrdz_tt04': dTrdz[2,:],'dTrdz_tt06': dTrdz[3,:],
                    'dTrdz_tt08': dTrdz[4,:],'dTrdz_tt10': dTrdz[5,:],'dTrdz_tt12': dTrdz[6,:],'dTrdz_tt14': dTrdz[7,:],'dTrdz_tt16': dTrdz[8,:],
                    'dTrdz_tt18': dTrdz[9,:]}
        df = pd.DataFrame(raw_data, columns = ['drC', 'dTrdz_tt00', 'dTrdz_tt02', 'dTrdz_tt04', 'dTrdz_tt06', 'dTrdz_tt08','dTrdz_tt10',    
                                               'dTrdz_tt12','dTrdz_tt14', 'dTrdz_tt16','dTrdz_tt18' ])
        filename1 = ('../results/metricsDataFrames/dTr1dz_%s_%s.csv' % (runs,sname))
        df.to_csv(filename1)
        
    
        
 
        


