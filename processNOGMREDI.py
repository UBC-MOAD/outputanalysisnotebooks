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



  Tr1 = rout.getField(Ptracers1,'Tr1')
  Tr2 = rout.getField(Ptracers1,'Tr2')
  Tr3 = rout.getField(Ptracers1,'Tr3')
  
  print('Finished reading tracer fields')
  
  Tr1ini = mpt.getProfile(Tr1[0,:,:,:],50,180) #Default is to get the whole column
  Tr2ini = mpt.getProfile(Tr2[0,:,:,:],50,180) #Default is to get the whole column
  Tr3ini = mpt.getProfile(Tr3[0,:,:,:],50,180) #Default is to get the whole column
  
  (WatTr1, TrMassTr1) = mpt.howMuchWaterX(Tr1,MaskCan,30,rACan,hFacCCan,drFCan,227,30,50,180) 
  (WatTr2, TrMassTr2) = mpt.howMuchWaterX(Tr2,MaskCan,30,rACan,hFacCCan,drFCan,227,30,50,180) 
  (WatTr3, TrMassTr3) = mpt.howMuchWaterX(Tr3,MaskCan,30,rACan,hFacCCan,drFCan,227,30,50,180) 
  print('Finished calculating mass on shelf')
  
  (WatTr1CV, MassTr1CV) = mpt.howMuchWaterCV(Tr1,MaskCan,30,rACan,hFacCCan,drFCan,227,30,50,180,49,309)
  (WatTr2CV, MassTr2CV) = mpt.howMuchWaterCV(Tr2,MaskCan,30,rACan,hFacCCan,drFCan,227,30,50,180,49,309)
  (WatTr3CV, MassTr3CV) = mpt.howMuchWaterCV(Tr3,MaskCan,30,rACan,hFacCCan,drFCan,227,30,50,180,49,309)
  print('Finished calculating mass in control volume')
  
  TracerList = ['Tr1','Tr2','Tr3']
  
  IniList = [Tr1ini,Tr2ini,Tr3ini]
  MassList = [TrMassTr1,TrMassTr2,TrMassTr3]
  WatList = [WatTr1,WatTr2,WatTr3]
  MassCVList = [MassTr1CV,MassTr2CV,MassTr3CV]
  WatTr1CV = [WatTr1CV,WatTr2CV,WatTr3CV]
  
  day = [0., 0.5, 1., 1.5, 2., 2.5, 3., 3.5, 4., 4.5, 5., 5.5,  6., 6.5,  7., 7.5,  8., 8.5,  9.]
 
  for trstr,a,b,c,d,e, in zip(TracerList,IniList,MassList,WatList,MassCVList,WatTr1CV):
    
    raw_data = {'day':day, 'TronShelf': b, 'HCWonShelf': c, 'TronCV': d, 'HCWonCV': e}
    df = pd.DataFrame(raw_data, columns = ['day', 'TronShelf', 'HCWonShelf', 'TronCV', 'HCWonCV'])
    
    filename1 = ('results/metricsDataFrames/NOREDI%s%s.csv' % (run,trstr))
    df.to_csv(filename1)
    
    print(filename1)
  
    raw_data_ini = {'depthsRC':rc ,'IniProfile': a}
    df2 = pd.DataFrame(raw_data_ini, columns = ['depthsRC', 'IniProfile'])
    
    filename2 = ('results/metricsDataFrames/NOREDI%sini%s.csv' % (run,trstr))
    df2.to_csv(filename2)
    
    print(filename2)
  
  print('Done writing')
  
  
  
main()

