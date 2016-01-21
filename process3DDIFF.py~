from math import *

from MITgcmutils import rdmds

from netCDF4 import Dataset

import numpy as np

import os 

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
  print('Finished reading tracer fields')
  
  
  Tr1ini = mpt.getProfile(Tr1[0,:,:,:],50,180) #Default is to get the whole column
  
  
  (WatTr1, TrMassTr1) = mpt.howMuchWaterX(Tr1,MaskCan,30,rACan,hFacCCan,drFCan,227,30,50,180) 
  print('Finished calculating mass on shlelf')
  
  (WatTr1CV, MassTr1CV) = mpt.howMuchWaterCV(Tr1,MaskCan,30,rACan,hFacCCan,drFCan,227,30,50,180,49,309)
  print('Finished calculating mass in control volume')
  
  filename1 = ('results/iniProfiles/3DDIFF%siniTr1' % run)
  mpt.dumpFiles(filename1,Tr1ini)
  
  filename2 = ('results/massShelf/3DDIFF%smassTr1' % run)
  mpt.dumpFiles(filename2,TrMassTr1)
  
  filename3 = ('results/volumeHCWShelf/3DDIFF%swat30Tr1' % run) 
  mpt.dumpFiles(filename3,WatTr1)
  
  filename4 = ('results/massCV/3DDIFF%smassTr1' % run)
  mpt.dumpFiles(filename4,MassTr1CV)
  
  filename5 =  ('results/volumeHCWCV/3DDIFF%swat30Tr1' % run)
  mpt.dumpFiles(filename5,WatTr1CV)
 
  print('Done writing')
  
  
  
main()

