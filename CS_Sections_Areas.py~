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
  dxF = rout.getField(Grid1,'dxF')
  dyF = rout.getField(Grid1,'dyF')

  MaskCan = rout.getMask(Grid1,'HFacC') 
  hFacCCan = rout.getField(Grid1,'HFacC') 
  rACan = rout.getField(Grid1,'rA') 
  drFCan=GridOut1.variables['drF']
  print('Finished reading grid variables')

  #Transect definitions (indices x,y,z,t)
  
  CS1 = [0,40,227,227,0,29]
  CS2 = [40,120,227,227,0,29]
  CS3 = [120,240,267,267,0,29]
  CS3sb = [120,240,227,227,0,29 ]
  CS4 = [240,320,227,227,0,29 ]
  CS5 = [320,359,227,227,0,29 ]
  AS1 = [120,120,227,267,0,29 ]
  AS2 = [240,240,227,267,0,29 ]
  LID1 = [120,180,227,267,29,29 ]
  LID2 = [180,240,227,267,29,29 ]
  
  
    
  #Get slices
  V_CS1a = mpt.slice_area( dxF,drFCan,rACan,hFacCCan,CS1[0],CS1[1],CS1[2],CS1[3],CS1[4],CS1[5])
  V_CS2a = mpt.slice_area(  dxF,drFCan,rACan,hFacCCan,CS2[0],CS2[1],CS2[2],CS2[3],CS2[4],CS2[5])
  V_CS3a = mpt.slice_area(  dxF,drFCan,rACan,hFacCCan,CS3[0],CS3[1],CS3[2],CS3[3],CS3[4],CS3[5])
  V_CS4a = mpt.slice_area(  dxF,drFCan,rACan,hFacCCan,CS4[0],CS4[1],CS4[2],CS4[3],CS4[4],CS4[5])
  V_CS5a = mpt.slice_area(  dxF,drFCan,rACan,hFacCCan,CS5[0],CS5[1],CS5[2],CS5[3],CS5[4],CS5[5])
  V_CS3sba = mpt.slice_area(  dxF,drFCan,rACan,hFacCCan,CS3sb[0],CS3sb[1],CS3sb[2],CS3sb[3],CS3sb[4],CS3sb[5])
  U_AS1a = mpt.slice_area(  dyF,drFCan,rACan,hFacCCan,AS1[0],AS1[1],AS1[2],AS1[3],AS1[4],AS1[5])
  U_AS2a = mpt.slice_area(  dyF,drFCan,rACan,hFacCCan,AS2[0],AS2[1],AS2[2],AS2[3],AS2[4],AS2[5])
  W_LID1a = mpt.slice_area(  dxF,drFCan,rACan,hFacCCan,LID1[0],LID1[1],LID1[2],LID1[3],LID1[4],LID1[5])
  W_LID2a = mpt.slice_area(  dxF,drFCan,rACan,hFacCCan,LID2[0],LID2[1],LID2[2],LID2[3],LID2[4],LID2[5])
  
  #add up
  V_CS1 = np.sum(V_CS1a)
  V_CS2 =  np.sum(V_CS2a)
  V_CS3 =  np.sum(V_CS3a )
  V_CS4 =  np.sum(V_CS4a )
  V_CS5 =  np.sum(V_CS5a )
  V_CS3sb =  np.sum(V_CS3sba )
  U_AS1 =  np.sum(U_AS1a )
  U_AS2 =  np.sum(U_AS2a )
  W_LID1 =  np.sum(W_LID1a)
  W_LID2 =  np.sum(W_LID2a)
  
  yin = 227
  zfin = 30
  
  [VolShNoHole,VolHole] = mpt.Volume_Sh_and_Hole(MaskCan,rACan,hFacCCan,drFCan,yin,zfin,xh1=120,xh2=240,yh1=227,yh2=267)
  
  raw_data = {'CS1area': V_CS1, 'CS2area': V_CS2, 'CS3area': V_CS3, 'CS3sbarea': V_CS3sb, 'CS4area': V_CS4, 'CS5area': V_CS5, 'AS1area':U_AS1, 'AS2area': U_AS2,'LID1area': W_LID1, 'LID2area': W_LID2,'VolHole': VolHole,'VolShNoHole':VolShNoHole}
  
  df = pd.DataFrame(raw_data, columns = ['CS1area', 'CS2area', 'CS3area', 'CS3sbarea', 'CS4area', 'CS5area', 'AS1area', 'AS2area', 'LID1area', 'LID2area','VolHole','VolShNoHole'], index=[0])
    
  filename1 = ('results/metricsDataFrames/Canyon_AreasVolumes.csv')
  df.to_csv(filename1)
   
  print(filename1)
  
    
  
  print('Done')
  
  
  
main()

