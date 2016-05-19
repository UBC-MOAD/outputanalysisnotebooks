from math import *

from mayavi import mlab

from netCDF4 import Dataset

import numpy as np

# Bathymetry input
grid=Dataset('/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run29/grid_few_vars.nc')
xc = grid.variables['XC'][:,:] # x coords tracer cells
yc = grid.variables['YC'][:,:] # y coords tracer cells
bathy = grid.variables['depths'][:,:]



# Particle trajectories
trajFile = Dataset('/ocean/kramosmu/Ariane/TracerExperiments/CNTDIFF/run29_10part/ariane_trajectories_qualitative.nc','r');

f_lont = trajFile.variables['traj_lon']
f_latt = trajFile.variables['traj_lat']
f_dept = trajFile.variables['traj_depth']

npart = len(f_lont[1,:])
partRange = np.arange(npart)



# mayavi figure
mlab.figure(size=(10, 10), bgcolor=(0.16, 0.28, 0.46))

surf = mlab.mesh(xc,yc,-bathy*30.0, color=(250.0/255,235.0/255,215.0/255),scale_factor=0.1) 

for nn in partRange:
  trajectory  = mlab.plot3d(f_lont[:34,nn], f_latt[:34,nn], f_dept[:34,nn]*30.0, f_dept[:34,nn], 
			    colormap='RdYlGn',tube_radius=None,
			    )
 
mlab.colorbar(trajectory, title='Depth', orientation='vertical')

mlab.show()
