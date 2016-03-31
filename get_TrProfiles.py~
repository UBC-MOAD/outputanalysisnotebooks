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

CGrid = '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run03/gridGlob.nc' 
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
           '/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run04',
           '/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run05',
           '/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run06',
           '/ocean/kramosmu/MITgcm/TracerExperiments/3DDIFF/run07']
           #'/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run07']
TrList = [['Tr1','Tr2','Tr3'], ['Tr1','Tr2','Tr3'], ['Tr1','Tr2','Tr3'], ['Tr1','Tr2','Tr3'], ['Tr1','Tr2','Tr3'], ['Tr1'],['Tr1'],['Tr1','Tr2','Tr3'],['Tr1'],['Tr1'],['Tr1'],['Tr1']]

expNames = ['CNTDIFF_run02',
           'CNTDIFF_run03',
           'CNTDIFF_run04',
           'CNTDIFF_run09',
           'CNTDIFF_run10',
           'CNTDIFF_run11',
           'CNTDIFF_run12',
           'CNTDIFF_run14',
           '3DDIFF_run04',
           '3DDIFF_run05',
           '3DDIFF_run06',
           '3DDIFF_run07']
           #'CNTDIFF_run07']


nzlim = 30
zfin = 30
xi = 180
yi = 50
xh1=120
xh2=240
yh1=227
yh2=267
g = 9.81 # ms^-2
  
times = [0,2,4,6,8,10,14,18]

for exp,runs,ii in zip(expList,expNames,range(len(TrList))):
    
    Cptracers = ('%s/ptracersGlob.nc' %exp) 
    
    for key in TrList[ii]:
      print(key)
      Tr = rout.getField(Cptracers,key)
      maskExp = mpt.maskExpand(MaskC,Tr)
      TrMask = np.ma.array(Tr,mask=maskExp)   
    
      for yi,xi,sname in zip(ys,xs,stations): # station indices
        profiles = np.ma.empty((len(times),nz))
        Ntr = np.ma.empty((len(times),nz-2))
        
        jj = 0
        
        for tt in times:  
            
            #Linear eq. of state 
            profiles[jj,:] = TrMask[tt,:,yi,xi]
            Ntr[jj,:] = (9.81/np.mean((TrMask[0,:,yi,xi])))*(TrMask[tt,2:,yi,xi]-TrMask[tt,:-2,yi,xi])/(-drC[3:]-drC[2:-1])
            
            jj = jj+1
            
        
        raw_data = {'rc' : rc[:],'Tr_tt00': profiles[0,:],'Tr_tt02': profiles[1,:],'Tr_tt04': profiles[2,:],'Tr_tt06': profiles[3,:],
                    'Tr_tt08': profiles[4,:],'Tr_tt10': profiles[5,:],'Tr_tt14': profiles[6,:],'Tr_tt18': profiles[7,:]}
        
        raw_data2 = {'drC' : drC[2:-1],'NTr_tt00': Ntr[0,:],'NTr_tt02': Ntr[1,:],'NTr_tt04': Ntr[2,:],'NTr_tt06': Ntr[3,:],
                    'NTr_tt08': Ntr[4,:],'NTr_tt10': Ntr[5,:],'NTr_tt14': Ntr[6,:],'NTr_tt18': Ntr[7,:]}
        
        df = pd.DataFrame(raw_data, columns = ['rc', 'Tr_tt00','Tr_tt02','Tr_tt04','Tr_tt06','Tr_tt08','Tr_tt10','Tr_tt14','Tr_tt18'])
        df2 = pd.DataFrame(raw_data2, columns = ['drC', 'NTr_tt00','NTr_tt02','NTr_tt04','NTr_tt06','NTr_tt08','NTr_tt10','NTr_tt14','NTr_tt18'])
        
        filename1 = ('results/metricsDataFrames/Profile_%s_%s_%s.csv' % (key,runs,sname))
        filename2 = ('results/metricsDataFrames/N2Tr_%s_%s_%s.csv' % (key,runs,sname))
        
        df.to_csv(filename1)
        df2.to_csv(filename2)
        
        print(filename1)
        

        

