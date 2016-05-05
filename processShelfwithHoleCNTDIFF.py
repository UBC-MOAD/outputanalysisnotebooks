from math import *

from MITgcmutils import rdmds

from netCDF4 import Dataset

import numpy as np

import os 

import pandas as pd

import pylab as pl

import scipy.io

import scipy as spy

import sys

lib_path = os.path.abspath('../../Building_canyon/BuildCanyon/PythonModulesMITgcm') # Add absolute path to my python scripts
sys.path.append(lib_path)

import ReadOutTools_MITgcm as rout 

import MetricsPythonTools as mpt


### -----------------------------------------------------------------------------------------------------------------------------------


def main():
  
  expPath = sys.argv[1]
  run = sys.argv[2]
  TrName = sys.argv[3]
  
  Grid1, GridOut1, State1,StateOut1,Ptracers1, PtracersOut1 = mpt.getDatasets(expPath, run)
  
  nx = 360
  ny = 360
  nz = 90
  nt = 19 # t dimension size 

  rc = GridOut1.variables['RC']
  xc = rout.getField(Grid1, 'XC') # x coords tracer cells
  yc = rout.getField(Grid1, 'YC') # y coords tracer cells

  drF = GridOut1.variables['drF'] # vertical distance between faces
  dxG = rout.getField(Grid1,'dxG')

  MaskCan = rout.getMask(Grid1,'HFacC') 
  hFacCCan = rout.getField(Grid1,'HFacC') 
  rACan = rout.getField(Grid1,'rA') 
  drFCan=GridOut1.variables['drF']
  day = StateOut1.variables['T']
  print('Finished reading grid variables')



  Tr1 = rout.getField(Ptracers1,TrName)
  
  print('Finished reading tracer fields')
  
  
  (WatTr1, TrMassTr1,WatHTr1,TrMassHTr1) = mpt.howMuchWaterShwHole(Tr1,MaskCan,30,rACan,hFacCCan,drFCan,227,30,50,180,xh1=120,xh2=240,yh1=227,yh2=267) 
   
  
  print('Finished calculating mass on shelf')
  
    
  TracerList = ['Tr1']
  
  MassList = [TrMassTr1]
  WatList = [WatTr1]
  MassHoleList = [TrMassHTr1]
  WatHoleList = [WatHTr1]
  
  
 
  for trstr,a,b,c,d in zip(TracerList,MassList,WatList,MassHoleList,WatHoleList):
    
    raw_data = {'day':day, 'TronShelfwHole': a, 'HCWonShelfwHole': b, 'TronHole': c, 'HCWonHole': d}
    df = pd.DataFrame(raw_data, columns = ['day', 'TronShelfwHole', 'HCWonShelfwHole', 'TronHole', 'HCWonHole'])
    
    filename1 = ('results/metricsDataFrames/CNTDIFF_hole_%s%s.csv' % (run,trstr))
    df.to_csv(filename1)
    
    print(filename1)
    
    
    
  print('Done writing')
  
  
  
main()

