#KRM
from decimal import getcontext, Decimal, Inexact

from math import *

import matplotlib.colors as mcolors

import matplotlib.pyplot as plt

from netCDF4 import Dataset

import numpy as np

import os

import pandas as pd

import pylab as pl

from scipy.stats import nanmean

import statsmodels.api as sm


def make_cmap(colors, position=None, bit=False):
  '''
  make_cmap takes a list of tuples which contain RGB values. The RGB
  values may either be in 8-bit [0 to 255] (in which bit must be set to
  true when called) or arithmetic [0 to 1] (default). make_cmap returns
  a cmap with equally spaced colors.
  Arrange your tuples so that the first color is the lowest value for the
  colorbar and the last is the highest.
  position contains values from 0 to 1 to dictate the location of each color.
  
  NAME: Custom Colormaps for Matplotlib 
  PURPOSE: This program shows how to implement make_cmap which is a function that
           generates a colorbar.  If you want to look at different color schemes,
           check out https://kuler.adobe.com/create.
  PROGRAMMER(S): Chris Slocum
  REVISION HISTORY: 20130411 -- Initial version created
                    20140313 -- Small changes made and code posted online
                    20140320 -- Added the ability to set the position of each color'''
    
  import matplotlib as mpl
  #import numpy as np
  bit_rgb = np.linspace(0,1,256)
  if position == None:
    position = np.linspace(0,1,len(colors))
  else:
    if len(position) != len(colors):
      sys.exit("position length must be the same as colors")
    elif position[0] != 0 or position[-1] != 1:
      sys.exit("position must start with 0 and end with 1")
    if bit:
      for i in range(len(colors)):
	colors[i] = (bit_rgb[colors[i][0]],
                     bit_rgb[colors[i][1]],
                     bit_rgb[colors[i][2]])
  cdict = {'red':[], 'green':[], 'blue':[]}
  for pos, color in zip(position, colors):
    cdict['red'].append((pos, color[0], color[0]))
    cdict['green'].append((pos, color[1], color[1]))
    cdict['blue'].append((pos, color[2], color[2]))
  
  cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
  return cmap

    
def getField(statefile, fieldname):
  """ Get field from MITgcm netCDF output
  statefile : string with /path/to/state.0000000000.t001.nc
  fieldname : string with the variable name as written on the netCDF file ('Temp', 'S','Eta', etc.)"""
    
  StateOut = Dataset(statefile)
  
  Fld = StateOut.variables[fieldname][:]
  
  shFld = np.shape(Fld)
  
  if len(shFld) == 1:
    
    return Fld
  
  if len(shFld) == 2:
        
    Fld2 = np.reshape(Fld,(shFld[0],shFld[1])) # reshape to pcolor order
    return Fld2 
    
  elif len(shFld) == 3:
        
    Fld2 = np.zeros((shFld[0],shFld[1],shFld[2])) 
    Fld2 = np.reshape(Fld,(shFld[0],shFld[1],shFld[2])) # reshape to pcolor order
    return Fld2 
        
  elif len(shFld) == 4:
        
    Fld2 = np.zeros((shFld[0],shFld[1],shFld[2],shFld[3])) 
    Fld2 = np.reshape(Fld,(shFld[0],shFld[1],shFld[2],shFld[3])) # reshape to pcolor order
    return Fld2
        
  else:
        
    print (' Check size of field ')
    
    
def dsum(iterable):
  
  """Full precision summation using Decimal objects for intermediate values
  Transform (exactly) a float to m * 2 ** e where m and e are integers.
  Convert (mant, exp) to a Decimal and add to the cumulative sum.
  If the precision is too small for exact conversion and addition,
  then retry with a larger precision."""
    
  getcontext().traps[Inexact] = True

  total = Decimal(0)
  for x in iterable:
    mant, exp = frexp(x)
    mant, exp = int(mant * 2.0 ** 53), exp-53
    while True:
      try:
	total += mant * Decimal(2) ** exp
        break
      except Inexact:
        getcontext().prec += 1
  return float(total)

    
def CalcDomVolume(filename2, nx, ny, nz):
  """ Calculate the volume of the domain. This function reads the fields HFacC (size (nz,ny,nx)) which contains the vertical fraction of open cell at center, 
    drF (size nz) the r cell face separation and rA the r-face area at cell center (size (ny, nx)). Then iterated through to calculate the value of each cell and add them up.
    
    filename2: Name of the grid file
    nx : number of x grid points on tracer grid
    ny : number of y grid points on tracer grid
    nz : number of z grid points on tracer grid
    
    output: 
    DomVolume: Volume of the domain
    hFacC (nz,ny,nx)
    drF (nz)
    rAC (ny,nx)
  """
    
  DomVolume = 0.0
    
  hFacC = getField(filename2,'HFacC')
  drF   = getField(filename2,'drF')
  rAC   = getField(filename2,'rA')
    
  for jj in np.arange(ny):
    
    for kk in np.arange(nz):
      
      DomVolume = DomVolume + hFacC[kk,jj,:]*drF[kk]*rAC[jj,:]
   
  #print('\n The total volume is %e m^3 \n' %DomVolume)
   
  return (sum(DomVolume), hFacC, drF, rAC)
    

def CalcVariance(nt, nz, ny, nx, DomVolume, hFacC, drF, rAC, tracer1):
  
  """ Calculate the volume-weighted mean of the squared concentration <q^2> """
  q2mean = np.zeros((nt,1))
    
  for tt in np.arange(nt):
    
    q2sum = 0.0
    
    for kk in np.arange(nz):
      
      for jj in np.arange(ny):
	
	q2sum = q2sum + np.sum(((hFacC[kk,jj,:]*drF[kk]*rAC[jj,:])/DomVolume)*(tracer1[tt,kk,jj,:])**2)
                    
    q2mean[tt] = q2sum
       
    #print('volume-weighted mean of q^2 nt=%d is %e  \n' %(tt, q2mean[tt]))
        
  return q2mean

def CalcTimeDer(q2mean, nt, delt):
  
  """Calculate time derivative using centered differences scheme """
  dqdt = (q2mean[2:]-q2mean[:-2])/(2.*delt) # approximation of time derivative of v-w mean q^2
    
  return dqdt    


def CalcAvgHorGrad(filename2, nt,nz,ny,nx,tracer1,DomVolume,hFacC, drF, rAC):
  
  """Calculate mean of (dq/dx)^2 + (dq/dy)^2)"""
  
  dxG = getField(filename2,'dxG')
  dyG = getField(filename2,'dyG')
    
  qmeanDh = np.zeros((nt,1))
  qmeanDx = np.zeros((nt,1))
  qmeanDy = np.zeros((nt,1))
    
  for tt in np.arange(nt):
    
    sumDx = 0.0
        
    tracer2dx = tracer1[tt,:,:,2:nx]
    tracer0dx = tracer1[tt,:,:,0:nx-2]
    tracerDerX = ((tracer2dx-tracer0dx)/(2.0*dxG[:,1:nx-1]))**2 # changed dxG[1:,1:nx-1] for dxG[:,1:nx-1]- size conflict
        
    for kk in np.arange(nz):
      
      for jj in np.arange(ny):
	
	sumDx = sumDx + np.sum((hFacC[kk,jj,1:nx-1]*drF[kk]*rAC[jj,1:nx-1])*(tracerDerX[kk,jj,:]))
              
        #print(sumDx)    
        
    qmeanDx[tt] = sumDx/DomVolume
        
   # print('The v-w mean of (dq/dx)^2 at nt=%d is %e \n' % (tt,qmeanDx[tt]))            
       
        
  for tt in np.arange(nt):
    
    sumDy = 0.0
        
    tracer2dy = tracer1[tt,:,2:ny,:]
    tracer0dy = tracer1[tt,:,0:ny-2,:]
    tracerDerY = ((tracer2dy-tracer0dy)/(2.0*dyG[1:ny-1,:]))**2 # changed dyG[1:ny-1,1:] for dyG[1:ny-1,:]- size conflict
        
    for kk in np.arange(nz):
      
      for ii in np.arange(nx):
	
	sumDy = sumDy + np.sum((hFacC[kk,1:ny-1,ii]*drF[kk]*rAC[1:ny-1,ii])*(tracerDerY[kk,:,ii]))
                
    qmeanDy[tt] = sumDy/DomVolume 
        
    #print('The v-w mean of (dq/dy)^2 at nt=%d is %e \n' % (tt,qmeanDy[tt]))            
    
  qmeanDh = qmeanDx + qmeanDy
    
  return qmeanDh
    
def CalcAvgVerGrad(filename2, nt,nz,ny,nx,tracer1,DomVolume,hFacC, drF, rAC):
  
  """ Calculate mean of (dq/dz)^2 """
  
  qmeanDz = np.zeros((nt,1))
    
  for tt in np.arange(nt):
    
    qsumDz = 0.0
    
    for ii in np.arange(nx):
      
      for jj in np.arange(ny):
	
	for kk in np.arange(nz-2):
	  
	  if (hFacC[kk,jj,ii]*drF[kk])+(hFacC[kk+1,jj,ii]*drF[kk+1]) == 0:
	    
	    continue
                        
          else :
	    
	    qsumDz =qsumDz +(hFacC[kk,jj,ii]*drF[kk]*rAC[jj,ii])*(((tracer1[tt,kk+1,jj,ii]-tracer1[tt,kk,jj,ii])/((hFacC[kk+1,jj,ii]*drF[kk+1])+(hFacC[kk,jj,ii]*drF[kk])))**2)
                       
    qmeanDz[tt] = qsumDz/DomVolume
        
         #print('Mean (dq/dz)^2 at nt=%d is %e \n' %(tt, qmeanDz[tt]))
      
  return qmeanDz
        
    
def FitDiffusivity(qmeanGrad, dqdt, delt):
  """Least squares fit to find the diffusivity coefficient.
     -delt is the time interval between model output.
     -dqdt is the time derivative of the volume weighted average of the tracer variance.
     -qmeanGrad is the volume weighted average of the horizontal or vertical gradient.
     *dqdt and qmeanGrad have the same shape.*
     
     This function returns the OSL (Ordinary Least Squares) regression results. to extract a value print, for example, 
     result.params or resulr.bse, etc."""
  
  x = qmeanGrad #variance of space derivatives
  
  y = 0.5*dqdt[0:len(dqdt)]

  #print(np.shape(x))
  #print(np.shape(y))

  ## fit a OLS model with intercept 
  #x = sm.add_constant(x)
  #est = sm.OLS(y, x).fit()
  result = sm.OLS(y,x).fit()
  #result.summary()
  return result 
