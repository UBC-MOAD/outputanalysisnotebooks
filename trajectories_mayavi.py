from math import *

from mayavi import mlab

import matplotlib.colors as mcolors

#from MITgcmutils import rdmds

from netCDF4 import Dataset

import numpy as np

import os 

import pylab as pl

import sys

from matplotlib import pylab

import matplotlib.cm as cm


lib_path = os.path.abspath('../../Building_canyon/BuildCanyon/PythonModulesMITgcm') # Add absolute path to my python scripts
#lib_path = os.path.abspath('../BuildCanyon/PythonModulesMITgcm') # Add absolute path to my python scripts

sys.path.append(lib_path)

import ReadOutTools_MITgcm as rout
import MetricsPythonTools as mpt


#########
CGrid ='/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run29/gridGlob_cropped.nc'
CGridOut = Dataset(CGrid )

CGridOut=Dataset(CGrid)
CState ='/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run29/stateGlob_cropped.nc' 

# General input

xc = rout.getField(CGrid, 'XC') # x coords tracer cells
yc = rout.getField(CGrid, 'YC') # y coords tracer cells

bathy = rout.getField(CGrid,'Depth')

#########

f = Dataset('/ocean/kramosmu/Ariane/TracerExperiments/CNTDIFF/run29_10part/ariane_trajectories_qualitative.nc','r');

f_lont=f.variables['traj_lon']
f_latt=f.variables['traj_lat']
f_dept=f.variables['traj_depth']


#########
npart = len(f_lont[1,:])

partRange = np.arange(npart)
mlab.figure(size=(10, 10), bgcolor=(0.16, 0.28, 0.46))

surf = mlab.mesh(xc,yc,-bathy*30.0, color=(250.0/255,235.0/255,215.0/255),scale_factor=0.1) 
#surf.actor.actor.mapper.scalar_visibility = False
#surf.actor.enable_texture = True
#surf.actor.tcoord_generator_mode = 'plane'
#mlab.show()

for nn in partRange:
  trajectory  = mlab.plot3d(f_lont[:34,nn], f_latt[:34,nn], f_dept[:34,nn]*30.0, f_dept[:34,nn], 
			    colormap='RdYlGn',tube_radius=None,
			    )
 
mlab.colorbar(trajectory, title='Depth', orientation='vertical')

mlab.show()
