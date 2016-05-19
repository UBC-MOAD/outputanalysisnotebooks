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

import sys

from matplotlib import pylab

from mpl_toolkits.mplot3d import Axes3D

import matplotlib.cm as cm

from mayavi import mlab

from matplotlib import animation

# lib_path = os.path.abspath('../../Building_canyon/BuildCanyon/
#PythonModulesMITgcm') # Add absolute path to my python scripts
lib_path = os.path.abspath('../BuildCanyon/PythonModulesMITgcm')
# Add absolute path to my python scripts

sys.path.append(lib_path)

import ReadOutTools_MITgcm as rout
import MetricsPythonTools as mpt

#########
CGrid = ('/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run29/gridGlob_cropped.nc')
CGridOut = Dataset(CGrid)

CGridOut = Dataset(CGrid)
CState = ('/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run29/stateGlob_cropped.nc')

# General input
npart = 10
nx = 360
ny = 360
nz = 90
nt = 19  # t dimension size

rc = CGridOut.variables['RC']
dxf = CGridOut.variables['dxF']
xc = rout.getField(CGrid, 'XC')  # x coords tracer cells
yc = rout.getField(CGrid, 'YC')  # y coords tracer cells

rA = rout.getField(CGrid, 'rA')

drF = CGridOut.variables['drF']  # vertical distance between faces
drC = CGridOut.variables['drC']  # vertical distance between centers

hFacC = rout.getField(CGrid, 'HFacC')
mask_NoC = rout.getMask(CGrid, 'HFacC')

bathy = rout.getField(CGrid, 'Depth')

#########

f = Dataset('/Users/Karina/Research/PhD/Tracers/Ariane/TracerExperiments/CNTDIFF/run29_10part/ariane_trajectories_qualitative.nc', 'r')

f_lont = f.variables['traj_lon']
f_latt = f.variables['traj_lat']
f_dept = f.variables['traj_depth']
f_timet = f.variables['traj_time']

f_zs = f.variables['init_z']
f_xs = f.variables['init_x']
f_ys = f.variables['init_y']
f_lont.shape

#########
n = np.arange(npart)
colors = cm.rainbow(np.linspace(0, 1, len(n)))
mlab.figure(size=(10, 10), bgcolor=(0.16, 0.28, 0.46))


surf = mlab.mesh(xc, yc, -bathy * 30.0,
                 color=(250.0/255, 235.0/255, 215.0/255),
                 scale_factor=0.1)
# surf.actor.actor.mapper.scalar_visibility = False
# surf.actor.enable_texture = True
# surf.actor.tcoord_generator_mode = 'plane'
# mlab.show()
for N, c in zip(n, colors):
    trajectory = mlab.plot3d(f_lont[:34, 2], f_latt[:34, 2],
                             f_dept[:34, 2] * 30.0, f_dept[:34, 2],
                             colormap='RdYlGn', tube_radius=None)

mlab.colorbar(trajectory, title='Depth', orientation='vertical')

mlab.show()
