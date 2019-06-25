
#===============================================================================================
# IUGG 2019 Plots
#
#  INITIAL PROFILES  O2, NITRATE, DIC, T. Alk
#
#  * Extra figure: density profiles
#===============================================================================================

import cmocean as cmo
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np
import seaborn as sns
import xarray as xr

def calc_rho(RhoRef,T,S,alpha=2.0E-4, beta=7.4E-4):
    """-----------------------------------------------------------------------------
    calc_rho calculates the density profile using a linear equation of state.
    
    INPUT:
    state: xarray dataframe
    RhoRef : reference density at the same z as T and S slices. Can be a scalar or a 
             vector, depending on the size of T and S.
    T, S   : should be 1D arrays size nz
    alpha = 2.0E-4 # 1/degC, thermal expansion coefficient
    beta = 7.4E-4, haline expansion coefficient
    OUTPUT:
    rho - Density [nz]
    -----------------------------------------------------------------------------"""
    
    #Linear eq. of state 
    rho = RhoRef*(np.ones(np.shape(T[:])) - alpha*(T[:]) + beta*(S[:]))
    return rho

def call_rho(t,state,zslice,xind,yind):
    T = state.Temp.isel(T=t,Z=zslice,X=xind,Y=yind)
    S = state.S.isel(T=t,Z=zslice,X=xind,Y=yind)
    rho = calc_rho(RhoRef,T,S,alpha=2.0E-4, beta=7.4E-4)
    return(rho) 

def getProfile(ptracers_file, mask, trac, xind, yind, zslice, tt):
    
    with Dataset(ptracers_file, 'r') as nbl:
        
        tr = np.ma.masked_array(nbl.variables[trac][tt,zslice,yind,xind], mask = mask[zslice,yind,xind])
       
    return (tr)

sns.set_context('talk')
sns.set_style('white')

ptr_fileB = '/data/kramosmu/results/TracerExperiments/UPW_10TR_BF4_BAR/01_Bar03/ptracersGlob.nc'
grid_fileB = '/data/kramosmu/results/TracerExperiments/UPW_10TR_BF4_BAR/01_Bar03/gridGlob.nc'

ptr_fileA = '/data/kramosmu/results/TracerExperiments/UPW_10TR_BF2_AST/01_Ast03/ptracersGlob.nc'
grid_fileA = '/data/kramosmu/results/TracerExperiments/UPW_10TR_BF2_AST/01_Ast03/gridGlob.nc'

state_file = '/data/kramosmu/results/TracerExperiments/UPW_10TR_BF2_AST/01_Ast03/stateGlob.nc'
state = xr.open_dataset(state_file)

with Dataset(grid_fileB, 'r') as nbl:
    ZB = nbl.variables['RC'][:]
    
with Dataset(grid_fileA, 'r') as nbl:
    ZA = nbl.variables['RC'][:]

nz = 104
sb_Ast = 29 # shelf break z-index Astoria
sb_Bar = 39 # shelf break z-index Barkley
RhoRef = 999.79998779 # It is constant in all my runs
    
plt.rcParams.update({'font.size': 13})

tracers = ['Tr03','Tr04','Tr09','Tr10']
labels = ['Oxygen','Nitrate','DIC', 'T. Alkalinity']
colours = ['#117733','#999933', 'dimgray', 'tan']

fig,(ax0,ax1,ax2,ax3) = plt.subplots(1,4,figsize=(8,4), sharey = True)
axs = [ax0,ax1,ax2,ax3]

for ax,ii, trac, col, lab in zip(axs,range(len(tracers)),tracers , colours, labels):

    ax.axhline(-150, linestyle=':', color='0.2', label='$H_s$ Astoria C. ')
    ax.axhline(-200, linestyle='--', color='0.2', label='$H_s$ Barkley C. ')
    
    for pfile, Z, style in zip([ptr_fileA],[ZA],['-']):
        with Dataset(pfile, 'r') as nbl:
        
            if (trac == 'Tr07' or trac == 'Tr08'):
                tr_profile = nbl.variables[trac][0,:,10,180]*1E-3
                ax.plot(tr_profile, Z, color=col,linestyle=style, linewidth=3)
                ax.set_xlabel(r'C /$\mu$M', labelpad=0)
            
            elif (trac == 'Tr03' or (trac == 'Tr09' or trac == 'Tr10')):
                profile = nbl.variables[trac][0,:,10,180]
                density = call_rho(0,state,slice(0,104),180,20)
                tr_profile = (density*profile/1000)
                
                if (trac == 'Tr09' or trac == 'Tr10'):
                    ax.plot(tr_profile-tr_profile[0], Z, color=col,linestyle=style, linewidth=3)
                    ax.set_xlabel(r'C-C$_0$ / $\mu$M', labelpad=0)
                    print(tr_profile[0])
                else:
                    ax.plot(tr_profile, Z, color=col,linestyle=style, linewidth=3)
                    ax.set_xlabel(r'C / $\mu$M', labelpad=0)
            else:
                ax.set_xlabel(r'C / $\mu$M', labelpad=0)
                tr_profile = nbl.variables[trac][0,:,10,180]
                ax.plot(tr_profile, Z, color=col,linestyle=style, linewidth=3)
                
        ax.set_title(lab,pad=2)
        ax.set_ylim(-1200,0)
        ax.tick_params(axis='x', pad=2)
  
ax2.text(0.0,0.05,r'$C_0$=2029.2 $\mu$M',transform=ax2.transAxes)
ax3.text(0.0,0.05,r'$C_0$=2226.0 $\mu$M',transform=ax3.transAxes)

ax0.set_ylabel('Depth / m', labelpad=0)        
ax3.legend(bbox_to_anchor=(1,1), handlelength=1, handletextpad=0.1)
ax0.tick_params(axis='y', pad=2)

plt.savefig('03_profiles.pdf',format='pdf', bbox_inches='tight')

# --------------------------------------------------------------------------------------------------
# Density and buoyancy frequency
fig,(ax0,ax1) = plt.subplots(1,2,figsize=(3,4), sharey = True)
axs = [ax0,ax1]

colors_rho = ['darkblue', 'royalblue', 'rebeccapurple','mediumpurple']
labels_rho = ['AST', 'ARGO', 'BAR', 'PATH']

state_files = ['/data/kramosmu/results/TracerExperiments/UPW_10TR_BF2_AST/01_Ast03/stateGlob.nc',
              '/data/kramosmu/results/TracerExperiments/UPW_10TR_BF2_AST/03_Ast03_Argo/stateGlob.nc',
              '/data/kramosmu/results/TracerExperiments/UPW_10TR_BF4_BAR/01_Bar03/stateGlob.nc',
              '/data/kramosmu/results/TracerExperiments/UPW_10TR_BF4_BAR/03_Bar03_Path/stateGlob.nc']

for st, col, lab in zip(state_files,colors_rho,labels_rho):
    ss = xr.open_dataset(st)
    density = call_rho(0,ss,slice(0,104),180,20)
    N = np.sqrt(-(9.81/RhoRef)*((density.data[2:]-density.data[:-2])/((Z[2:]-Z[:-2]))))
    
    ax0.plot(density-1000,Z, color=col, label=lab) 
    ax1.plot(N*1000,Z[1:-1], color=col, label=lab) 

ax0.axhline(-150, linestyle=':', color='0.2')
ax0.axhline(-200, linestyle='--', color='0.2')
ax1.axhline(-150, linestyle=':', color='0.2', label='$H_s$ Astoria C.')
ax1.axhline(-200, linestyle='--', color='0.2',label='$H_s$ Barkley C.')
    
ax1.legend(bbox_to_anchor=(1,1),handlelength=0.7, handletextpad=0.1)
ax0.set_title('Density', pad=2)
ax1.set_title('Stratification', pad=2)

ax0.set_xlabel(r'$\sigma_{\theta}$ / kg m$^{-3}$', labelpad=-1)
ax0.tick_params(axis='x', pad=2)
ax1.tick_params(axis='x', pad=2)
ax1.set_xlabel('$N$ / $10^{-3}$s$^{-1}$', labelpad=0)

plt.savefig('03b_density_profiles.pdf',format='pdf', bbox_inches='tight')
