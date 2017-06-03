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

import savitzky_golay as sg

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
    ConcFiltered = np.empty((19,360,360))
    ConcAreaFiltered = np.empty((19,360,360))
    Area = np.empty((360,360))
    BottomInd = np.argmax(hfac[::-1,:,:]>0.0,axis=0) # start looking for first no-land cell from the bottom up.
    BottomInd = np.ones(np.shape(BottomInd))*89 - BottomInd # Get index of unreversed z axis
    
    print(np.shape(BottomInd))
    for tt in range(19):
        #print(tt)
        for j in range(360):
            for i in range(360):
                
                TrBottom = Tr[tt,BottomInd[i,j],i,j]
                ConcArea[tt,i,j] = TrBottom*ra[i,j]
                Conc[tt,i,j] = TrBottom
                Area[i,j] = ra[i,j]
                
            # Filter step noise
            ConcFiltered[tt,:,j] = sg.savitzky_golay(Conc[tt,:,j], 7,3) 
            ConcAreaFiltered[tt,:,j] = sg.savitzky_golay(ConcArea[tt,:,j], 7,3)     
    print(np.shape(ConcArea))
    
    maskShelf2D = mask2DCanyon(bathy, sbdepth)
    maskShelf = np.expand_dims(maskShelf2D,0) # expand along time dimension
    maskShelf = maskShelf + np.zeros(Conc.shape)
    
    return (np.ma.masked_array(ConcAreaFiltered, mask=maskShelf),
            np.ma.masked_array(ConcFiltered, mask=maskShelf),
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

CACanyonOut = np.empty((nt,nrunsCanyon)) # Concentration * area integrated over shelf bottom
CACanyonIn = np.empty((nt,nrunsCanyon)) # Concentration * area integrated over shelf bottom

CAFlatOut = np.empty((nt,nrunsFlat)) # Concentration * area integrated over shelf bottom
CAFlatIn = np.empty((nt,nrunsFlat)) # Concentration * area integrated over shelf bottom


ii = 0

for ptracerFile, tracerID in zip(ptracerListCanyon, tracerListCanyon):
    
    Tr = rout.getField(ptracerFile, tracerID) 
    print(ptracerFile)
    concArea, conc, area = ConcArea(Tr, hFacC, rA, bathy)
    
    CACanyonOut[:,ii] = a_weight_mean(concArea[:,:267,:],area[:267,:])
    CACanyonIn[:,ii] = a_weight_mean(concArea[:,267:,:],area[267:,:])
    
    
    ii = ii + 1

raw_data = {'time':time, 
            'ConcArea02Out':CACanyonOut[:,0],
            'ConcArea03Out':CACanyonOut[:,1],
            'ConcArea04Out':CACanyonOut[:,2],
            'ConcArea11Out':CACanyonOut[:,3],
            'ConcArea12Out':CACanyonOut[:,4],
            'ConcArea14Out':CACanyonOut[:,5],
            'ConcArea15Out':CACanyonOut[:,6],
            'ConcArea16Out':CACanyonOut[:,7],
            'ConcArea17Out':CACanyonOut[:,8],
            'ConcArea18Out':CACanyonOut[:,9],
            'ConcArea19Out':CACanyonOut[:,10],
            'ConcArea20Out':CACanyonOut[:,11],
            'ConcArea21Out':CACanyonOut[:,12],
            'ConcArea3D04Out':CACanyonOut[:,13],
            'ConcArea3D05Out':CACanyonOut[:,14],
            'ConcArea3D06Out':CACanyonOut[:,15],
            'ConcArea3D07Out':CACanyonOut[:,16],
            'ConcArea02In':CACanyonIn[:,0],
            'ConcArea03In':CACanyonIn[:,1],
            'ConcArea04In':CACanyonIn[:,2],
            'ConcArea11In':CACanyonIn[:,3],
            'ConcArea12In':CACanyonIn[:,4],
            'ConcArea14In':CACanyonIn[:,5],
            'ConcArea15In':CACanyonIn[:,6],
            'ConcArea16In':CACanyonIn[:,7],
            'ConcArea17In':CACanyonIn[:,8],
            'ConcArea18In':CACanyonIn[:,9],
            'ConcArea19In':CACanyonIn[:,10],
            'ConcArea20In':CACanyonIn[:,11],
            'ConcArea21In':CACanyonIn[:,12],
            'ConcArea3D04In':CACanyonIn[:,13],
            'ConcArea3D05In':CACanyonIn[:,14],
            'ConcArea3D06In':CACanyonIn[:,15],
            'ConcArea3D07In':CACanyonIn[:,16],
           }
           
           
           
           
          
df = pd.DataFrame(raw_data, columns = ['day', 
                                       'ConcArea02Out',
                                       'ConcArea03Out',
                                       'ConcArea04Out',
                                       'ConcArea11Out',
                                       'ConcArea12Out',
                                       'ConcArea14Out',
                                       'ConcArea15Out',
                                       'ConcArea16Out',
                                       'ConcArea17Out',
                                       'ConcArea18Out',
                                       'ConcArea19Out',
                                       'ConcArea20Out',
                                       'ConcArea21Out',
                                       'ConcArea3D04Out',
                                       'ConcArea3D05Out',
                                       'ConcArea3D06Out',
                                       'ConcArea3D07Out', 
                                       'ConcArea02In',
                                       'ConcArea03In',
                                       'ConcArea04In',
                                       'ConcArea11In',
                                       'ConcArea12In',
                                       'ConcArea14In',
                                       'ConcArea15In',
                                       'ConcArea16In',
                                       'ConcArea17In',
                                       'ConcArea18In',
                                       'ConcArea19In',
                                       'ConcArea20In',
                                       'ConcArea21In',
                                       'ConcArea3D04In',
                                       'ConcArea3D05In',
                                       'ConcArea3D06In',
                                       'ConcArea3D07In',  
])
    
filename1 = ('results/metricsDataFrames/bottomConcentrationAreaFiltCanyonRunsCoastalInt.csv' )
df.to_csv(filename1)
    
print(filename1)



nrunsFlat = len(ptracerListFlat)


ii = 0   
for ptracerFile, tracerID in zip(ptracerListFlat, tracerListFlat):
    
    Tr = rout.getField(ptracerFile, tracerID) 
    print(ptracerFile)
    concArea, conc, area = ConcArea(Tr, hFacCNoC, rANoC, bathyNoC)
    CAFlatOut[:,ii] = a_weight_mean(concArea[:,:267,:],area[:267,:])
    CAFlatIn[:,ii] = a_weight_mean(concArea[:,267:,:],area[267:,:])
    
    
    
    ii = ii + 1

raw_data = {'time':time,
            'ConcArea07Out':CAFlatOut[:,0],
            'ConcArea22Out':CAFlatOut[:,1],
            'ConcArea23Out':CAFlatOut[:,2],
            'ConcArea24Out':CAFlatOut[:,3],
            'ConcArea25Out':CAFlatOut[:,4],
            'ConcArea26Out':CAFlatOut[:,5],
            'ConcArea27Out':CAFlatOut[:,6],
            'ConcArea28Out':CAFlatOut[:,7],
            'ConcArea30Out':CAFlatOut[:,8],
            'ConcArea07In':CAFlatIn[:,0],
            'ConcArea22In':CAFlatIn[:,1],
            'ConcArea23In':CAFlatIn[:,2],
            'ConcArea24In':CAFlatIn[:,3],
            'ConcArea25In':CAFlatIn[:,4],
            'ConcArea26In':CAFlatIn[:,5],
            'ConcArea27In':CAFlatIn[:,6],
            'ConcArea28In':CAFlatIn[:,7],
            'ConcArea30In':CAFlatIn[:,8],
            }

dfFlat = pd.DataFrame(raw_data, columns = ['day', 
                                       'ConcArea07Out',
                                       'ConcArea22Out',
                                       'ConcArea23Out',
                                       'ConcArea24Out',
                                       'ConcArea25Out',
                                       'ConcArea26Out',
                                       'ConcArea27Out',
                                       'ConcArea28Out',
                                       'ConcArea30Out',
                                       'ConcArea07In',
                                       'ConcArea22In',
                                       'ConcArea23In',
                                       'ConcArea24In',
                                       'ConcArea25In',
                                       'ConcArea26In',
                                       'ConcArea27In',
                                       'ConcArea28In',
                                       'ConcArea30In',
                                       ])
    
filename2 = ('results/metricsDataFrames/bottomConcentrationAreaFiltFlatRunsCoastalInt.csv' )
dfFlat.to_csv(filename2)
    
print(filename2)
    
    
