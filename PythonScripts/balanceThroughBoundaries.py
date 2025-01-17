### This script calculates the flux of mass and tracer through the 4 boundaries of the domain as an advective flux.
### o-KRM-o

# o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o

from math import *
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from MITgcmutils import rdmds
from netCDF4 import Dataset
import numpy as np
import os
import pylab as pl
import scipy.io
import seaborn as sns
import sys

lib_path = os.path.abspath('../../Building_canyon/BuildCanyon/PythonModulesMITgcm') # Add absolute path to my python scripts
sys.path.append(lib_path)

import ReadOutTools_MITgcm as rout
import TransportTools_MITgcm as trt

# o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o

def areaWall(hfac,dr,dx,jj,orient):
  '''Calculate area of wall.
   INPUT
   hfac : Fraction of open cell at cell center (hFacC)
   dr : r cell face separation (drf)
   dx : cell center separation (DxG or DyG)
   jj : index of the wall location alongshore or across-shore
   orient: Character indicating whether the wall runs alongshore ('y') or across-shore ('x')

   OUTPUT
   area : np 2D array
 '''
  sizes = np.shape(hfac)
  nx = sizes[2]
  ny = sizes[1]
  nz = sizes[0]

  if orient == 'y':
    area = np.empty((nz,nx))
    for ii in range(nx):
      area[:,ii] = hfac[:,jj,ii] * dr[:] * dx[jj,ii]
    return(area)

  elif orient == 'x':
    area = np.empty((nz,ny))
    for ii in range(ny):
       area[:,ii] = hfac[:,ii,jj] * dr[:] * dx[ii,jj]
    return(area)

  else:
    print('Orient should be either y or x')

#--------------------------------------------------------------------------------------------------
def transportBdyNS(wallArea, maskC, nt, yi, fld, vel, transType='w'):
  '''Calculate the transport [mol/s or m^3/s] through N or S boundary.
  INPUT
  wallArea : 2D array with the area of the boundary. Output from areaWall.
  maskC : logical mask of the Field and velocity
  nt : number of snapshots or output time size.
  yi : boundary location index (0 for S and 359 for N)
  fld : 4D array with the scalar variable flowing through bdy. Mostly tracers.
  vel : 4D array of unstaggered normal-to-bdy component of velocity.
  transType : Character indicating whether the transport is of a scalar field (north or south) 'fn or fs' or water 'w'. Default is w.
  OUTPUT
  transportBdy : 1D array size nt with the transport through the bdy at every snapshot.
  '''
  transportBdy = np.empty(nt)

  if transType == 'w':
    for tt in range(nt):
      velo = np.ma.array(vel[tt,:,yi,:],mask=maskC[:,yi,:])
      transportBdy[tt] = np.sum(wallArea[:,:]*velo)
    return(transportBdy)

  elif transType == 'fn':
    for tt in range(nt):
      field=np.ma.array(fld[tt,:,yi,:],mask=maskC[:,yi,:])
      velo=np.ma.array(vel[tt,:,yi,:],mask=maskC[:,yi,:])
      transportBdy[tt] = np.sum(wallArea[:,:]*field*1000.0*velo) # 1000 is the conversion factor
    return(transportBdy)

  elif transType == 'fs':
    for tt in range(nt):
      
      field=np.ma.array(fld[tt,:,yi,:],mask=maskC[:,yi,:])
      velo=np.ma.array(vel[tt,:,yi,:],mask=maskC[:,yi,:])
      transportBdy[tt] = np.sum(wallArea[:,:]*field*1000.0*velo) # 1000 is the conversion factor
    return(transportBdy)

  else:
    print('transType can only be w or f')

#--------------------------------------------------------------------------------------------------
def transportBdyWE(wallArea, maskC, nt, xi, fld, vel, transType='w'):
  '''Calculate the transport [mol/s or m^3/s] through W or E boundary.
  INPUT
    wallArea : 2D array with the area of the boundary. Output from areaWall.
    maskC : logical mask of the Field and velocity
    nt : number of snapshots or output time size.
    xi : boundary location index (0 for W and 359 for E)
    fld : 4D array with the scalar variable flowing through bdy. Mostly tracers.
    vel : 4D array of unstaggered normal-to-bdy component of velocity.
    transType : Character indicating whether the transport is of a scalar field east 'fe', 'fw' scalar field west or water 'w'. Default is w.
  OUTPUT
    transportBdy : 1D array size nt with the transport through the bdy at every snapshot.
  '''
  transportBdy = np.empty(nt)

  if transType == 'w':
    for tt in range(nt):
      velo=np.ma.array(vel[tt,:,:,xi],mask=maskC[:,:,xi])
      transportBdy[tt] = np.sum(wallArea[:,:]*velo)
    return(transportBdy)

  elif transType == 'fe':
    for tt in range(nt):
      velo = np.ma.array(vel[tt,:,:,xi],mask=maskC[:,:,xi])
      field = np.ma.array(fld[tt,:,:,xi],mask=maskC[:,:,xi])
      transportBdy[tt] = np.sum(wallArea[:,:]*field*1000.0*velo) # 1000 is the conversion factor
    return(transportBdy)

  elif transType == 'fw':
    for tt in range(nt):
      velo = np.ma.array(vel[tt,:,:,xi],mask=maskC[:,:,xi])
      field = np.ma.array(fld[tt,:,:,xi],mask=maskC[:,:,xi])
      transportBdy[tt] = np.sum(wallArea[:,:]*field*1000.0*velo) # 1000 is the conversion factor
    return(transportBdy)

  else:
    print('transType can only be w, fe or fw')

#--------------------------------------------------------------------------------------------------
def balanceBdys(N,S,E,W,nt):
  '''Calculate the balance of mass or volume through boundaries.
  '''
  balance = -N + S - E + W

  return balance

#--------------------------------------------------------------------------------------------------
def balancePeriodicBdys(E,W,nt):
  '''Calculate the balance of mass or volume through boundaries.
  '''
  balance =  W - E

  return balance

#--------------------------------------------------------------------------------------------------
def balanceOpenBdys(N,S,nt):
  '''Calculate the balance of mass or volume through boundaries.
  '''
  balance = - N + S

  return balance


#--------------------------------------------------------------------------------------------------
def plotTransBdyWater(Ntrans,Strans,Etrans,Wtrans,figname):

  fig66=plt.figure(figsize=(20,15))
  sns.set(context='talk', style='whitegrid', font='sans-serif',rc={"lines.linewidth": 1.5})

  plt.subplot(2,2,1)
  ax = plt.gca()
  plt.plot(Ntrans,'go-')
  plt.ylabel('Total transport ($m^3/s$)')
  plt.xlabel('Time index')
  plt.title('North (OB)')

  plt.subplot(2,2,2)
  ax = plt.gca()
  plt.plot(Strans,'bo-')
  plt.ylabel('Total transport ($m^3/s$)')
  plt.xlabel('Time index')
  plt.title('South (OB)')

  plt.subplot(2,2,3)
  ax = plt.gca()
  plt.plot(Etrans,'mo-')
  plt.ylabel('Total transport ($m^3/s$)')
  plt.xlabel('Time index')
  plt.title('East (Periodic)')

  plt.subplot(2,2,4)
  ax = plt.gca()
  plt.plot(Wtrans,'yo-')
  plt.ylabel('Total transport ($m^3/s$)')
  plt.xlabel('Time index')
  plt.title('West (Periodic)')
  plt.show()

  fig66.savefig(figname, format='eps', dpi=1000, bbox_inches='tight')
#--------------------------------------------------------------------------------------------------
def plotTransBdyTr(Ntrans,Strans,Etrans,Wtrans,figname):

  fig67=plt.figure(figsize=(20,15))
  sns.set(context='talk', style='whitegrid', font='sans-serif',rc={"lines.linewidth": 1.5})

  plt.subplot(2,2,1)
  ax = plt.gca()
  plt.plot(Ntrans,'go-')
  plt.ylabel('Total transport ($mol/s$)')
  plt.xlabel('Time index')
  plt.title('North (OB)')

  plt.subplot(2,2,2)
  ax = plt.gca()
  plt.plot(Strans,'bo-')
  plt.ylabel('Total transport ($mol/s$)')
  plt.xlabel('Time index')
  plt.title('South (OB)')

  plt.subplot(2,2,3)
  ax = plt.gca()
  plt.plot(Etrans,'mo-')
  plt.ylabel('Total transport ($mol/s$)')
  plt.xlabel('Time index')
  plt.title('East (Periodic)')

  plt.subplot(2,2,4)
  ax = plt.gca()
  plt.plot(Wtrans,'yo-')
  plt.ylabel('Total transport ($mol/s$)')
  plt.xlabel('Time index')
  plt.title('West (Periodic)')
  plt.show()

  fig67.savefig(figname, format='eps', dpi=1000, bbox_inches='tight')
#--------------------------------------------------------------------------------------------------
def plotBalanceWater(balancevect,figname):

  fig68=plt.figure(figsize=(10,8))
  sns.set(context='talk', style='whitegrid', font='sans-serif',rc={"lines.linewidth": 1.5})

  plt.plot(balancevect,'bo-')
  plt.ylabel('Total transport ($m^3/s$)')
  plt.xlabel('Time index')
  plt.title('Water balance through boundaries')
  plt.show()

  fig68.savefig(figname, format='eps', dpi=1000, bbox_inches='tight')
#--------------------------------------------------------------------------------------------------
def plotBalanceTr(balancevect,figname):

  fig69=plt.figure(figsize=(10,8))
  sns.set(context='talk', style='whitegrid', font='sans-serif',rc={"lines.linewidth": 1.5})

  plt.plot(balancevect,'bo-')
  plt.ylabel('Total transport ($mol/s$)')
  plt.xlabel('Time index')
  plt.title('Tracer balance through boundaries')
  plt.show()

  fig69.savefig(figname, format='eps', dpi=1000, bbox_inches='tight')
# o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
def main():

  nx = 360
  ny = 360
  nz = 90
  nt = 19

  stateFile1='/ocean/kramosmu/MITgcm/TracerExperiments/NOGMREDI/run06/stateGlob.nc'
  StateOut1 = Dataset(stateFile1)

  gridFile='/ocean/kramosmu/MITgcm/TracerExperiments/NOGMREDI/run06/gridGlob.nc'
  GridOut = Dataset(gridFile)

  ptracersFile1='/ocean/kramosmu/MITgcm/TracerExperiments/NOGMREDI/run06/ptracersGlob.nc'
  PtracersOut1 = Dataset(ptracersFile1)

  X = StateOut1.variables['X']
  Y = StateOut1.variables['Y']
  Z = StateOut1.variables['Z']
  Time = StateOut1.variables['T']

  drF = GridOut.variables['drF'] # vertical distance between faces
  dxG = rout.getField(gridFile,'dxG')
  dyG = rout.getField(gridFile,'dyG')

  hFacC = rout.getField(gridFile, 'HFacC')
  MaskC = rout.getMask(gridFile,'HFacC') # same for 3 runs

  hFacS = rout.getField(gridFile, 'HFacS')
  MaskS = rout.getMask(gridFile,'HFacS') # same for 3 runs

  hFacW = rout.getField(gridFile, 'HFacW')
  MaskW = rout.getMask(gridFile,'HFacW') # same for 3 runs

  Tr1 = rout.getField(ptracersFile1,'Tr1') # [Tr#Run#] = mol/L = mol/dm^3
  uu = rout.getField(stateFile1,'U')
  vv = rout.getField(stateFile1,'V')

  U = (uu[:,:,:,:-1]+uu[:,:,:,1:])/2
  V = (vv[:,:,:-1,:]+vv[:,:,1:,:])/2
  
  rout.unstagger(uu,vv)

  NArea = areaWall(hFacC,drF,dxG,359,'y')
  NBWater = transportBdyNS(NArea, MaskC, nt, 359, V, V,  transType='w')
  NBTr1 = transportBdyNS(NArea, MaskC, nt, 359, Tr1, V, transType='fn')

  SArea = areaWall(hFacC,drF,dxG,227,'y') # Use index = 1 to calculate through Southern boundary
  SBWater = transportBdyNS(SArea, MaskC, nt, 227, V, V, transType='w')
  SBTr1 = transportBdyNS(SArea, MaskC, nt, 227, Tr1, V,transType= 'fs')

  WArea = areaWall(hFacC,drF,dyG,0,'x')
  WBWater = transportBdyWE(WArea, MaskC, nt, 0, U, U, transType='w')
  WBTr1 = transportBdyWE(WArea, MaskC, nt, 0, Tr1, U,transType= 'fw')

  EArea = areaWall(hFacC,drF,dyG,359,'x')
  EBWater = transportBdyWE(EArea, MaskC, nt, 359, U, U, 'w')
  EBTr1 = transportBdyWE(EArea, MaskC, nt, 359, Tr1, U, 'fe')

  
  #balanceWater = balancePeriodicBdys(EBWater,WBWater,nt)
  #balanceTr =balancePeriodicBdys(EBTr1,WBTr1,nt)
  
  balanceWater = balanceBdys(NBWater,SBWater,EBWater,WBWater,nt)
  balanceTr = balanceBdys(NBTr1,SBTr1,EBTr1,WBTr1,nt)
  
  figname1 = '/ocean/kramosmu/Figures/MassBalance/transBdyWaterRun06NOGMREDI_SB.eps'
  figname2 = '/ocean/kramosmu/Figures/MassBalance/transBdyTrRun06NOGMREDI_SB.eps'
  figname3 = '/ocean/kramosmu/Figures/MassBalance/balanceWaterRun06NOGMREDI_SB.eps'
  figname4 = '/ocean/kramosmu/Figures/MassBalance/balanceTrRun06NOGMREDI_SB.eps'

  plotTransBdyWater(NBWater,SBWater,EBWater,WBWater,figname1)
  plotTransBdyTr(NBTr1,SBTr1,EBTr1,WBTr1,figname2)

  plotBalanceWater(balanceWater,figname3)
  plotBalanceTr(balanceTr,figname4)

  print('Transport Water N')
  print(NBWater)
  print('Transport Water S')
  print(SBWater)
  print('Transport Water E')
  print(EBWater)
  print('Transport Water W')
  print(WBWater)
  print('Water balance')
  print(balanceWater)

  print('Transport Tr N')
  print(NBTr1)
  print('Transport Tr S')
  print(SBTr1)
  print('Transport Tr E')
  print(EBTr1)
  print('Transport Tr W')
  print(WBTr1)
  print('Tr balance')
  print(balanceTr)




main()
