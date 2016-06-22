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
    
    sumNum = np.sum(np.sum(ConcArea,axis=1),axis=1)
    sumDen = np.sum(Area)
    
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


NoCanyonGrid='/ocean/kramosmu/MITgcm/TracerExperiments/BARKLEY/run02/gridGlob.nc'
NoCanyonGridOut = Dataset(NoCanyonGrid)

CanyonGrid='/ocean/kramosmu/MITgcm/TracerExperiments/BARKLEY/run01/gridGlob.nc'
CanyonGridOut = Dataset(CanyonGrid)

CanyonState='/ocean/kramosmu/MITgcm/TracerExperiments/BARKLEY/run01/stateGlob.nc'
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

CACanyonOut = np.empty((nt,len(tracerListCanyon))) # Concentration * area integrated over shelf bottom
CACanyonIn = np.empty((nt,len(tracerListCanyon))) # Concentration * area integrated over shelf bottom

CAFlatOut = np.empty((nt,len(tracerListFlat))) # Concentration * area integrated over shelf bottom
CAFlatIn = np.empty((nt,len(tracerListFlat))) # Concentration * area integrated over shelf bottom


ii = 0

for tracerID in tracerListCanyon:
    
    Tr = rout.getField(ptracerCanyon, tracerID) 
    print(ptracerCanyon)
    concArea,conc,area=ConcArea(Tr, hFacC, rA, bathy)
    CACanyonOut[:,ii] = a_weight_mean(concArea[:,:267,:],area[:267,:])
    CACanyonIn[:,ii] = a_weight_mean(concArea[:,267:,:],area[267:,:])
    
    
    ii = ii + 1

raw_data = {'time':time[:], 
            'ConcAreaLinOut':CACanyonOut[:,0],
            'ConcAreaSltOut':CACanyonOut[:,1],
            'ConcAreaOxyOut':CACanyonOut[:,2],
            'ConcAreaNitOut':CACanyonOut[:,3],
            'ConcAreaSilOut':CACanyonOut[:,4],
            'ConcAreaPhoOut':CACanyonOut[:,5],
            'ConcAreaNAcOut':CACanyonOut[:,6],
            'ConcAreaMetOut':CACanyonOut[:,7],
            'ConcAreaLinIn':CACanyonIn[:,0],
            'ConcAreaSltIn':CACanyonIn[:,1],
            'ConcAreaOxyIn':CACanyonIn[:,2],
            'ConcAreaNitIn':CACanyonIn[:,3],
            'ConcAreaSilIn':CACanyonIn[:,4],
            'ConcAreaPhoIn':CACanyonIn[:,5],
            'ConcAreaNAcIn':CACanyonIn[:,6],
            'ConcAreaMetIn':CACanyonIn[:,7], 
           }
           
           
           
           
          
df = pd.DataFrame(raw_data, columns = ['time', 
                                       'ConcAreaLinOut',
                                       'ConcAreaSltOut',
                                       'ConcAreaOxyOut',
                                       'ConcAreaNitOut',
                                       'ConcAreaSilOut',
                                       'ConcAreaPhoOut',
                                       'ConcAreaNAcOut',
                                       'ConcAreaMetOut', 
                                       'ConcAreaLinIn',
                                       'ConcAreaSltIn',
                                       'ConcAreaOxyIn',
                                       'ConcAreaNitIn',
                                       'ConcAreaSilIn',
                                       'ConcAreaPhoIn',
                                       'ConcAreaNAcIn',
                                       'ConcAreaMetIn',
])
    
filename1 = ('results/metricsDataFrames/bottomConcentrationAreaFiltCanyonRunsBarkleyCoastalInt.csv' )
df.to_csv(filename1)
    
print(filename1)


ii = 0   
for tracerID in tracerListFlat:
    
    Tr = rout.getField(ptracerFlat, tracerID) 
    print(ptracerFlat)
    concArea,conc,area=ConcArea(Tr, hFacCNoC, rANoC, bathyNoC)
    CAFlatOut[:,ii] = a_weight_mean(concArea[:,:267,:],area[:267,:])
    CAFlatIn[:,ii] = a_weight_mean(concArea[:,267:,:],area[267:,:])
    
    
    
    ii = ii + 1

raw_data = {'time':time[:],
            'ConcAreaFlatLinOut':CAFlatOut[:,0],
            'ConcAreaFlatSltOut':CAFlatOut[:,1],
            'ConcAreaFlatOxyOut':CAFlatOut[:,2],
            'ConcAreaFlatNitOut':CAFlatOut[:,3],
            'ConcAreaFlatSilOut':CAFlatOut[:,4],
            'ConcAreaFlatPhoOut':CAFlatOut[:,5],
            'ConcAreaFlatNAcOut':CAFlatOut[:,6],
            'ConcAreaFlatMetOut':CAFlatOut[:,7],
            'ConcAreaFlatLinIn':CAFlatIn[:,0],
            'ConcAreaFlatSltIn':CAFlatIn[:,1],
            'ConcAreaFlatOxyIn':CAFlatIn[:,2],
            'ConcAreaFlatNitIn':CAFlatIn[:,3],
            'ConcAreaFlatSilIn':CAFlatIn[:,4],
            'ConcAreaFlatPhoIn':CAFlatIn[:,5],
            'ConcAreaFlatNAcIn':CAFlatIn[:,6],
            'ConcAreaFlatMetIn':CAFlatIn[:,7],
            }

dfFlat = pd.DataFrame(raw_data, columns = ['time', 
                                       'ConcAreaFlatLinOut',
                                       'ConcAreaFlatSltOut',
                                       'ConcAreaFlatOxyOut',
                                       'ConcAreaFlatNitOut',
                                       'ConcAreaFlatSilOut',
                                       'ConcAreaFlatPhoOut',
                                       'ConcAreaFlatNAcOut',
                                       'ConcAreaFlatMetOut',
                                       'ConcAreaFlatLinIn',
                                       'ConcAreaFlatSltIn',
                                       'ConcAreaFlatOxyIn',
                                       'ConcAreaFlatNitIn',
                                       'ConcAreaFlatSilIn',
                                       'ConcAreaFlatPhoIn',
                                       'ConcAreaFlatNAcIn',
                                       'ConcAreaFlatMetIn',
])
    
filename2 = ('results/metricsDataFrames/bottomConcentrationAreaFiltFlatRunsBarkleyCoastalInt.csv' )
dfFlat.to_csv(filename2)
    
print(filename2)
    
    