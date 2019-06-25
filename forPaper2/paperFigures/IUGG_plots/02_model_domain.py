#===============================================================================================
# IUGG 2019 Plots
#
#  MODEL DOMAIN
#
# * Astoria-like and barkley-like bathymetries
# * White contours correspond to Barkley-like bathymetry and contourf to Astoria-like bathymetry.
#
#===============================================================================================

import cmocean as cmo
import matplotlib.pyplot as plt
import matplotlib.gridspec as gspec
from matplotlib.lines import Line2D
import numpy as np
import seaborn as sns
import xarray as xr
import canyon_tools.readout_tools as rout
import canyon_tools.savitzky_golay as sg

sns.set_context('talk')
sns.set_style('white')

# Grid
grid_file1 = '/data/kramosmu/results/TracerExperiments/UPW_10TR_BF2_AST/01_Ast03/gridGlob.nc'
grid = xr.open_dataset(grid_file1)

grid_file2 = '/data/kramosmu/results/TracerExperiments/UPW_10TR_BF4_BAR/01_Bar03/gridGlob.nc'
gridBar = xr.open_dataset(grid_file2)

# General input
yslice = slice(0,360)
xslice = slice(0,616)
yslice_CS = slice(0,360) # yslice cross-shelf profiles
sb_bar = 200.0   # shelf break depth Barkely
sb_ast = 150.0   # shelf-break depth Astoria
xind_shelf = 100 # x-index shelf profile 
xind_axis = 180  # x-index canyon axis


# Create axes grid
f = plt.figure(figsize = (15,6)) 
gs = gspec.GridSpec(1, 2, width_ratios=[0.7,0.3], wspace=0.2)
ax0 = plt.subplot(gs[0])
ax1 = plt.subplot(gs[1])

#---------------- ax0 - DEPTH CONTOURS --------------------------------------------------------------
levels = [20,100,200,300,400,500,600,700,800,900,1000,1200]

CS = ax0.contourf(grid.X[xslice]/1000,grid.Y[yslice]/1000,grid.Depth[yslice,xslice],levels,
              cmap=cmo.cm.deep)
plt.colorbar(CS, ax=ax0, orientation='horizontal', aspect = 30)
ax0.text(0.45,-0.5,'Depth/m',transform=ax0.transAxes )

# Shelf break contours
ax0.contour(gridBar.X[xslice]/1000,gridBar.Y[yslice]/1000,gridBar.Depth[yslice,xslice],levels=[sb_bar],
              colors='k')
ax0.contour(grid.X[xslice]/1000,grid.Y[yslice]/1000,grid.Depth[yslice,xslice],levels=[sb_ast],
              colors='0.5')

# legend
legend_elements = [Line2D([0], [0],color='k',linewidth=2,
                          label='Barkley Canyon (%1.0f m)' %sb_bar),
                   Line2D([0], [0],color='0.5',linewidth=2,
                          label='Astoria Canyon (%1.0f m)' %sb_ast),
                   ]
ax0.legend(handles=legend_elements, bbox_to_anchor=(1,1), handletextpad=1)

# Arrows for current
ax0.arrow(10, 66, 30, 0 , width = 3, head_width=10, head_length=10, fc=sns.xkcd_rgb['coral'], ec='k')
ax0.arrow(10, 20, 30, 0 , width = 3, head_width=10, head_length=10, fc=sns.xkcd_rgb['coral'], ec='k')
ax0.text(10,75,'Alongshelf current',color=sns.xkcd_rgb['coral'] )

# ------- ax1 - CROSS-SHELF VIEW ---------------------------------------------------------------------
ax1.plot(grid.Y[yslice_CS]/1000, -grid.Depth[yslice_CS,xind_shelf], color='0.5', label='Astoria C. shelf')
ax1.plot(grid.Y[yslice_CS]/1000, -grid.Depth[yslice_CS,xind_axis], color='0.5', linestyle='--',label='Astoria C. axis')
ax1.plot(gridBar.Y[yslice_CS]/1000, -gridBar.Depth[yslice_CS,xind_shelf], color='k', label='Barkley C. shelf')
ax1.plot(gridBar.Y[yslice_CS]/1000, -gridBar.Depth[yslice_CS,xind_axis], color='k', linestyle='--', label='barkley C. axis')
ax1.legend()
ax1.set_xlim(0,110)

# labels all axes
ax0.set_aspect(1)
ax0.set_ylabel('Cross-shelf distance / km')    
ax0.set_xlabel('Alongshelf distance / km')    
ax1.set_xlabel('Cross-shelf distance / km')    
ax1.set_ylabel('Depth / m')    

plt.savefig('02_model_domain.pdf',format='pdf',bbox_inches='tight')