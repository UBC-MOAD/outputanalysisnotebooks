# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#         %%% Calculate and save bottom average concentration and shelf area %%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# The area of the pool is defined as the sum of area of the cells with anomaly of concentration 
# higher than zero. Anomaly of concentration is the bottom concentration in the canyon case 
# minus the no canyon case.
#
# The area-weighted average concentration of the pool is defined as
# $\Gamma =\frac{\sum_{i,j} C_{i,j}a_{i,j}}{\sum a_{i,j}}$
# where $C_{i,j}$ is the concentration of the (i,j)th cell with anomaly of concentration higher 
# than zero and $a_{i,j}$ is it's area.
#
# This script calls functions ConcArea(Tr, hfac, ra, bathy, sbdepth=-152.5) that returns the 
# concentration at cell closest to bottom with size (tt,nx,ny) and the area of the domain.
# Mask2DCanyon that masks out the canyon from the shelf and returns that mask ; and ConcAreaPool
# that takes the anomaly of tracer concentration (canyon-no canyon)and returns the concentration 
# at cell closest to bottom times its area. A cell is NaN if canyon case < no canyon case for 
# that cell. ConcFiltered is the masked filtered concentration near bottom and the area of the 
# pool.
#
# This script creates a xarray dataset with the variables BAC_effect, ConcPoolFilt, AreaPool, 
# ConcBaseCan, ConcBaseNoC, AreaBaseCan. 
# 
# BAC_effect is the variable I use as a metric for the effect of the canyon oon bottom average 
# concentration.
#
# To run, call as:
#
# python calc_save_BAC.py gridFile NoCgridFile ptracerFile NoCPtracerFile OUT_FILENAME 
# 			  
# KRM 06-Oct-16
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import numpy as np
from netCDF4 import Dataset
import sys 
import xarray as xr
#import canyon_tools.savitzky_golay as sg

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
  """Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
      The Savitzky-Golay filter removes high frequency noise from data.
        It has the advantage of preserving the original shape and
        features of the signal better than other types of filtering
        approaches, such as moving averages techniques.
        Parameters
        ----------
        y : array_like, shape (N,)
           the values of the time history of the signal.
       window_size : int
           the length of the window. Must be an odd integer number.
       order : int
           the order of the polynomial used in the filtering.
           Must be less then `window_size` - 1.
       deriv: int
           the order of the derivative to compute (default = 0 means only smoothing)
       Returns
       -------
       ys : ndarray, shape (N)
           the smoothed signal (or it's n-th derivative).
       Notes
       -----
       The Savitzky-Golay is a type of low-pass filter, particularly
       suited for smoothing noisy data. The main idea behind this
       approach is to make for each point a least-square fit with a
       polynomial of high order over a odd-sized window centered at
       the point.
       Examples
       --------
       t = np.linspace(-4, 4, 500)
       y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
       ysg = savitzky_golay(y, window_size=31, order=4)
       import matplotlib.pyplot as plt
       plt.plot(t, y, label='Noisy signal')
       plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
       plt.plot(t, ysg, 'r', label='Filtered signal')
       plt.legend()
       plt.show()
       References
       ----------
       .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
          Data by Simplified Least Squares Procedures. Analytical
          Chemistry, 1964, 36 (8), pp 1627-1639.
       .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
         W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
          Cambridge University Press ISBN-13: 9780521880688
       """
  import numpy as np
  from math import factorial
   
  try:
    window_size = np.abs(np.int(window_size))
    order = np.abs(np.int(order))
  
  except (ValueError, msg):
    raise ValueError("window_size and order have to be of type int")
  
  if window_size % 2 != 1 or window_size < 1:
    raise TypeError("window_size size must be a positive odd number")
  if window_size < order + 2:
    raise TypeError("window_size is too small for the polynomials order")
  
  order_range = range(order+1)
  half_window = (window_size -1) // 2
  # precompute coefficients
  b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
  m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
  # pad the signal at the extremes with
  # values taken from the signal itself
  firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
  lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
  y = np.concatenate((firstvals, y, lastvals))
  return np.convolve( m[::-1], y, mode='valid')

def ConcArea(Tr, hfac, ra, bathy, sbdepth=-152.5):
  '''Tr:tracer field (nt,nz,ny,nx)
      hfac: fraction of open cell at center (nz,ny,nx)
      ra: array of cell horizontal areas (ny,nx)
      bathy : depths 2D array from the grid file (ny,nx)
      sbdepth: shelf break depth (negative value)
      
      RETURNS:
       ConcFiltered = concentration at cell closest to bottom(nt,ny,nx)
       Area of domain'''
   
  Conc = np.empty((19,360,360))
  ConcFiltered = np.empty((19,360,360))
  Area = np.empty((360,360))
  BottomInd = np.argmax(np.array(hfac[::-1,:,:])>0.0,axis=0) # start looking for first no-land cell from the bottom up.
  BottomInd = np.ones(np.shape(BottomInd))*89 - BottomInd # Get index of unreversed z axis
  
  
  for tt in range(19):
    print(tt)
    for j in range(360):
      print(j)
      for i in range(360):
        indx = int(BottomInd[i,j])
        TrBottom = Tr[tt,indx,i,j]
        Conc[tt,i,j] = TrBottom
        Area[i,j] = ra[i,j]
      # Filter step noise
      ConcFiltered[tt,:,j] = savitzky_golay(Conc[tt,:,j], 7,3) 
               
  maskShelf = mask2DCanyon(bathy, sbdepth)
  maskShelf = np.expand_dims(maskShelf,0) # expand along time dimension
  maskShelf = maskShelf + np.zeros(Conc.shape)
  
  return (np.ma.masked_array(ConcFiltered, mask=maskShelf),Area)

def mask2DCanyon(bathy, sbdepth=-152.5):
  '''Mask out the canyon from the shelf.
   bathy : depths 2D array from the grid file
   sbdepth: shelf depth, always negative float 
   Returns mask'''
   
  bathyMasked = np.ma.masked_less(-bathy, -152.5)
  return(bathyMasked.mask)

def ConcAreaPool(Tr, hfac, ra, bathy, sbdepth=-152.5):
  '''Tr: Anomaly in tracer field (canyon - no canyon )(nt,nz,ny,nx)
       hfac: fraction of open cell at center (nz,ny,nx)
       ra: array of cell horizontal areas (ny,nx)
       bathy : depths 2D array from the grid file (ny,nx)
       sbdepth: shelf break depth (negative value)
       
       RETURNS:
       ConcArea = concentration at cell closest to bottom times its area. (nt,ny,nx)
                  A cell is NaN if canyon case < no canyon case for that cell. 
       ConcFiltered = masked filtered concentration near bottom  (nt,ny,nx)
       Area = Area of pool'''
  ConcArea = np.empty((19,360,360))
  Conc = np.empty((19,360,360))
  ConcFiltered = np.empty((19,360,360))
  Area = np.empty((19,360,360))
  BottomInd = np.argmax(np.array(hfac[::-1,:,:])>0.0,axis=0) # start looking for first no-land cell from the bottom up.
  BottomInd = np.ones(np.shape(BottomInd))*89 - BottomInd # Get index of unreversed z axis
  
  for tt in range(19):
    for j in range(360):
      for i in range(360):
        TrBottom = Tr[tt,BottomInd[i,j],i,j].data
        if TrBottom > 0.0:
          ConcArea[tt,i,j] = TrBottom*ra[i,j]
          Conc[tt,i,j] = TrBottom
          Area[tt,i,j] = ra[i,j]
        else:
          ConcArea[tt,i,j] = np.NaN
          Conc[tt,i,j] = np.NaN
          Area[tt,i,j] = np.NaN
                    
      # Filter step noise
      ConcFiltered[tt,:,j] = savitzky_golay(Conc[tt,:,j], 7,3) 
      
  maskShelf = mask2DCanyon(bathy, sbdepth)
  maskShelf = np.expand_dims(maskShelf,0) # expand along time dimension
  maskShelf = maskShelf + np.zeros(Conc.shape)
    
  return (ConcArea,np.ma.masked_array(ConcFiltered, mask=maskShelf),Area)

  
  
def main():
  
  # Input files and xarray datasets
  grid_file = sys.argv[1]+'gridGlob.nc'
  grid = xr.open_dataset(grid_file)
  
  grid_NoC_file = sys.argv[2]+'gridGlob.nc'
  grid_NoC = xr.open_dataset(grid_NoC_file)
  
  ptracer_file = sys.argv[1]+'ptracersGlob.nc'
  ptracer = xr.open_dataset(ptracer_file)
  
  ptracer_NoC_file = sys.argv[2]+'ptracersGlob.nc'
  ptracer_NoC = xr.open_dataset(ptracer_NoC_file)
  
  out_name = sys.argv[3]
  
  # Grid dimensions and variables
  nx = 360
  ny = 360
  nz = 90
  nt = 19 # t dimension size 

  bathy = grid.Depth
  hFacC = grid.HFacC
  bathyNoC = grid_NoC.Depth
  hFacCNoC = grid_NoC.HFacC
  rA = grid.rA
  
  # calculate bottom concentrations
  ConcBaseNoC, AreaBaseNoC = ConcArea(ptracer_NoC.Tr1,hFacC, rA, bathy)
  ConcBaseCan, AreaBaseCan = ConcArea(ptracer.Tr1, hFacC, rA, bathy)
  ConcxAreaPool,  ConcPoolFilt, AreaPool = ConcAreaPool(ptracer.Tr1-ptracer_NoC.Tr1, hFacC,rA, bathy)
  
  # Bottom pool effect 
  ConcTimesArea = np.nansum(np.nansum(ConcPoolFilt[:,227:300,100:]*AreaPool[:,227:300,100:],axis=1),axis=1)
  ConcTimesArea_NoC = np.nansum(ConcBaseNoC[0,227:300,100:]*AreaBaseNoC[227:300,100:])
  BAC_effect = (ConcTimesArea*100)/ConcTimesArea_NoC
  
  # save variables
  BAC_effect.name = 'BAC_effect'
  BAC_effect.attrs['units'] = '%'
    
  ConcPoolFilt.name = 'pool concentration'
  ConcPoolFilt.attrs['units'] = 'Mol/l'
  
  AreaPool.name = 'Pool area'
  AreaPool.attrs['units'] = 'm^2'
    
  ConcBaseNoC.name = 'Bottom concentration no canyon'
  ConcBaseNoC.attrs['units'] = 'Mol/l'
  
  ConcBaseCan.name = 'Bottom concentration with canyon'
  ConcBaseCan.attrs['units'] = 'Mol/l'
 
  AreaBaseCan.name = 'Area bottom shelf'
  AreaBaseCan.attrs['units'] = 'm^2'
  
  
  # Gather variables in one Dataset and save as netCDF
  objects = [BAC_effect, ConcPoolFilt,AreaPool, ConcBaseCan, ConcBaseNoC, AreaBaseCan]
  BAC_vars = xr.merge(objects, compat='broadcast_equals', join='outer')
  BAC_vars.to_netcdf(path=out_name, mode='w', format='NETCDF4')
    
    
main()