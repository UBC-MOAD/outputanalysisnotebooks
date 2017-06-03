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
  print('Finished reading grid variables')

  #Transect definitions (indices x,y,z,t)
  
  CS1 = [0,40,227,227,0,29,0,18]
  CS2 = [40,120,227,227,0,29,0,18]
  CS3 = [120,240,267,267,0,29,0,18]
  CS3sb = [120,240,227,227,0,29,0,18]
  CS4 = [240,320,227,227,0,29,0,18]
  CS5 = [320,359,227,227,0,29,0,18]
  AS1 = [120,120,227,267,0,29,0,18]
  AS2 = [240,240,227,267,0,29,0,18]
  LID1 = [120,180,227,267,29,29,0,18]
  LID2 = [180,240,227,267,29,29,0,18]
  
  
  day = [0.0,0.5, 1., 1.5, 2., 2.5, 3., 3.5, 4., 4.5, 5., 5.5,  6., 6.5,  7., 7.5,  8., 8.5] 
  
  velfile = State1
  
  keyw = 'W'
  keyv = 'V' 
  keyu = 'U' 
  
  W = rout.getField(velfile,keyw)
  UT = rout.getField(velfile,keyu)
  VT = rout.getField(velfile,keyv)
  U,V = rout.unstagger(UT,VT)
    
  

  
  #Get slices
  V_CS1a = mpt.slice_TRAC(V,CS1[0],CS1[1],CS1[2],CS1[3],CS1[4],CS1[5],CS1[6],CS1[7])
  V_CS2a = mpt.slice_TRAC(V,CS2[0],CS2[1],CS2[2],CS2[3],CS2[4],CS2[5],CS2[6],CS2[7])
  V_CS3a = mpt.slice_TRAC(V,CS3[0],CS3[1],CS3[2],CS3[3],CS3[4],CS3[5],CS3[6],CS3[7])
  V_CS4a = mpt.slice_TRAC(V,CS4[0],CS4[1],CS4[2],CS4[3],CS4[4],CS4[5],CS4[6],CS4[7])
  V_CS5a = mpt.slice_TRAC(V,CS5[0],CS5[1],CS5[2],CS5[3],CS5[4],CS5[5],CS5[6],CS5[7])
  V_CS3sba = mpt.slice_TRAC(V,CS3sb[0],CS3sb[1],CS3sb[2],CS3sb[3],CS3sb[4],CS3sb[5],CS3sb[6],CS3sb[7])
  U_AS1a = mpt.slice_TRAC(U,AS1[0],AS1[1],AS1[2],AS1[3],AS1[4],AS1[5],AS1[6],AS1[7])
  U_AS2a = mpt.slice_TRAC(U,AS2[0],AS2[1],AS2[2],AS2[3],AS2[4],AS2[5],AS2[6],AS2[7])
  W_LID1a = mpt.slice_TRAC(W,LID1[0],LID1[1],LID1[2],LID1[3],LID1[4],LID1[5],LID1[6],LID1[7])
  W_LID2a = mpt.slice_TRAC(W,LID2[0],LID2[1],LID2[2],LID2[3],LID2[4],LID2[5],LID2[6],LID2[7])
  
  #add up
  V_CS1 = np.sum(np.sum(V_CS1a,axis=1),axis=1)
  V_CS2 = np.sum(np.sum(V_CS2a,axis=1),axis=1)
  V_CS3 = np.sum(np.sum(V_CS3a,axis=1),axis=1)
  V_CS4 = np.sum(np.sum(V_CS4a,axis=1),axis=1)
  V_CS5 = np.sum(np.sum(V_CS5a,axis=1),axis=1)
  V_CS3sb = np.sum(np.sum(V_CS3sba,axis=1),axis=1)
  U_AS1 = np.sum(np.sum(U_AS1a,axis=1),axis=1)
  U_AS2 = np.sum(np.sum(U_AS2a,axis=1),axis=1)
  W_LID1 = np.sum(np.sum(W_LID1a,axis=2),axis=1)
  W_LID2 = np.sum(np.sum(W_LID2a,axis=2),axis=1)
  
  print(np.shape(day), np.shape(W_LID1))
   
  raw_data = {'day':day, 'CS1': V_CS1, 'CS2': V_CS2, 'CS3': V_CS3, 'CS3sb': V_CS3sb, 'CS4': V_CS4, 'CS5': V_CS5, 'AS1':U_AS1, 'AS2': U_AS2, 'LID1': W_LID1, 'LID2': W_LID2}
  df = pd.DataFrame(raw_data, columns = ['day', 'CS1', 'CS2', 'CS3', 'CS3sb', 'CS4', 'CS5', 'AS1', 'AS2', 'LID1', 'LID2'])
    
  filename1 = ('results/metricsDataFrames/NOGMREDI_WaterCSTRANS_%s.csv' % run)
  df.to_csv(filename1)
    
  print(filename1)
  
    
  
  print('Done water transport')
  
  
  
main()

