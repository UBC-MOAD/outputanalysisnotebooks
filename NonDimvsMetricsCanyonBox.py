### Non dimensional parameters vs.  metrics



from math import *

import matplotlib.pyplot as plt

import matplotlib.colors as mcolors

from netCDF4 import Dataset

import numpy as np

import os 

import pandas as pd

import pylab as pl

import scipy.io

import scipy as spy

import seaborn as sns

import sys

lib_path = os.path.abspath('../../Building_canyon/BuildCanyon/PythonModulesMITgcm') # Add absolute path to my python scripts
#lib_path = os.path.abspath('../BuildCanyon/PythonModulesMITgcm') # Add absolute path to my python scripts

sys.path.append(lib_path)

import ReadOutTools_MITgcm as rout 
import MetricsPythonTools as mpt




#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_metrics(exp, run, TrNum, key):
    '''Get column from a tracer metrics pandas dataframe using the key name, run (01, 02, etc) and experiment 
    abreviated name (BAR, CNTDIFF, 3DDIFF, NOGMREDI). All input variables are strings. Returns the desired column from the dataframe'''
    df = pd.read_csv(('results/metricsDataFrames/%srun%sTr%s.csv' %(exp,run,TrNum)))
    col = df[key]
    return col
    
def get_water(exp, run, key):
    '''Get column from a tracer metrics pandas dataframe using the key name, run (01, 02, etc) and experiment 
    abreviated name (BAR, CNTDIFF, 3DDIFF, NOGMREDI). All input variables are strings. Returns the desired column from the dataframe'''
    df = pd.read_csv(('results/metricsDataFrames/%srun%s.csv' %(exp,run)))
    col = df[key]
    return col

def get_areas(file, key):
    '''Get column from a tracer metrics pandas dataframe using the key name, run (01, 02, etc) and experiment 
    abreviated name (BAR, CNTDIFF, 3DDIFF, NOGMREDI). All input variables are strings. Returns the desired column from the dataframe'''
    df = pd.read_csv(file)
    col = df[key]
    return col
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

sns.set()
sns.set_style('darkgrid')
sns.set_context('poster')

#Exp
#CGrid = '/Users/Karina/Research/PhD/Tracers/TemporaryData/BARKLEY/run01/gridGlob.nc' # Smallest volume grid, closed bdy, no canyon.
CGrid = '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run03/gridGlob.nc' # Smallest volume grid, closed bdy, no canyon.
CGridOut = Dataset(CGrid)

# General input

nx = 360
ny = 360
nz = 90
nt = 19 # t dimension size 
numTr = 22 # number of tracers in total (CNT =22, 3D = 4, total = 19)

rc = CGridOut.variables['RC']

xc = rout.getField(CGrid, 'XC') # x coords tracer cells
yc = rout.getField(CGrid, 'YC') # y coords tracer cells

drF = CGridOut.variables['drF'] # vertical distance between faces
drC = CGridOut.variables['drC'] # vertical distance between centers

labels = ['$K_v=10^{-7}$(out), $10^{-3}$(in), $K_i=1 m^2s^{-1}$','Kv=1E-7(out), 1E-4(in), Ki=1','Kv=1E-5(out), 1E-3(in), Ki=1',
          'Kv=1E-5(out), 1E-4(in), Ki=1','Kv=1E-5, Ki=1','Kv=1E-4, Ki=1','Kv=1E-3, Ki=1','Kv=3.8E-5, Ki=10',
          'Kv=2.8E-5, Ki=10','Kv=1.3E-5, Ki=10','Kv_noc=1E-5, Ki=1','Kv_noc=1E-4, Ki=1','Kv_noc=1E-3, Ki=1',
          'Kv=1E-5, Ki=10','Kv=1E-4, Ki=10','Kv=1E-3, Ki=10','Kv=1E-5, Ki=0.1','Kv=1E-4, Ki=0.1',
          'Kv=1E-3, Ki=0.1','Kv=3.8E-5, Ki=1','Kv=2.8E-5, Ki=1','Kv=1.3E-5, Ki=1']

wlabels = ['run04 - 3D','run05 - 3D','run06 - 3D','run07 - 3D','run02 - CNT','run03 - CNT','run04 - CNT',
           'run07 - CNT','run09 - CNT','run10 - CNT']


times = np.arange(0,nt,1)

# LOAD AREAS
CS1A = get_areas('results/metricsDataFrames/Canyon_AreasVolumes.csv', 'CS1area' )
CS2A = get_areas('results/metricsDataFrames/Canyon_AreasVolumes.csv', 'CS2area' )
CS3A = get_areas('results/metricsDataFrames/Canyon_AreasVolumes.csv', 'CS3area' )
CS3sbA = get_areas('results/metricsDataFrames/Canyon_AreasVolumes.csv', 'CS3sbarea' )
CS4A = get_areas('results/metricsDataFrames/Canyon_AreasVolumes.csv', 'CS4area' )
CS5A = get_areas('results/metricsDataFrames/Canyon_AreasVolumes.csv', 'CS5area' )
AS1A = get_areas('results/metricsDataFrames/Canyon_AreasVolumes.csv', 'AS1area' )
AS2A = get_areas('results/metricsDataFrames/Canyon_AreasVolumes.csv', 'AS2area' )
LID1A = get_areas('results/metricsDataFrames/Canyon_AreasVolumes.csv', 'LID1area' )
LID2A = get_areas('results/metricsDataFrames/Canyon_AreasVolumes.csv', 'LID2area' )
VolHole = get_areas('results/metricsDataFrames/Canyon_AreasVolumes.csv', 'VolHole'  )
VoleShwoHole = get_areas('results/metricsDataFrames/Canyon_AreasVolumes.csv', 'VolShNoHole' )


tracers_3D = ['04','05','06','07'] #run number because there's only 1 tr per run
tracers_CNT03 = ['1','2','3'] # tracer number , constant runs
tracers_CNT09 = ['1','2','3'] # tracer number , average diffusivity runs
tracers_CNT07 = ['1','2','3'] # tracer number , no canyon case
tracers_CNT02 = ['1','2','3'] # tracer number , Kiso=0.1
tracers_CNT04 = ['1','2','3'] # tracer number , Kiso=10
tracers_CNT10 = ['1','2','3'] # tracer number , Kiso=1

# LOAD TRACER ON SHELF DATA

TrOnSh = np.zeros((nt,numTr)) 
HWC = np.zeros((nt,numTr)) 

kk = 0

fields = ['TronShelfwHole', 'HCWonShelfwHole','TronHole','HCWonHole']

for ii in tracers_3D:
    
    TrOnShwHole = get_metrics('3DDIFF_hole_', ii, '1', fields[0] )
    TrOnHole = get_metrics('3DDIFF_hole_', ii, '1', fields[2] )
    
    TrOnSh[:,kk] =  TrOnHole
    
    HWCsh = get_metrics('3DDIFF_hole_', ii, '1', fields[1] )
    HWChole = get_metrics('3DDIFF_hole_', ii, '1', fields[1] )
    
    HWC[:,kk] =  HWChole  
    
    kk=kk+1

for ii in tracers_CNT03:
    
    TrOnShwHole = get_metrics('CNTDIFF_hole_',  '03',ii, fields[0] )
    TrOnHole = get_metrics('CNTDIFF_hole_', '03', ii, fields[2] )
    
    TrOnSh[:,kk] = TrOnHole
    
    HWCsh = get_metrics('CNTDIFF_hole_',  '03', ii,fields[1] )
    HWChole = get_metrics('CNTDIFF_hole_',  '03',ii,  fields[1] )
    
    HWC[:,kk] =  HWChole  
    
    kk=kk+1

for ii in tracers_CNT09:
    
    TrOnShwHole = get_metrics('CNTDIFF_hole_',  '09',ii, fields[0] )
    TrOnHole = get_metrics('CNTDIFF_hole_','09',ii, fields[2] )
    
    TrOnSh[:,kk] = TrOnHole
    
    HWCsh = get_metrics('CNTDIFF_hole_',  '09',ii, fields[1] )
    HWChole = get_metrics('CNTDIFF_hole_',  '09',ii, fields[1] )
    
    HWC[:,kk] =  HWChole  
    
    kk=kk+1

for ii in tracers_CNT07:
    
    
    TrSh = get_metrics('CNTDIFF_hole_', '07', ii, fields[0] )
    TrHole= get_metrics('CNTDIFF_hole_', '07', ii, fields[2] )
    
    HWCSh = get_metrics('CNTDIFF_hole_', '07', ii, fields[1] )
    HWCHole = get_metrics('CNTDIFF_hole_', '07', ii, fields[3] )
    
    TrOnSh[:,kk] =  TrHole 
    HWC[:,kk] =  HWCHole
    
    kk=kk+1

for ii in tracers_CNT02:
    
    TrOnShwHole = get_metrics('CNTDIFF_hole_',  '02',ii, fields[0] )
    TrOnHole = get_metrics('CNTDIFF_hole_',  '02',ii, fields[2] )
    
    TrOnSh[:,kk] =  TrOnHole
    
    HWCsh = get_metrics('CNTDIFF_hole_', '02',ii, fields[1] )
    HWChole = get_metrics('CNTDIFF_hole_',  '02', ii,fields[1] )
    HWC[:,kk] =  HWChole  
    
    kk=kk+1

for ii in tracers_CNT04:
    
    TrOnShwHole = get_metrics('CNTDIFF_hole_',  '04',ii, fields[0] )
    TrOnHole = get_metrics('CNTDIFF_hole_', '04',ii, fields[2] )
    
    TrOnSh[:,kk] =  TrOnHole
    
    HWCsh = get_metrics('CNTDIFF_hole_',  '04',ii, fields[1] )
    HWChole = get_metrics('CNTDIFF_hole_',  '04',ii, fields[1] )
    HWC[:,kk] =  HWChole  
    
    kk=kk+1

for ii in tracers_CNT10:
    
    TrOnShwHole = get_metrics('CNTDIFF_hole_', '10',ii, fields[0] )
    TrOnHole = get_metrics('CNTDIFF_hole_', '10',ii, fields[2] )
    
    TrOnSh[:,kk] = TrOnHole
    
    HWCsh = get_metrics('CNTDIFF_hole_', '10',ii, fields[1] )
    HWChole = get_metrics('CNTDIFF_hole_',  '10',ii, fields[1] )
    
    HWC[:,kk] =  HWChole  
    
    
    kk=kk+1

# LOAD TRANSPORTS

CS1 = np.zeros((nt-1,numTr)) 
CS2 = np.zeros((nt-1,numTr)) 
CS3 = np.zeros((nt-1,numTr)) 
CS4 = np.zeros((nt-1,numTr)) 
CS5 = np.zeros((nt-1,numTr)) 
CS3sb = np.zeros((nt-1,numTr)) 
AS1 = np.zeros((nt-1,numTr)) 
AS2 = np.zeros((nt-1,numTr)) 
LID1 = np.zeros((nt-1,numTr)) 
LID2 = np.zeros((nt-1,numTr)) 

CS1a = np.zeros((nt-1,numTr)) 
CS2a = np.zeros((nt-1,numTr)) 
CS3a = np.zeros((nt-1,numTr)) 
CS4a = np.zeros((nt-1,numTr)) 
CS5a = np.zeros((nt-1,numTr)) 
CS3sba = np.zeros((nt-1,numTr)) 
AS1a = np.zeros((nt-1,numTr)) 
AS2a = np.zeros((nt-1,numTr)) 
LID1a = np.zeros((nt-1,numTr)) 
LID2a = np.zeros((nt-1,numTr)) 

CS1d = np.zeros((nt-1,numTr)) 
CS2d = np.zeros((nt-1,numTr)) 
CS3d = np.zeros((nt-1,numTr)) 
CS4d = np.zeros((nt-1,numTr)) 
CS5d = np.zeros((nt-1,numTr)) 
CS3sbd = np.zeros((nt-1,numTr)) 
AS1d = np.zeros((nt-1,numTr)) 
AS2d = np.zeros((nt-1,numTr)) 
LID1d = np.zeros((nt-1,numTr)) 
LID2d = np.zeros((nt-1,numTr)) 


kk = 0

fields = ['CS1','CS2','CS3','CS3sb','CS4','CS5','AS1' ,'AS2','LID1' ,'LID2']
fieldsDiff = ['CS1','CS2','CS3','CS3sb','CS4','CS5','AS1' ,'AS2','LID1' ,'LID2','LID1i' ,'LID2i']

for ii in tracers_3D:
    
    CS1a[:,kk] = get_metrics('3DDIFF_CS_ADVFLUX_', ii, '1', fields[0] )
    CS2a[:,kk] = get_metrics('3DDIFF_CS_ADVFLUX_', ii, '1', fields[1] )
    CS3a[:,kk] = get_metrics('3DDIFF_CS_ADVFLUX_', ii, '1', fields[2] )
    CS3sba[:,kk] = get_metrics('3DDIFF_CS_ADVFLUX_', ii, '1', fields[3] )
    CS4a[:,kk] = get_metrics('3DDIFF_CS_ADVFLUX_', ii, '1', fields[4] )
    CS5a[:,kk] = get_metrics('3DDIFF_CS_ADVFLUX_', ii, '1', fields[5] )
    AS1a[:,kk] = get_metrics('3DDIFF_CS_ADVFLUX_', ii, '1', fields[6] )
    AS2a[:,kk] = get_metrics('3DDIFF_CS_ADVFLUX_', ii, '1', fields[7] )
    LID1a[:,kk] = get_metrics('3DDIFF_CS_ADVFLUX_', ii, '1', fields[8] )
    LID2a[:,kk] = get_metrics('3DDIFF_CS_ADVFLUX_', ii, '1', fields[9] )
    
    CS1d[:,kk] =  get_metrics('3DDIFF_CS_DIFFFLUX_', ii, '1', fieldsDiff[0] )
    CS2d[:,kk] = get_metrics('3DDIFF_CS_DIFFFLUX_', ii, '1', fieldsDiff[1] )
    CS3d[:,kk] = get_metrics('3DDIFF_CS_DIFFFLUX_', ii, '1', fieldsDiff[2] )
    CS3sbd[:,kk] = get_metrics('3DDIFF_CS_DIFFFLUX_', ii, '1', fieldsDiff[3] )
    CS4d[:,kk] = get_metrics('3DDIFF_CS_DIFFFLUX_', ii, '1', fieldsDiff[4] )
    CS5d[:,kk] = get_metrics('3DDIFF_CS_DIFFFLUX_', ii, '1', fieldsDiff[5] )
    AS1d[:,kk] = get_metrics('3DDIFF_CS_DIFFFLUX_', ii, '1', fieldsDiff[6] )
    AS2d[:,kk] = get_metrics('3DDIFF_CS_DIFFFLUX_', ii, '1', fieldsDiff[7] )
    LID1d[:,kk] = (get_metrics('3DDIFF_CS_DIFFFLUX_', ii, '1', fieldsDiff[8] )
                  +get_metrics('3DDIFF_CS_DIFFFLUX_', ii, '1', fieldsDiff[10] ))
    LID2d[:,kk] = (get_metrics('3DDIFF_CS_DIFFFLUX_', ii, '1', fieldsDiff[9] ) 
                  +get_metrics('3DDIFF_CS_DIFFFLUX_', ii, '1', fieldsDiff[11] ))
  
    kk=kk+1
    

for ii in tracers_CNT03:
    
    CS1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '03', ii, fields[0] )
    CS2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '03', ii, fields[1] )
    CS3a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '03', ii, fields[2] )
    CS3sba[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '03', ii, fields[3] )
    CS4a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '03', ii, fields[4] )
    CS5a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '03', ii, fields[5] )
    AS1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '03', ii, fields[6] )
    AS2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '03', ii, fields[7] )
    LID1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '03', ii, fields[8] )
    LID2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '03', ii, fields[9] )
    
    CS1d[:,kk] =  get_metrics('CNTDIFF_CS_DIFFFLUX_', '03',ii,  fieldsDiff[0] )
    CS2d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '03', ii, fieldsDiff[1] )
    CS3d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '03', ii, fieldsDiff[2] )
    CS3sbd[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '03', ii,  fieldsDiff[3] )
    CS4d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '03', ii,  fieldsDiff[4] )
    CS5d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '03', ii,  fieldsDiff[5] )
    AS1d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '03', ii,  fieldsDiff[6] )
    AS2d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '03', ii,  fieldsDiff[7] )
    LID1d[:,kk] = (get_metrics('CNTDIFF_CS_DIFFFLUX_', '03', ii, fieldsDiff[8] )
                  +get_metrics('CNTDIFF_CS_DIFFFLUX_', '03', ii, fieldsDiff[10] ))
    LID2d[:,kk] = (get_metrics('CNTDIFF_CS_DIFFFLUX_', '03', ii, fieldsDiff[9] ) 
                  +get_metrics('CNTDIFF_CS_DIFFFLUX_', '03', ii, fieldsDiff[11] ))
    
    kk=kk+1

for ii in tracers_CNT09:
    
    CS1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '09', ii, fields[0] )
    CS2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '09', ii, fields[1] )
    CS3a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '09', ii, fields[2] )
    CS3sba[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '09', ii, fields[3] )
    CS4a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '09', ii, fields[4] )
    CS5a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '09', ii, fields[5] )
    AS1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '09', ii, fields[6] )
    AS2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '09', ii, fields[7] )
    LID1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '09', ii, fields[8] )
    LID2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '09', ii, fields[9] )
    
    CS1d[:,kk] =  get_metrics('CNTDIFF_CS_DIFFFLUX_', '09',ii,  fieldsDiff[0] )
    CS2d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '09', ii, fieldsDiff[1] )
    CS3d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '09', ii, fieldsDiff[2] )
    CS3sbd[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '09', ii,  fieldsDiff[3] )
    CS4d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '09', ii,  fieldsDiff[4] )
    CS5d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '09', ii,  fieldsDiff[5] )
    AS1d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '09', ii,  fieldsDiff[6] )
    AS2d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '09', ii,  fieldsDiff[7] )
    LID1d[:,kk] = (get_metrics('CNTDIFF_CS_DIFFFLUX_', '09', ii, fieldsDiff[8] )
                  +get_metrics('CNTDIFF_CS_DIFFFLUX_', '09', ii, fieldsDiff[10] ))
    LID2d[:,kk] = (get_metrics('CNTDIFF_CS_DIFFFLUX_', '09', ii, fieldsDiff[9] ) 
                  +get_metrics('CNTDIFF_CS_DIFFFLUX_', '09', ii, fieldsDiff[11] ))
    
    kk=kk+1

for ii in tracers_CNT07:
    
    CS1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '07', ii, fields[0] )
    CS2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '07', ii, fields[1] )
    CS3a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '07', ii, fields[2] )
    CS3sba[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '07', ii, fields[3] )
    CS4a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '07', ii, fields[4] )
    CS5a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '07', ii, fields[5] )
    AS1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '07', ii, fields[6] )
    AS2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '07', ii, fields[7] )
    LID1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '07', ii, fields[8] )
    LID2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '07', ii, fields[9] )
    
    CS1d[:,kk] =  get_metrics('CNTDIFF_CS_DIFFFLUX_', '07',ii,  fieldsDiff[0] )
    CS2d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '07', ii, fieldsDiff[1] )
    CS3d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '07', ii, fieldsDiff[2] )
    CS3sbd[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '07', ii,  fieldsDiff[3] )
    CS4d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '07', ii,  fieldsDiff[4] )
    CS5d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '07', ii,  fieldsDiff[5] )
    AS1d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '07', ii,  fieldsDiff[6] )
    AS2d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '07', ii,  fieldsDiff[7] )
    LID1d[:,kk] = (get_metrics('CNTDIFF_CS_DIFFFLUX_', '07', ii, fieldsDiff[8] )
                  +get_metrics('CNTDIFF_CS_DIFFFLUX_', '07', ii, fieldsDiff[10] ))
    LID2d[:,kk] = (get_metrics('CNTDIFF_CS_DIFFFLUX_', '07', ii, fieldsDiff[9] ) 
                  +get_metrics('CNTDIFF_CS_DIFFFLUX_', '07', ii, fieldsDiff[11] ))
    
    kk=kk+1

for ii in tracers_CNT02:
    
    CS1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '02', ii, fields[0] )
    CS2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '02', ii, fields[1] )
    CS3a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '02', ii, fields[2] )
    CS3sba[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '02', ii, fields[3] )
    CS4a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '02', ii, fields[4] )
    CS5a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '02', ii, fields[5] )
    AS1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '02', ii, fields[6] )
    AS2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '02', ii, fields[7] )
    LID1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '02', ii, fields[8] )
    LID2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '02', ii, fields[9] )
    
    CS1d[:,kk] =  get_metrics('CNTDIFF_CS_DIFFFLUX_', '02',ii,  fieldsDiff[0] )
    CS2d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '02', ii, fieldsDiff[1] )
    CS3d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '02', ii, fieldsDiff[2] )
    CS3sbd[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '02', ii,  fieldsDiff[3] )
    CS4d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '02', ii,  fieldsDiff[4] )
    CS5d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '02', ii,  fieldsDiff[5] )
    AS1d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '02', ii,  fieldsDiff[6] )
    AS2d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '02', ii,  fieldsDiff[7] )
    LID1d[:,kk] = (get_metrics('CNTDIFF_CS_DIFFFLUX_', '02', ii, fieldsDiff[8] )
                  +get_metrics('CNTDIFF_CS_DIFFFLUX_', '02', ii, fieldsDiff[10] ))
    LID2d[:,kk] = (get_metrics('CNTDIFF_CS_DIFFFLUX_', '02', ii, fieldsDiff[9] ) 
                  +get_metrics('CNTDIFF_CS_DIFFFLUX_', '02', ii, fieldsDiff[11] ))
    
    kk=kk+1

for ii in tracers_CNT04:
    
    CS1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '04', ii, fields[0] )
    CS2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '04', ii, fields[1] )
    CS3a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '04', ii, fields[2] )
    CS3sba[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '04', ii, fields[3] )
    CS4a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '04', ii, fields[4] )
    CS5a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '04', ii, fields[5] )
    AS1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '04', ii, fields[6] )
    AS2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '04', ii, fields[7] )
    LID1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '04', ii, fields[8] )
    LID2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '04', ii, fields[9] )
    
    CS1d[:,kk] =  get_metrics('CNTDIFF_CS_DIFFFLUX_', '04',ii,  fieldsDiff[0] )
    CS2d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '04', ii, fieldsDiff[1] )
    CS3d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '04', ii, fieldsDiff[2] )
    CS3sbd[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '04', ii,  fieldsDiff[3] )
    CS4d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '04', ii,  fieldsDiff[4] )
    CS5d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '04', ii,  fieldsDiff[5] )
    AS1d[:,kk] =get_metrics('CNTDIFF_CS_DIFFFLUX_', '04', ii,  fieldsDiff[6] )
    AS2d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '04', ii,  fieldsDiff[7] )
    LID1d[:,kk] = (get_metrics('CNTDIFF_CS_DIFFFLUX_', '04', ii, fieldsDiff[8] )
                  +get_metrics('CNTDIFF_CS_DIFFFLUX_', '04', ii, fieldsDiff[10] ))
    LID2d[:,kk] = (get_metrics('CNTDIFF_CS_DIFFFLUX_', '04', ii, fieldsDiff[9] ) 
                  +get_metrics('CNTDIFF_CS_DIFFFLUX_', '04', ii, fieldsDiff[11] ))
    
    
    kk=kk+1

for ii in tracers_CNT10:
    
    CS1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '10', ii, fields[0] )
    CS2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '10', ii, fields[1] )
    CS3a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '10', ii, fields[2] )
    CS3sba[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '10', ii, fields[3] )
    CS4a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '10', ii, fields[4] )
    CS5a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '10', ii, fields[5] )
    AS1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '10', ii, fields[6] )
    AS2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '10', ii, fields[7] )
    LID1a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '10', ii, fields[8] )
    LID2a[:,kk] = get_metrics('CNTDIFF_CS_ADVFLUX_', '10', ii, fields[9] )
    
    CS1d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '10',ii,  fieldsDiff[0] )
    CS2d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '10', ii, fieldsDiff[1] )
    CS3d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '10', ii, fieldsDiff[2] )
    CS3sbd[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '10', ii,  fieldsDiff[3] )
    CS4d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '10', ii,  fieldsDiff[4] )
    CS5d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '10', ii,  fieldsDiff[5] )
    AS1d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '10', ii,  fieldsDiff[6] )
    AS2d[:,kk] = get_metrics('CNTDIFF_CS_DIFFFLUX_', '10', ii,  fieldsDiff[7] )
    LID1d[:,kk] = (get_metrics('CNTDIFF_CS_DIFFFLUX_', '10', ii, fieldsDiff[8] )
                  +get_metrics('CNTDIFF_CS_DIFFFLUX_', '10', ii, fieldsDiff[10] ))
    LID2d[:,kk] = (get_metrics('CNTDIFF_CS_DIFFFLUX_', '10', ii, fieldsDiff[9] ) 
                  +get_metrics('CNTDIFF_CS_DIFFFLUX_', '10', ii, fieldsDiff[11] ))
    
    
    kk=kk+1

CS1 = CS1a +CS1d  
CS2 =  CS2a +CS2d
CS3 = CS3a +CS3d
CS4 =  CS4a +CS4d
CS5 = CS5a+ CS5d
CS3sb =  CS3sba +CS3sbd
AS1 = AS1a +AS1d
AS2 =  AS2a +AS2d
LID1 = LID1a+ LID1d 
LID2 = LID2a +LID2d
    
#  LOAD WATER TRANSPORT

numWat = 10

water_3D = ['04','05','06','07'] #run number 
water_CNT = ['02','03','04','07','09','10'] # run number , constant runs

wCS1 = np.zeros((nt-1,numWat)) 
wCS2 = np.zeros((nt-1,numWat)) 
wCS3 = np.zeros((nt-1,numWat)) 
wCS4 = np.zeros((nt-1,numWat)) 
wCS5 = np.zeros((nt-1,numWat)) 
wCS3sb = np.zeros((nt-1,numWat)) 
wAS1 = np.zeros((nt-1,numWat)) 
wAS2 = np.zeros((nt-1,numWat)) 
wLID1 = np.zeros((nt-1,numWat)) 
wLID2 = np.zeros((nt-1,numWat)) 

kk = 0

fields = ['CS1','CS2','CS3','CS3sb','CS4','CS5','AS1' ,'AS2','LID1' ,'LID2']

for ii in water_3D:
    
    wCS1[:,kk] = get_water('3DDIFF_WaterCSTRANS_', ii,  fields[0] )
    wCS2[:,kk] = get_water('3DDIFF_WaterCSTRANS_', ii,  fields[1] )
    wCS3[:,kk] = get_water('3DDIFF_WaterCSTRANS_', ii,  fields[2] )
    wCS3sb[:,kk] = get_water('3DDIFF_WaterCSTRANS_', ii,  fields[3] )
    wCS4[:,kk] = get_water('3DDIFF_WaterCSTRANS_', ii,  fields[4] )
    wCS5[:,kk] = get_water('3DDIFF_WaterCSTRANS_', ii,  fields[5] )
    wAS1[:,kk] = get_water('3DDIFF_WaterCSTRANS_', ii,  fields[6] )
    wAS2[:,kk] = get_water('3DDIFF_WaterCSTRANS_', ii,  fields[7] )
    wLID1[:,kk] = get_water('3DDIFF_WaterCSTRANS_', ii,  fields[8] )
    wLID2[:,kk] = get_water('3DDIFF_WaterCSTRANS_', ii,  fields[9] )
    
    kk=kk+1
    

for ii in water_CNT:
    
    wCS1[:,kk] = get_water('CNTDIFF_WaterCSTRANS_',  ii, fields[0] )
    wCS2[:,kk] = get_water('CNTDIFF_WaterCSTRANS_',  ii, fields[1] )
    wCS3[:,kk] = get_water('CNTDIFF_WaterCSTRANS_',  ii, fields[2] )
    wCS3sb[:,kk] = get_water('CNTDIFF_WaterCSTRANS_',  ii, fields[3] )
    wCS4[:,kk] = get_water('CNTDIFF_WaterCSTRANS_',   ii, fields[4] )
    wCS5[:,kk] = get_water('CNTDIFF_WaterCSTRANS_',   ii, fields[5] )
    wAS1[:,kk] = get_water('CNTDIFF_WaterCSTRANS_',   ii, fields[6] )
    wAS2[:,kk] = get_water('CNTDIFF_WaterCSTRANS_',   ii, fields[7] )
    wLID1[:,kk] = get_water('CNTDIFF_WaterCSTRANS_',  ii, fields[8] )
    wLID2[:,kk] = get_water('CNTDIFF_WaterCSTRANS_',  ii, fields[9] )
    
    
    
    kk=kk+1

    
### NON-DIMENSIONAL PARAMETERS
kdout = np.array([1.E-7,1.E-7,1.E-5,1.E-5,
               1.E-5,1.E-4,1.E-3,(3.81)*1.E-5,(2.8)*1.E-5,(1.3)*1.E-5,1.E-5,1.E-4,1.E-3,1.E-5,1.E-4,1.E-3,
               1.E-5,1.E-4,1.E-3,(3.81)*1.E-5,(2.8)*1.E-5,(1.3)*1.E-5])

kdcan = np.array([1.E-3,1.E-4,1.E-3,1.E-4,
               1.E-5,1.E-4,1.E-3,(3.81)*1.E-5,(2.8)*1.E-5,(1.3)*1.E-5,1.E-5,1.E-4,1.E-3,1.E-5,1.E-4,1.E-3,
               1.E-5,1.E-4,1.E-3,(3.81)*1.E-5,(2.8)*1.E-5,(1.3)*1.E-5])

ki = np.array([1.0,1.0,1.0,1.0,1.0,1.0,1.0,10.0,10.0,10.0,1.0,1.0,1.0,10.0,10.0,10.0,0.1,0.1,0.1,1.0,1.0,1.0])

Z = np.array([72.0,84.0,76.0,85.0,85.0,85.0,85.0,85.0,85.0,85.0,85.0,85.0,85.0,85.0,85.0,85.0,85.0,85.0,85.0,85.0,
              85.0,85.0])
U = np.array([0.294,0.410,0.328,0.410,0.410,0.410,0.410,0.410,0.410,0.410,0.410,0.410,0.410,0.410,0.410,0.410,0.410,
             0.410,0.410,0.410,0.410,0.410])
Om = np.array([0.0033,0.00526,0.0038,0.0055,0.0055,0.0055,0.0055,0.0055,0.0055,0.0055,0.0055,0.0055,0.0055,0.0055,
               0.0055,0.0055,0.0055,0.0055,0.0055,0.0055,0.0055,0.0055])

L = 6400.0 # meters

Peh = (L*U)/ki
Pev_can = (Z*Om)/kdcan
Pev_out = (Z*Om)/kdout

K_out = (Z*Z*ki)/(L*L*kdout)
K_can = (Z*Z*ki)/(L*L*kdcan)

TrOnShList = [TrOnSh[:,0], TrOnSh[:,1],TrOnSh[:,2], TrOnSh[:,3], TrOnSh[:,4],TrOnSh[:,5], TrOnSh[:,6]
              ,TrOnSh[:,7],TrOnSh[:,8], TrOnSh[:,9],TrOnSh[:,13], TrOnSh[:,14], TrOnSh[:,15],TrOnSh[:,16],
              TrOnSh[:,17], TrOnSh[:,18],TrOnSh[:,19],TrOnSh[:,20], TrOnSh[:,21]]
HWCList = [HWC[:,0], HWC[:,1],HWC[:,2], HWC[:,3], HWC[:,4],HWC[:,5], HWC[:,6],HWC[:,7],HWC[:,8], HWC[:,9],
           HWC[:,13],HWC[:,14], HWC[:,15],HWC[:,16],HWC[:,17], HWC[:,18],HWC[:,19],HWC[:,20], HWC[:,21]]

vertical = LID1+LID2
total = AS1-AS2-CS3+CS3sb

verticala = LID1a+LID2a
totala = AS1a-AS2a-CS3a+CS3sba

verticald = LID1d+LID2d
totald = AS1d-AS2d-CS3d+CS3sbd

watVert = LID1A[0]*1000.0*wLID1 + LID2A[0]*1000.0*wLID2
watTot  = 1000.0*AS1A[0]*wAS1 -1000.0*AS2A[0]  - 1000.0*CS3A[0] + 1000.0*CS3sbA[0]



## FIGURES ##
sns.set_palette( 'Set1',9)

marker = ['s','s','s','s','o','o','o','*','*','*','d','d','d','^','^','^','>','>','>']
wmarker = ['s','s','s','s','o','*','d','.','^','>']

indexList = [0,1,2,3,4,5,6,7,8,9,13,14,15,16,17,18,19,20,21]
windexList = [0,1,2,3,4,5,6,8,9]
transEqIndex = [0,1,2,3,13,4,16,10,7,19]

#-----------------------------------------------------------------------------------------------------------------------------           

## Pe_v Advective phase
sns.set_context("talk", font_scale=0.9, rc={"lines.linewidth": 2.5})
fig42=plt.figure(figsize=(15,12))

jj=0

for ii in indexList:
    ax1 = plt.subplot(3,3,1)
    plt.plot( Pev_can[ii] ,np.mean(TrOnSh[10:,ii]),marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Mean tr mass (Mol)')
    plt.xlabel('$Pe_{vCan}$')
    plt.title(' Tracer in canyon box - Advective phase ')
    ax1.set_xscale("log", nonposy='clip')
    
    ax2 = plt.subplot(3,3,2)
    plt.plot(Pev_out[ii] , np.nanmean(HWC[10:,ii]),marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Mean volume ($m^3$)')
    plt.xlabel('$Pe_{vOut}$')
    plt.title('HCW on canyon box  ')
    ax2.set_xscale("log", nonposy='clip')
    

    ax4 = plt.subplot(3,3,4)
    plt.plot(Pev_can[ii] , np.mean(total[10:,ii]+vertical[10:,ii])*1000.0,marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Tracer transport  ($Mol/s$)')
    plt.xlabel('$Pe_{vCan}$')
    plt.title('Total transport through canyon box  ')
    ax4.set_xscale("log", nonposy='clip')
    
    
    ax7 = plt.subplot(3,3,7)
    plt.plot(Pev_can[ii] , np.mean(vertical[10:,ii])*1000.0,marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Tracer transport ($Mol/s$)')
    plt.xlabel('$Pe_{vCan}$')
    plt.title('Vertical ')
    ax7.set_xscale("log", nonposy='clip')
    
    ax8 = plt.subplot(3,3,8)
    plt.plot(Pev_can[ii] , np.mean(verticala[10:,ii])*1000.0,marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Tracer transport ($Mol/s$)')
    plt.xlabel('$Pe_{vCan}$')
    plt.title('Advective, vertical')
    ax8.set_xscale("log", nonposy='clip')
    
    ax9 = plt.subplot(3,3,9)
    plt.plot(Pev_can[ii] ,np.mean(verticald[10:,ii])*1000.0,marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Tracer transport ($Mol/s$)')
    plt.xlabel('$Pe_{vCan}$')
    plt.title('Diffusive, vertical ')
    ax9.set_xscale("log", nonposy='clip')
    
    
    jj = jj+1

for mm, ii in zip(transEqIndex,windexList):
     
    ax5 = plt.subplot(3,3,5)
    
    plt.plot(Pev_can[mm] , np.nanmean(watVert[10:,ii]),wmarker[ii], markersize = 13,alpha = 0.8,label = wlabels[ii])
    plt.ylabel('Transport ($m^3/s$)')
    plt.xlabel('$Pe_{vCan}$')
    plt.title('Vertical transport water  ')
    ax5.set_xscale("log", nonposy='clip')

plt.tight_layout()
ax2.legend(loc ='upper right', bbox_to_anchor=(2.1,1))
#ax2.legend(loc =0)          
     
plt.show()           
#fig42.savefig('results/figures/posterOSM/PevAllMetricsAdvectivePhase.eps', format='eps', dpi=1000, bbox_inches='tight')
#-----------------------------------------------------------------------------------------------------------------------------           
## Pe_h Advective phase
sns.set_context("talk", font_scale=0.9, rc={"lines.linewidth": 2.5})
fig43=plt.figure(figsize=(15,12))

jj=0

for ii in indexList:
    ax1 = plt.subplot(3,3,1)
    plt.plot( Peh[ii] ,np.mean(TrOnSh[10:,ii]),marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Mean tr mass (Mol)')
    plt.xlabel('$Pe_{h}$')
    plt.title(' Tracer in canyon box - Advective phase ')
    ax1.set_xscale("log", nonposy='clip')
    
    ax2 = plt.subplot(3,3,2)
    plt.plot(Peh[ii] , np.nanmean(HWC[10:,ii]),marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Mean volume ($m^3$)')
    plt.xlabel('$Pe_{h}$')
    plt.title('HCW on canyon box  ')
    ax2.set_xscale("log", nonposy='clip')
    

    ax4 = plt.subplot(3,3,4)
    plt.plot(Peh[ii] , np.mean(total[10:,ii]+vertical[10:,ii])*1000.0,marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Tracer transport  ($Mol/s$)')
    plt.xlabel('$Pe_{h}$')
    plt.title('Total transport through canyon box  ')
    ax4.set_xscale("log", nonposy='clip')
    
    
    ax7 = plt.subplot(3,3,7)
    plt.plot(Peh[ii] , np.mean(vertical[10:,ii])*1000.0,marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Tracer transport ($Mol/s$)')
    plt.xlabel('$Pe_{h}$')
    plt.title('Vertical ')
    ax7.set_xscale("log", nonposy='clip')
    
    ax8 = plt.subplot(3,3,8)
    plt.plot(Peh[ii] , np.mean(verticala[10:,ii])*1000.0,marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Tracer transport ($Mol/s$)')
    plt.xlabel('$Pe_{h}$')
    plt.title('Advective, vertical')
    ax8.set_xscale("log", nonposy='clip')
    
    ax9 = plt.subplot(3,3,9)
    plt.plot(Peh[ii] ,np.mean(verticald[10:,ii])*1000.0,marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Tracer transport ($Mol/s$)')
    plt.xlabel('$Pe_{h}$')
    plt.title('Diffusive, vertical ')
    ax9.set_xscale("log", nonposy='clip')
    
    
    jj = jj+1

for mm, ii in zip(transEqIndex,windexList):
     
    ax5 = plt.subplot(3,3,5)
    
    plt.plot(Peh[mm] , np.nanmean(watVert[10:,ii]),wmarker[ii], markersize = 13,alpha = 0.8,label = wlabels[ii])
    plt.ylabel('Transport ($m^3/s$)')
    plt.xlabel('$Pe_{h}$')
    plt.title('Vertical transport water  ')
    ax5.set_xscale("log", nonposy='clip')

plt.tight_layout()
ax2.legend(loc ='upper right', bbox_to_anchor=(2.1,1))
#ax2.legend(loc =0)          
     
plt.show()           
#fig43.savefig('results/figures/posterOSM/PehAllMetricsAdvectivePhase.eps', format='eps', dpi=1000, bbox_inches='tight')
#-----------------------------------------------------------------------------------------------------------------------------           
   
## Kappa Advective phase
sns.set_context("talk", font_scale=0.9, rc={"lines.linewidth": 2.5})
fig44=plt.figure(figsize=(15,12))

jj=0

for ii in indexList:
    ax1 = plt.subplot(3,3,1)
    plt.plot( K_can[ii] ,np.mean(TrOnSh[10:,ii]),marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Mean tr mass (Mol)')
    plt.xlabel('$\kappa_{can}$')
    plt.title(' Tracer in canyon box - Advective phase ')
    ax1.set_xscale("log", nonposy='clip')
    
    ax2 = plt.subplot(3,3,2)
    plt.plot(K_out[ii] , np.nanmean(HWC[10:,ii]),marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Mean volume ($m^3$)')
    plt.xlabel('$\kappa_{out}$')
    plt.title('HCW on canyon box  ')
    ax2.set_xscale("log", nonposy='clip')
    

    ax4 = plt.subplot(3,3,4)
    plt.plot(K_out[ii] , np.mean(total[10:,ii]+vertical[10:,ii])*1000.0,marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Tracer transport  ($Mol/s$)')
    plt.xlabel('$\kappa_{out}$')
    plt.title('Total transport through canyon box  ')
    ax4.set_xscale("log", nonposy='clip')
    
    
    ax7 = plt.subplot(3,3,7)
    plt.plot(K_can[ii] , np.mean(vertical[10:,ii])*1000.0,marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Tracer transport ($Mol/s$)')
    plt.xlabel('$\kappa_{can}$')
    plt.title('Vertical ')
    ax7.set_xscale("log", nonposy='clip')
    
    ax8 = plt.subplot(3,3,8)
    plt.plot(K_can[ii] , np.mean(verticala[10:,ii])*1000.0,marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Tracer transport ($Mol/s$)')
    plt.xlabel('$\kappa_{can}$')
    plt.title('Advective, vertical')
    ax8.set_xscale("log", nonposy='clip')
    
    ax9 = plt.subplot(3,3,9)
    plt.plot(K_can[ii] ,np.mean(verticald[10:,ii])*1000.0,marker[jj], markersize = 13,alpha = 0.8,label = labels[ii])
    plt.ylabel('Tracer transport ($Mol/s$)')
    plt.xlabel('$\kappa_{can}$')
    plt.title('Diffusive, vertical ')
    ax9.set_xscale("log", nonposy='clip')
    
    
    jj = jj+1

for mm, ii in zip(transEqIndex,windexList):
     
    ax5 = plt.subplot(3,3,5)
    
    plt.plot(K_can[mm] , np.nanmean(watVert[10:,ii]),wmarker[ii], markersize = 13,alpha = 0.8,label = wlabels[ii])
    plt.ylabel('Transport ($m^3/s$)')
    plt.xlabel('$\kappa_{can}$')
    plt.title('Vertical transport water  ')
    ax5.set_xscale("log", nonposy='clip')

plt.tight_layout()
ax2.legend(loc ='upper right', bbox_to_anchor=(2.1,1))
#ax2.legend(loc =0)          
     
plt.show()           
#fig44.savefig('results/figures/posterOSM/KappaAllMetricsAdvectivePhase.eps', format='eps', dpi=1000, bbox_inches='tight')
#-----------------------------------------------------------------------------------------------------------------------------           
   
