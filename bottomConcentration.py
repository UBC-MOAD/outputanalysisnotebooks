
#KRM
import numpy as np

from math import *

import scipy.io

import scipy as spy

from netCDF4 import Dataset

import pandas as pd

import pylab as pl

import os 

import sys

lib_path = os.path.abspath('../../Building_canyon/BuildCanyon/PythonModulesMITgcm') # Add absolute path to my python scripts
sys.path.append(lib_path)

import ReadOutTools_MITgcm as rout 


#--------------------- Functions------------------------------------------------------------------------------------- 
def a_weight_mean(ConcArea,Area):
    
    sumNum = np.nansum(np.nansum(ConcArea,axis=1),axis=1)
    sumDen = np.nansum(Area)
    
    awmean = sumNum/sumDen
    return awmean

def mask2DCanyon(bathy, sbdepth=-152.5):
    '''Mask out the canyon from the shelf.
    bathy : depths 2D array from the grid file
    sbdepth: shelf depth, always negative float 
    Returns mask'''
    
    bathyMasked = np.ma.masked_less(-bathy, -152.5)
    return(bathyMasked.mask)

def ConcArea(Tr, hfac, ra, bathy, sbdepth=-152.5):
    '''Tr: tracer field (nt,nz,ny,nx)
       hfac: fraction of open cell at center (nz,ny,nx)
       ra: array of cell horizontal areas (ny,nx)
       bathy : depths 2D array from the grid file (ny,nx)
       sbdepth: shelf break depth (negative value)
       
       RETURNS:
       ConcArea = concentration at cell closest to bottom times its area (nt,ny,nx)
       Conc = cocnetration near bottom (nt,ny,nx)'''
    
    ConcArea = np.empty((19,360,360))
    Conc = np.empty((19,360,360))
    Area = np.empty((360,360))
    BottomInd = np.argmax(hfac[::-1,:,:]>0.0,axis=0) # start looking for first no-land cell from the bottom up.
    BottomInd = np.ones(np.shape(BottomInd))*89 - BottomInd # Get index of unreversed z axis

    print(np.shape(BottomInd))
    for tt in range(19):
        #print(tt)
        for i in range(360):
            for j in range(360):
                TrBottom = Tr[tt,BottomInd[i,j],i,j]
                ConcArea[tt,i,j] = TrBottom*ra[i,j]
                Conc[tt,i,j] = TrBottom
                Area[i,j] = ra[i,j]
    
    print(np.shape(ConcArea))
    
    maskShelf2D = mask2DCanyon(bathy, sbdepth)
    maskShelf = np.expand_dims(maskShelf2D,0) # expand along time dimension
    maskShelf = maskShelf + np.zeros(Conc.shape)
    
    

    #ConcAreaMasked = np.ma.masked_values(ConcDepths,-2.5)
    #ConcDepths[np.where(np.ma.getmask(ConcDepthsMasked)==True)] = np.nan

    return (np.ma.masked_array(ConcArea, mask=maskShelf),
	    np.ma.masked_array(Conc, mask=maskShelf), 
	    np.ma.masked_array(Area, mask=maskShelf2D),
	    )

#---------------------------------------------------------------------------------------------------------- 


NoCanyonGrid='/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run07/gridGlob.nc'
NoCanyonGridOut = Dataset(NoCanyonGrid)

CanyonGrid='/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run03/gridGlob.nc'
CanyonGridOut = Dataset(CanyonGrid)

CanyonState='/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run03/stateGlob.nc'
CanyonStateOut = Dataset(CanyonState)

nx = 360
ny = 360
nz = 90


hFacCNoC = rout.getField(NoCanyonGrid, 'HFacC')
MaskCNoC = rout.getMask(NoCanyonGrid, 'HFacC')
rANoC = rout.getField(NoCanyonGrid, 'rA')
bathyNoC = rout.getField(NoCanyonGrid, 'Depth')

hFacC = rout.getField(CanyonGrid, 'HFacC')
MaskC = rout.getMask(CanyonGrid, 'HFacC')
rA = rout.getField(CanyonGrid, 'rA')
bathy = rout.getField(CanyonGrid, 'Depth')

z = CanyonStateOut.variables['Z']
time = CanyonStateOut.variables['T']


ptracerListCanyon = ['/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run02/ptracersGlob.nc',
                     '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run03/ptracersGlob.nc',
                     '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run04/ptracersGlob.nc',
                     '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run11/ptracersGlob.nc',
                     '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run12/ptracersGlob.nc',
                     '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run14/ptracersGlob.nc',
                     '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run15/ptracersGlob.nc',
                     '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run16/ptracersGlob.nc',
                     '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run17/ptracersGlob.nc',
                     '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run18/ptracersGlob.nc',
                     '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run19/ptracersGlob.nc',
                     '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run20/ptracersGlob.nc',
                     '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run21/ptracersGlob.nc',
                     '/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run04/ptracersGlob.nc',
                     '/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run05/ptracersGlob.nc',
                     '/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run06/ptracersGlob.nc',
                     '/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run07/ptracersGlob.nc',
]

ptracerListFlat = ['/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run07/ptracersGlob.nc',
                   '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run22/ptracersGlob.nc',
                   '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run23/ptracersGlob.nc',
                   '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run24/ptracersGlob.nc',
                   '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run25/ptracersGlob.nc',
                   '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run26/ptracersGlob.nc',
                   '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run27/ptracersGlob.nc',
                   '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run28/ptracersGlob.nc',
                   '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run30/ptracersGlob.nc',
              
]

labelsListCanyon = ['High iso',
                    'Base', 
                    'low iso',
                    'kv=1E-4',
                    'kv=1E-3',
                    'N=3.9E-3',
                    'N=6.3E-3',
                    'N=3.0E-3',
                    'kv=1E-7',
                    'f=7.68E-5',
                    'f=4.84E-5',
                    'kv=3.8E-5',
                    'kv=2.8E-5',
                    'kv_can=1E-7, kv_out=1E-3',
                    'kv_can=1E-7, kv_out=1E-4',
                    'kv_can=1E-5, kv_out=1E-3',
                    'kv_can=1E-5, kv_out=1E-4',
]

labelsListFlat = ['Base flat',
                  'f=7.68E-5 flat',
                  'f=4.84E-5 flat',
                  'kv=1E-4 flat',
                  'kv=1E-3 flat',
                  'N=3.9E-3 flat',
                  'N=6.3E-3 flat',
                  'N=3.0E-3 flat',
                  'kv=1E-7 flat',
]








tracerListCanyon = ['Tr1','Tr1','Tr1',
                    'Tr2','Tr3','Tr1',
                    'Tr1','Tr1','Tr3',
                    'Tr1','Tr1','Tr2',
                    'Tr3','Tr1','Tr1',
                    'Tr1','Tr1',
]

tracerListFlat = ['Tr1','Tr1','Tr1',
                  'Tr1','Tr1','Tr1',
                  'Tr1','Tr1','Tr1',
]


nt = len(time)
nrunsCanyon = len(ptracerListCanyon)
nrunsFlat = len(ptracerListFlat)

CACanyon = np.empty((nt,nrunsCanyon)) # Concentration * area integrated over shelf bottom
CAFlat = np.empty((nt,nrunsFlat)) # Concentration * area integrated over shelf bottom


ii = 0

for ptracerFile, tracerID in zip(ptracerListCanyon, tracerListCanyon):
    
    Tr = rout.getField(ptracerFile, tracerID) 
    print(ptracerFile)
    concArea,conc,area=ConcArea(Tr, hFacC, rA, bathy)
    CACanyon[:,ii] = a_weight_mean(concArea,area)
    
    
    ii = ii + 1

raw_data = {'time':time, 
            'ConcArea02':CACanyon[:,0],
            'ConcArea03':CACanyon[:,1],
            'ConcArea04':CACanyon[:,2],
            'ConcArea11':CACanyon[:,3],
            'ConcArea12':CACanyon[:,4],
            'ConcArea14':CACanyon[:,5],
            'ConcArea15':CACanyon[:,6],
            'ConcArea16':CACanyon[:,7],
            'ConcArea17':CACanyon[:,8],
            'ConcArea18':CACanyon[:,9],
            'ConcArea19':CACanyon[:,10],
            'ConcArea20':CACanyon[:,11],
            'ConcArea21':CACanyon[:,12],
            'ConcArea3D04':CACanyon[:,13],
            'ConcArea3D05':CACanyon[:,14],
            'ConcArea3D06':CACanyon[:,15],
            'ConcArea3D07':CACanyon[:,16],
           }
           
           
           
           
          
df = pd.DataFrame(raw_data, columns = ['day', 
                                       'ConcArea02',
                                       'ConcArea03',
                                       'ConcArea04',
                                       'ConcArea11',
                                       'ConcArea12',
                                       'ConcArea14',
                                       'ConcArea15',
                                       'ConcArea16',
                                       'ConcArea17',
                                       'ConcArea18',
                                       'ConcArea19',
                                       'ConcArea20',
                                       'ConcArea21',
                                       'ConcArea3D04',
				       'ConcArea3D05',
				       'ConcArea3D06',
				       'ConcArea3D07',                                       
])
    
filename1 = ('results/metricsDataFrames/bottomConcentrationAreaCanyonRuns.csv' )
df.to_csv(filename1)
    
print(filename1)



nrunsFlat = len(ptracerListFlat)

CAFlat = np.empty((nt,nrunsFlat)) # Concentration * area integrated over shelf bottom

CFlat = np.empty((nt,nrunsFlat)) # Concentration * area integrated over shelf bottom

ii = 0   
for ptracerFile, tracerID in zip(ptracerListFlat, tracerListFlat):
    
    Tr = rout.getField(ptracerFile, tracerID) 
    print(ptracerFile)
    concArea,conc,area=ConcArea(Tr, hFacCNoC, rANoC, bathyNoC)
    CAFlat[:,ii] = a_weight_mean(concArea,area)
    
    
    
    ii = ii + 1

raw_data = {'time':time,
            'ConcArea07':CAFlat[:,0],
            'ConcArea22':CAFlat[:,1],
            'ConcArea23':CAFlat[:,2],
            'ConcArea24':CAFlat[:,3],
            'ConcArea25':CAFlat[:,4],
            'ConcArea26':CAFlat[:,5],
            'ConcArea27':CAFlat[:,6],
            'ConcArea28':CAFlat[:,7],
            'ConcArea30':CAFlat[:,8],
            }

dfFlat = pd.DataFrame(raw_data, columns = ['day', 
                                       'ConcArea07',
                                       'ConcArea22',
                                       'ConcArea23',
                                       'ConcArea24',
                                       'ConcArea25',
                                       'ConcArea26',
                                       'ConcArea27',
                                       'ConcArea28',
                                       'ConcArea30',
                                       ])
    
filename2 = ('results/metricsDataFrames/bottomConcentrationAreaFlatRuns.csv' )
dfFlat.to_csv(filename2)
    
print(filename2)
    
    
