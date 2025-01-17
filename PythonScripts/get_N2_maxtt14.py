import gsw 

from math import *

import matplotlib.pyplot as plt

import matplotlib.colors as mcolors

from MITgcmutils import rdmds

from netCDF4 import Dataset

import numpy as np

import os 

import pandas as pd

import pylab as pl

import scipy.io

import scipy as spy

import seaborn as sns

import sys

# import my modules
lib_path = os.path.abspath('../../Building_canyon/BuildCanyon/PythonModulesMITgcm') # Add absolute path to my python scripts
#lib_path = os.path.abspath('../BuildCanyon/PythonModulesMITgcm') # Add absolute path to my python scripts
sys.path.append(lib_path)

import ReadOutTools_MITgcm as rout 
import MetricsPythonTools as mpt 

sns.set()
sns.set_style('darkgrid')
sns.set_context('talk')

CGrid = '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run03/gridGlob.nc' # Smallest volume grid, closed bdy, no canyon.
phiHyd = '/ocean/kramosmu/MITgcm/TracerExperiments/BARKLEY/run02/phiHydGlob.nc'
pout = Dataset(phiHyd)
CGridOut = Dataset(CGrid)

# General input

nx = 360
ny = 360
nz = 90
nt = 19 # t dimension size 
numTr = 3 # number of tracers in run

rc = CGridOut.variables['RC']

xc = rout.getField(CGrid, 'XC') # x coords tracer cells
yc = rout.getField(CGrid, 'YC') # y coords tracer cells

drF = CGridOut.variables['drF'] # vertical distance between faces
drC = CGridOut.variables['drC'] # vertical distance between centers

hFacC = rout.getField(CGrid, 'HFacC')
MaskC = rout.getMask(CGrid, 'HFacC')
rA = rout.getField(CGrid, 'rA')

Tp = pout.variables['T']
bathy = rout.getField(CGrid, 'Depth')

# STATIONS
ys = [262,220,262,227,100,245,245,262,220]
xs = [60,60,180,180,180,160,200,300,300]
stations = ['UpSh','UpSl','CH','CM','CO','UpC','DnC','DnSh','DnSl']

#All experiments in CNT and 3D including no canyon one (run07)
expList = ['/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run02',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run03',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run04',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run09',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run10',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run11',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run12',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run14',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run15',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run16',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run17',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run18',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run19',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run20',
           '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run21',
           '/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run04',
           '/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run05',
           '/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run06',
           '/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run07']
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run07']
expNames = ['CNTDIFF_run02',
           'CNTDIFF_run03',
           'CNTDIFF_run04',
           'CNTDIFF_run09',
           'CNTDIFF_run10',
           'CNTDIFF_run11',
           'CNTDIFF_run12',
           'CNTDIFF_run14',
           'CNTDIFF_run15',
           'CNTDIFF_run16',
           'CNTDIFF_run17',
           'CNTDIFF_run18',
           'CNTDIFF_run19',
           'CNTDIFF_run20',
           'CNTDIFF_run21',
           '3DDIFF_run04',
           '3DDIFF_run05',
           '3DDIFF_run06',
           '3DDIFF_run07']
           #'CNTDIFF_run07']

RhoRef = np.squeeze(rdmds('/ocean/kramosmu/MITgcm/TracerExperiments/BARKLEY/run02/RhoRef'))

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
  
times = [0,6,10,14,18]

for exp,runs in zip(expList,expNames):
    print(runs)
    CState = ('%s/stateGlob.nc' %exp) 
        
    Temp = rout.getField(CState,'Temp')
    S = rout.getField(CState,'S')
    P = rout.getField(phiHyd,'phiHyd')
        
        
    maskExp = mpt.maskExpand(MaskC,Temp)
    TempMask=np.ma.array(Temp,mask=maskExp)   
    SMask=np.ma.array(S,mask=maskExp)   
    print(runs,'done reading')
    
    for yi,xi,sname in zip(ys,xs,stations): # station indices
        N2 = np.ma.empty((len(times),nz-2))
        ii = 0
        
        for tt in times:  
            
            #Linear eq. of state 
            rho = RhoRef*(np.ones(np.shape(RhoRef)) - alpha*(TempMask[tt,:,yi,xi]) + beta*(SMask[tt,:,yi,xi]))
            # N^2 for each station
            N2[ii,:] = (-g/RhoRef[0])*((rho[2:] - rho[:-2])/(-drC[3:]-drC[2:-1]))
            #N2[ii,:] = (-g/RhoRef[0])*((rho[2:] - rho[:-2])/(-drC[3:]-drC[2:-1]))
            
            ii = ii+1
        
        raw_data = {'drC' : drC[2:-1],'N2_tt00': N2[0,:],'N2_tt06': N2[1,:],
                    'N2_tt10': N2[2,:],'N2_tt14': N2[3,:],'N2_tt18': N2[4,:]}
        df = pd.DataFrame(raw_data, columns = ['drC', 'N2_tt00', 'N2_tt06', 'N2_tt10', 'N2_tt14', 'N2_tt18' ])
        filename1 = ('results/metricsDataFrames/N2_%s_%s.csv' % (runs,sname))
        df.to_csv(filename1)
        
    
        
# calculate average N2 between canyon head depth and shelf break during the middle of the advective phase (t=7days) 
# at dmand save as pandas dataframe. For all runs

Navg = np.zeros(len(expNames)) # 11 experiments
kk = 0

for runs in expNames:
    
    key = ['N2_tt14']
    sname = 'CM'
    filename1 = ('results/metricsDataFrames/N2_%s_%s.csv' % (runs,sname))
    print(filename1)
    df = pd.read_csv(filename1)
    col = df[key]   
    Navg[kk] = np.max(np.sqrt(col))
    kk=kk+1
        
raw_data = {'expNames':expNames,'N': Navg}
df2 = pd.DataFrame(raw_data, columns = ['expNames','N'])
filename2 = ('results/metricsDataFrames/N_t14max_%s.csv' %sname)
df2.to_csv(filename2)
        
        


