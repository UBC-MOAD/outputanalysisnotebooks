
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


# General input

nx = 360
ny = 360
nz = 90
nt = 19 # t dimension size 

stations = ['UpSh','UpSl','CH','CM','CO','UpC','DnC','DnSh','DnSl']


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
TrListExp = ['Run02Tr1','Run02Tr2','Run02Tr3', 'Run03Tr1','Run03Tr2','Run03Tr3', 'Run04Tr1','Run04Tr2','Run04Tr3',
         'Run09Tr1','Run09Tr2','Run09Tr3', 'Run10Tr1','Run10Tr2','Run10Tr3', 'Run11Tr1','Run12Tr1','Run14Tr1','Run14Tr2','Run14Tr3',
         '3DRun04Tr1','3DRun05Tr1','3DRun06Tr1','3DRun07Tr1']

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


Navg = np.zeros(24) # all tracers up to March 22, 2016
kk = 0

for exp,runs,ii in zip(expList,expNames,range(len(TrList))):
    
    
    for trname in TrList[ii]:
    
      key = ['NTr_tt14']
      sname = 'DnC'
      filename1 = ('results/metricsDataFrames/N2Tr_%s_%s_%s.csv' % (trname,runs,sname))
      print(filename1)
      df = pd.read_csv(filename1)
      col = df[key]   
      Navg[kk] = np.max(np.sqrt(-col))
      kk=kk+1
        
raw_data = {'tracerList':TrListExp,'N': Navg}
df2 = pd.DataFrame(raw_data, columns = ['tracerList','N'])
filename2 = ('results/metricsDataFrames/Ntr_t14max_%s.csv' %sname)
df2.to_csv(filename2)
   