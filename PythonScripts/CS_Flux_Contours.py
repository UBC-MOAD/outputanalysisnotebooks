## generate colors of time dep phase and adv phase of CS transport and flux 


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


# Plotting options
sns.set()
sns.set_style('dark')
sns.set_context('talk')

# Files
CGrid = '/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run03/gridGlob.nc' # Smallest volume grid, closed bdy, no canyon.
CGridOut = Dataset(CGrid)

FluxTR01 = ('/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run03/FluxTR01Glob.nc' )
FluxTR01NoC = ('/ocean/kramosmu/MITgcm/TracerExperiments/CNTDIFF/run07/FluxTR01Glob.nc' )

# General input
nx = 360
ny = 360
nz = 90
nt = 19 # t dimension size 

rc = CGridOut.variables['RC']
xc = rout.getField(CGrid, 'XC') # x coords tracer cells
yc = rout.getField(CGrid, 'YC') # y coords tracer cells
depth = rout.getField(CGrid, 'Depth') # y coords tracer cells

drF = CGridOut.variables['drF'] # vertical distance between faces
drC = CGridOut.variables['drC'] # vertical distance between centers

times = np.arange(0,nt,1)
MaskCan = rout.getMask(CGrid,'HFacC') 
hFacCCan = rout.getField(CGrid,'HFacC') 


#Transect definitions (indices x,y,z,t)
  
CS1 = [0,40,227,227,0,30,0,18]
CS2 = [40,120,227,227,0,30,0,18]
CS3 = [120,240,267,267,0,30,0,18]
CS3sb = [120,240,227,227,0,30,0,18]
CS4 = [240,320,227,227,0,30,0,18]
CS5 = [320,359,227,227,0,30,0,18]
AS1 = [120,120,227,267,0,30,0,18]
AS2 = [240,240,227,267,0,30,0,18]
LID1 = [120,180,227,267,30,30,0,18]
LID2 = [180,240,227,267,30,30,0,18]
  
day = [0.5, 1., 1.5, 2., 2.5, 3., 3.5, 4., 4.5, 5., 5.5,  6., 6.5,  7., 7.5,  8., 8.5,  9.] # Fluxes are calculated between two outputs

TracerList = ['Tr1']  
fluxfile = [FluxTR01]
fluxtr = ['1']
  
for f,tr,trstr in zip (fluxfile,fluxtr,TracerList):
    
    keyw = ('WTRAC0%s' %tr)
    keyv = ('VTRAC0%s' %tr)
    keyu = ('UTRAC0%s' %tr)
    
    Wnm,Vnm,Unm = mpt.get_TRAC(f, keyw ,keyv, keyu)
    
    MaskExp = mpt.maskExpand(MaskCan,Unm)
    U = np.ma.MaskedArray(Unm,mask=MaskExp)
    V = np.ma.MaskedArray(Vnm,mask=MaskExp)
    W = np.ma.MaskedArray(Wnm,mask=MaskExp)


    #Get slices
    V_CS1a = mpt.slice_TRAC(V,CS1[0],CS1[1],CS1[2],CS1[3],CS1[4],CS1[5],CS1[6],CS1[7])
    V_CS2a = mpt.slice_TRAC(V,CS2[0],CS2[1],CS2[2],CS2[3],CS2[4],CS2[5],CS2[6],CS2[7])
    V_CS3a = mpt.slice_TRAC(V,CS3[0],CS3[1],CS3[2],CS3[3],CS3[4],CS3[5],CS3[6],CS3[7])
    V_CS4a = mpt.slice_TRAC(V,CS4[0],CS4[1],CS4[2],CS4[3],CS4[4],CS4[5],CS4[6],CS4[7])
    V_CS5a = mpt.slice_TRAC(V,CS5[0],CS5[1],CS5[2],CS5[3],CS5[4],CS5[5],CS5[6],CS5[7])
    V_CS3sba = mpt.slice_TRAC(V,CS3sb[0],CS3sb[1],CS3sb[2],CS3sb[3],CS3sb[4],CS3sb[5],CS3sb[6],CS3sb[7])
    U_AS1a = mpt.slice_TRAC(U,AS1[0],AS1[1],AS1[2],AS1[3],AS1[4],AS1[5],AS1[6],AS1[7])
    U_AS2a = mpt.slice_TRAC(U,AS2[0],AS2[1],AS2[2],AS2[3],AS2[4],AS2[5],AS2[6],AS2[7])
    W_LID1a = mpt.slice_TRAC(W,LID1[0],LID1[1],LID1[2],LID1[3],LID1[4],LID1[5],LID1[6],LID1[7])
    W_LID2a = mpt.slice_TRAC(W,LID2[0],LID2[1],LID2[2],LID2[3],LID2[4],LID2[5],LID2[6],LID2[7])

    
# Concatenate arrays to plot
Up = np.concatenate((V_CS1a,V_CS2a),axis = 2)
ASup = -U_AS1a
Head = V_CS3a
ASdown = U_AS2a[:,:,::-1]
Down= np.concatenate((V_CS4a,V_CS5a),axis = 2)
Vert = np.concatenate((W_LID1a,W_LID2a),axis = 2)


## FIGURE
sns.set_context("talk", font_scale=0.9, rc={"lines.linewidth": 2.5})
sns.set_palette( sns.hls_palette(11, l=.4, s=.8)) 
sns.set_style("ticks")

plt.clf()

fig45=plt.figure(figsize=(24,6))

tt = 12
ax1 = plt.subplot(1,6,1)
cn = ax1.contourf(xc[227,0:120]/1000.0,rc[0:30],np.mean(Up[10:,:,:],axis=0),15, vmax = np.max(np.mean(Up[10:,:,:],axis=0)),
                  vmin = -np.max(np.mean(Up[10:,:,:],axis=0)), cmap = 'RdYlBu_r')
cb = plt.colorbar(cn, orientation = 'horizontal',ticks=[-1, 0, 1])
cb.label('Mol/l m/s')
plt.ylabel('Depth (m) ')
plt.xlabel('Alongshore distance (km) ')


ax2 = plt.subplot(1,6,2)
cn = ax2.contourf(yc[227:267,120]/1000.0,rc[0:30],np.mean(ASup[10:,:,:],axis=0),15, vmax = -np.min(np.mean(ASup[10:,:,:],axis=0)),
                  vmin = np.min(np.mean(ASup[10:,:,:],axis=0)),cmap = 'RdYlBu_r')
cb = plt.colorbar(cn,orientation = 'horizontal')
plt.xlabel('Cross-shore distance (km) ')

ax3 = plt.subplot(1,6,3)
cn = ax3.contourf(xc[267,120:240]/1000.0,rc[0:30],np.mean(Head[10:,:,:],axis=0),15, vmax = np.max(np.mean(Head[10:,:,:],axis=0)),
                  vmin = -np.max(np.mean(Head[10:,:,:],axis=0)),cmap = 'RdYlBu_r')
cb = plt.colorbar(cn,orientation = 'horizontal')
plt.xlabel('Alongshore distance (km) ')
plt.title('CNTDIFF canyon, $K_v = 10^{-5}m^2s^{-1}$, Mean Cross-shelf transport Adv phase')

ax4 = plt.subplot(1,6,4)
cn = ax4.contourf(yc[227:267,120]/1000.0,rc[0:30],np.mean(ASdown[10:,:,:],axis=0),15, vmax = np.max(np.mean(ASdown[10:,:,:],axis=0)),
                  vmin = -np.max(np.mean(ASdown[10:,:,:],axis=0)),cmap = 'RdYlBu_r')
cb = plt.colorbar(cn,orientation = 'horizontal')
plt.xlabel('Cross-shore distance (km) ')

ax5 = plt.subplot(1,6,5)
cn = ax5.contourf(xc[227,240:-1]/1000.0,rc[0:30],np.mean(Down[10:,:,:],axis=0),15, vmax = -np.min(np.mean(Down[10:,:,:],axis=0)),
                  vmin = np.min(np.mean(Down[10:,:,:],axis=0)),cmap = 'RdYlBu_r')
cb = plt.colorbar(cn,orientation = 'horizontal')
plt.xlabel('Alongshore distance (km) ')

ax5 = plt.subplot(1,6,6)
cn = ax5.contourf(xc[227,120:240]/1000.0,yc[227:267,120]/1000.0,np.mean(Vert[10:,:,:],axis=0),15, vmax = np.max(np.mean(Vert[10:,:,:],axis=0)),
                  vmin = -np.max(np.mean(Vert[10:,:,:],axis=0)),cmap = 'RdYlBu_r')
shelfbreakline = ax5.contour(xc[227,120:240]/1000.0,yc[227:267,120]/1000.0,depth[227:267,120:240],[152.0],colors='k') 
cb = plt.colorbar(cn,orientation = 'horizontal')
plt.xlabel('Alongshore distance (km) ')
plt.ylabel('Cross-shore distance (km) ')
plt.title('Vertical transport shelf-break depth')

plt.show()
#fig45.savefig('results/figures/PosterOSM16/CS_TRANS_AdvPh_CNTrun03Tr1.eps', format='eps', dpi=1000, bbox_inches='tight')
