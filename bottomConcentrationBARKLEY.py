
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
    
    sumNum = np.sum(np.sum(ConcArea,axis=1),axis=1)
    sumDen = np.sum(Area)
    
    awmean = sumNum/sumDen
    return awmean

def ConcArea(Tr, hfac, ra):
    '''Tr: tracer field (nt,nz,ny,nx)
       hfac: fraction of open cell at center (nz,ny,nx)
       ra: array of cell horizontal areas (ny,nx)
       RETURNS:
       ConcArea = concentration at cell closest to bottom times its area (nt,ny,nx)
       Conc = cocnetration near bottom (nt,ny,nx)'''
    
    ConcArea = np.empty((19,360,360))
    Conc = np.empty((19,360,360))
    Area = np.empty((360,360))
    BottomInd = np.argmax(hfac[::-1,:,:]>0.0,axis=0) # start looking for first no-land cell from the bottom up.
    BottomInd = np.ones(np.shape(BottomInd))*89 - BottomInd # Get index of unreversed z axis

    
    for tt in range(19):
        for i in range(360):
            for j in range(360):
                TrBottom = Tr[tt,BottomInd[i,j],i,j]
                ConcArea[tt,i,j] = TrBottom*ra[i,j]
                Conc[tt,i,j] = TrBottom
                Area[i,j] = ra[i,j]
    

    return (ConcArea,Conc, Area)

#---------------------------------------------------------------------------------------------------------- 


NoCanyonGrid='/ocean/kramosmu/MITgcm/TracerExperiments/BARKLEY/run02/gridGlob.nc'
NoCanyonGridOut = Dataset(NoCanyonGrid)

CanyonState='/ocean/kramosmu/MITgcm/TracerExperiments/BARKLEY/run01/stateGlob.nc'
CanyonStateOut = Dataset(CanyonState)

nx = 360
ny = 360
nz = 90


hFacCNoC = rout.getField(NoCanyonGrid, 'HFacC')
MaskCNoC = rout.getMask(NoCanyonGrid, 'HFacC')
rANoC = rout.getField(NoCanyonGrid, 'rA')

z = CanyonStateOut.variables['Z']
time = CanyonStateOut.variables['T']


ptracerCanyon = '/ocean/kramosmu/MITgcm/TracerExperiments/BARKLEY/run01/ptracersGlob.nc'
                 

ptracerFlat = '/ocean/kramosmu/MITgcm/TracerExperiments/BARKLEY/run02/ptracersGlob.nc'
                 

labelsListCanyon = ['Linear',
                    'Salt',
                    'Oxygen',
                    'Nitrate',
                    'Silicate',
                    'Phosphate',
                    'Nitrous_Acid',
                    'Methane',
]

labelsListFlat = ['Linear',
                    'Salt',
                    'Oxygen',
                    'Nitrate',
                    'Silicate',
                    'Phosphate',
                    'Nitrous_Acid',
                    'Methane',
]

tracerListCanyon = ['Tr01','Tr02','Tr03',
                    'Tr04','Tr05','Tr06',
                    'Tr07','Tr08',
]

tracerListFlat = ['Tr01','Tr02','Tr03',
                  'Tr04','Tr05','Tr06',
                  'Tr07','Tr08',
]


nt = len(time)

CACanyon = np.empty((nt,len(tracerListCanyon))) # Concentration * area integrated over shelf bottom
CAFlat = np.empty((nt,len(tracerListFlat))) # Concentration * area integrated over shelf bottom


ii = 0

for tracerID in tracerListCanyon:
    
    Tr = rout.getField(ptracerCanyon, tracerID) 
    print(ptracerCanyon)
    concArea,conc,area=ConcArea(Tr, hFacCNoC, rANoC)
    CACanyon[:,ii] = a_weight_mean(concArea,area)
    
    
    ii = ii + 1

raw_data = {'time':time[:], 
            'ConcAreaLin':CACanyon[:,0],
            'ConcAreaSlt':CACanyon[:,1],
            'ConcAreaOxy':CACanyon[:,2],
            'ConcAreaNit':CACanyon[:,3],
            'ConcAreaSil':CACanyon[:,4],
            'ConcAreaPho':CACanyon[:,5],
            'ConcAreaNAc':CACanyon[:,6],
            'ConcAreaMet':CACanyon[:,7],
            }
           
           
           
           
          
df = pd.DataFrame(raw_data, columns = ['time', 
                                       'ConcAreaLin',
                                       'ConcAreaSlt',
                                       'ConcAreaOxy',
                                       'ConcAreaNit',
                                       'ConcAreaSil',
                                       'ConcAreaPho',
                                       'ConcAreaNAc',
                                       'ConcAreaMet',                                       
])
    
filename1 = ('results/metricsDataFrames/bottomConcentrationAreaCanyonRunsBarkley.csv' )
df.to_csv(filename1)
    
print(filename1)


ii = 0   
for tracerID in tracerListFlat:
    
    Tr = rout.getField(ptracerFlat, tracerID) 
    print(ptracerFlat)
    concArea,conc,area=ConcArea(Tr, hFacCNoC, rANoC)
    CAFlat[:,ii] = a_weight_mean(concArea,area)
    
    
    
    ii = ii + 1

raw_data = {'time':time[:],
            'ConcAreaFlatLin':CAFlat[:,0],
            'ConcAreaFlatSlt':CAFlat[:,1],
            'ConcAreaFlatOxy':CAFlat[:,2],
            'ConcAreaFlatNit':CAFlat[:,3],
            'ConcAreaFlatSil':CAFlat[:,4],
            'ConcAreaFlatPho':CAFlat[:,5],
            'ConcAreaFlatNAc':CAFlat[:,6],
            'ConcAreaFlatMet':CAFlat[:,7],
            }

dfFlat = pd.DataFrame(raw_data, columns = ['time', 
                                       'ConcAreaFlatLin',
                                       'ConcAreaFlatSlt',
                                       'ConcAreaFlatOxy',
                                       'ConcAreaFlatNit',
                                       'ConcAreaFlatSil',
                                       'ConcAreaFlatPho',
                                       'ConcAreaFlatNAc',
                                       'ConcAreaFlatMet',
])
    
filename2 = ('results/metricsDataFrames/bottomConcentrationAreaFlatRunsBarkley.csv' )
dfFlat.to_csv(filename2)
    
print(filename2)
    
    
