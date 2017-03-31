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
ys = [262,220,262,227,100,245,245,262,220]
xs = [60,60,180,180,180,160,200,300,300]
stations = ['UpSh','UpSl','CH','CM','CO','UpC','DnC','DnSh','DnSl']

#All experiments in CNT and 3D including no canyon one (run07)
expList = [#'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run36',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run37',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run38',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run43',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run44',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run45',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run46',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run51',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run52',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run55',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run56',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run57',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run61',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run62',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run63',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run67',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run68',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run69',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run70',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run71',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run72', 
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run73',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run75',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run76', 
           #'/ocean/kramosmu/MITgcm/TracerExperiments/3DVISC/run01',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/3DVISC/run02',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/3DVISC/run03',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/3DVISC/run04',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/3DVISC/run06',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run04',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run05',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run06',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run07',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/FORCING_SPNDN/run01',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/EW_OBCS/run06',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/LOW_BF/run01',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/LOWER_BF/run01',
           #'/ocean/kramosmu/MITgcm/TracerExperiments/LOWEST_BF/run01',
           '/ocean/kramosmu/MITgcm/TracerExperiments/LOWEST_BF/run03',
           '/ocean/kramosmu/MITgcm/TracerExperiments/LOWEST_BF/run05',
           '/ocean/kramosmu/MITgcm/TracerExperiments/LOWEST_BF/run07',
]
           
expNames = [#'CNTDIFF_run36',
           #'CNTDIFF_run37',
           #'CNTDIFF_run38',
           #'CNTDIFF_run43',
           #'CNTDIFF_run44',
           #'CNTDIFF_run45',
           #'CNTDIFF_run46',
           #'CNTDIFF_run51',
           #'CNTDIFF_run52',
           #'CNTDIFF_run55',
           #'CNTDIFF_run56',
           #'CNTDIFF_run57',
           #'CNTDIFF_run61',
           #'CNTDIFF_run62',
           #'CNTDIFF_run63',
           #'CNTDIFF_run67',
           #'CNTDIFF_run68',
           #'CNTDIFF_run69',
           #'CNTDIFF_run70',
           #'CNTDIFF_run71', 
           #'CNTDIFF_run72',
           #'CNTDIFF_run73',
           #'CNTDIFF_run75', 
           #'CNTDIFF_run76',
           #'3DVISC_run01',
           #'3DVISC_run02',
           #'3DVISC_run03',
           #'3DVISC_run04',
           #'3DVISC_run06',
           #'3DDIFF_run04',
           #'3DDIFF_run05',
           #'3DDIFF_run06',
           #'3DDIFF_run07',
           #'FORCING_SPNDN_run01',
           #'EW_OBCS_run06',
           #'LOW_BF_run01',
           #'LOWER_BF_run01',
           #'LOWEST_BF_run01',
           'LOWEST_BF_run03',
           'LOWEST_BF_run05',
           'LOWEST_BF_run07',
]
           

  
times = [0,2,4,6,8,10,12,14,16,18]

for exp,runs in zip(expList,expNames):
    print(runs)
    CSptracers = ('%s/ptracersGlob.nc' %exp) 
        
    Tr1 = np.ma.masked_array(rout.getField(CSptracers,'Tr1'),mask=maskExp)
            
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
        
    
        
 
        


