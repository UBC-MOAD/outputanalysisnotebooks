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
  runNoC = sys.argv[3]

  Grid1, GridOut1, State1,StateOut1,Ptracers1, PtracersOut1 = mpt.getDatasets(expPath, run)
  GridNoC, GridOutNoC, StateNoC,StateOutNoC,PtracersNoC, PtracersOutNoC = mpt.getDatasets(expPath, runNoC)

  nx = 360
  ny = 360
  nz = 90
  nt = 19 # t dimension size

  rc = GridOut1.variables['RC']
  xc = rout.getField(Grid1, 'XC') # x coords tracer cells
  yc = rout.getField(Grid1, 'YC') # y coords tracer cells

  drF = GridOut1.variables['drF'] # vertical distance between faces
  dxG = rout.getField(Grid1,'dxG')

  MaskNoC = rout.getMask(GridNoC,'HFacC')
  hFacCNoC = rout.getField(GridNoC,'HFacC')
  rACNoC = rout.getField(GridNoC,'rA')
  drFCan=GridOut1.variables['drF']
  print('Finished reading grid variables')



  Tr1 = rout.getField(Ptracers1,'Tr1')
  Tr2 = rout.getField(Ptracers1,'Tr2')
  Tr3 = rout.getField(Ptracers1,'Tr3')
  print('Finished reading tracer fields')



  (WatTr1, TrMassTr1,WatHTr1,TrMassHTr1) = mpt.howMuchWaterShwHole(Tr1,MaskNoC,30,rACNoC,hFacCNoC,drFCan,227,30,180,50, xh1=120,xh2=240,yh1=227,yh2=267)
  (WatTr2, TrMassTr2,WatHTr2,TrMassHTr2) = mpt.howMuchWaterShwHole(Tr2,MaskNoC,30,rACNoC,hFacCNoC,drFCan,227,30,180,50, xh1=120,xh2=240,yh1=227,yh2=267)
  (WatTr3, TrMassTr3,WatHTr3,TrMassHTr3) = mpt.howMuchWaterShwHole(Tr3,MaskNoC,30,rACNoC,hFacCNoC,drFCan,227,30,180,50, xh1=120,xh2=240,yh1=227,yh2=267)
  print('Finished calculating mass on shelf')


  TracerList = ['Tr1','Tr2','Tr3','Tr4','Tr5','Tr6','Tr7','Tr8']

  MassList = [TrMassTr1,TrMassTr2,TrMassTr3]
  WatList = [WatTr1,WatTr2,WatTr3]
  MassHoleList = [TrMassHTr1,TrMassHTr2,TrMassHTr3]
  WatHoleList = [WatHTr1,WatHTr2,WatHTr3]

  day = [0., 0.5, 1., 1.5, 2., 2.5, 3., 3.5, 4., 4.5, 5., 5.5,  6., 6.5,  7., 7.5,  8., 8.5,  9.]

  for trstr,a,b,c,d in zip(TracerList,MassList,WatList,MassHoleList,WatHoleList):

    raw_data = {'day':day, 'TronShelfwHole': a, 'HCWonShelfwHole': b, 'TronHole': c, 'HCWonHole': d}
    df = pd.DataFrame(raw_data, columns = ['day', 'TronShelfwHole', 'HCWonShelfwHole', 'TronHole', 'HCWonHole'])

    filename1 = ('results/metricsDataFrames/CNT_hole_NoCMask_%s%s.csv' % (run,trstr))
    df.to_csv(filename1)

    print(filename1)



  print('Done writing')



main()
