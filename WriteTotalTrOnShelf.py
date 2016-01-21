
# coding: utf-8

# ## Develop functions and script to write down metrics on files
# 
# 

# In[1]:

#import gsw as sw # Gibbs seawater package

from math import *

from MITgcmutils import rdmds

from netCDF4 import Dataset

import numpy as np

import os 

import pylab as pl

import scipy.io

import scipy as spy

import sys


# In[2]:

lib_path = os.path.abspath('../../Building_canyon/BuildCanyon/PythonModulesMITgcm') # Add absolute path to my python scripts
sys.path.append(lib_path)

import ReadOutTools_MITgcm as rout 


# In[ ]:




# In[3]:

def getDatasets(expPath, runName):
    '''Specify the experiment and run from which to analyse state and ptracers output.
    expName : (string) Path to experiment folder. E.g. '/ocean/kramosmu/MITgcm/TracerExperiments/BARKLEY', etc.
    runName : (string) Folder name of the run. E.g. 'run01', 'run10', etc
    '''
    Grid =   "%s/%s/gridGlob.nc" %(expPath,runName)
    GridOut = Dataset(Grid)

    State =  "%s/%s/stateGlob.nc" %(expPath,runName)
    StateOut = Dataset(State)

    Ptracers =  "%s/%s/ptracersGlob.nc" %(expPath,runName)
    PtracersOut = Dataset(Ptracers)
    
    return (Grid, GridOut, State,StateOut,Ptracers, PtracersOut)


# In[5]:

def getProfile(Tr,yi,xi,nz0=0,nzf=89):
    '''Slice tracer profile at x,y = xi,yi form depth index k=nz0 to k=nzf. Default values are nz0=0 (surface)
    and nzf = 89, bottom. Tr is a time slice (3D) of the tracer field'''
    IniProf = Tr[nz0:nzf,xi,yi]
    return IniProf


# In[7]:

def maskExpand(mask,Tr):
    
    '''Expand the dimensions of mask to fit those of Tr. mask should have one dimension less than Tr (time axis). 
    It adds a dimension before the first one.'''
    
    mask_expand = np.expand_dims(mask,0)
    
    mask_expand = mask_expand + np.zeros(Tr.shape)
    
    return mask_expand

    


# In[14]:

def howMuchWaterX(Tr,MaskC,nzlim,rA,hFacC,drF,yin,zfin,xi,yi):
    '''
    INPUT----------------------------------------------------------------------------------------------------------------
    Tr    : Array with concentration values for a tracer. Until this function is more general, this should be size 19x90x360x360
    MaskC : Land mask for tracer
    nzlim : The nz index under which to look for water properties
    rA    : Area of cell faces at C points (360x360)
    fFacC : Fraction of open cell (90x360x360)
    drF   : Distance between cell faces (90)
    yin   : across-shore index of shelf break
    zfin  : shelf break index + 1 
    xi    : initial profile x index
    yi    : initial profile y index
    
    OUTPUT----------------------------------------------------------------------------------------------------------------
    VolWaterHighConc =  Array with the volume of water over the shelf [:,:30,227:,:] at every time output.
    Total_Tracer =  Array with the mass of tracer (m^3*[C]*l/m^3) at each x-position over the shelf [:,:30,227:,:] at 
                    every time output. Total mass of tracer at xx on the shelf.
                                                
    -----------------------------------------------------------------------------------------------------------------------
    '''
    maskExp = maskExpand(MaskC,Tr)

    TrMask=np.ma.array(Tr,mask=maskExp)   
    
    trlim = TrMask[0,nzlim,yi,xi]
    
    print('tracer limit concentration is: ',trlim)
    
    WaterX = 0
    
    # mask cells with tracer concentration < trlim on shelf
    HighConc_Masked = np.ma.masked_less(TrMask[:,:zfin,yin:,:], trlim) 
    HighConc_Mask = HighConc_Masked.mask
    
    #Get volume of water of cells with relatively high concentration
    rA_exp = np.expand_dims(rA[yin:,:],0)
    drF_exp = np.expand_dims(np.expand_dims(drF[:zfin],1),1)
    rA_exp = rA_exp + np.zeros(hFacC[:zfin,yin:,:].shape)
    drF_exp = drF_exp + np.zeros(hFacC[:zfin,yin:,:].shape)
    
    ShelfVolume = hFacC[:zfin,yin:,:]*drF_exp*rA_exp
    ShelfVolume_exp = np.expand_dims(ShelfVolume,0)
    ShelfVolume_exp = ShelfVolume_exp + np.zeros(HighConc_Mask.shape)
    
    HighConc_CellVol = np.ma.masked_array(ShelfVolume_exp,mask = HighConc_Mask) 
    VolWaterHighConc = np.ma.sum(np.ma.sum(np.ma.sum(HighConc_CellVol,axis = 1),axis=1),axis=1)
    
    #Get total mass of tracer on shelf
    Total_Tracer = np.ma.sum(np.ma.sum(np.ma.sum(ShelfVolume_exp*TrMask[:,:zfin,yin:,:]*1000.0,axis = 1),axis=1),axis=1) 
    # 1 m^3 = 1000 l
    
    return (VolWaterHighConc, Total_Tracer)



# In[ ]:

#import glob
#def specifyExpFluxes(expPath, runName):
#    '''Specify the experiment and run from which to analyse output.
#    expName : (string) Path to experiment folder. E.g. '/ocean/kramosmu/MITgcm/TracerExperiments/BARKLEY', etc.
#    runName : (string) Folder name of the run. E.g. 'run01', 'run10', etc
#    '''
#    path = "%s/%s/Flux*.nc" %(expPath,runName)
#    for fname in glob.glob(path):
#    print(fname)


# In[9]:

# General input

Grid1, GridOut1, State1,StateOut1,Ptracers1, PtracersOut1 = getDatasets('/ocean/kramosmu/MITgcm/TracerExperiments/BARKLEY', 'run01')

nx = 360
ny = 360
nz = 90
nt = 19 # t dimension size 

rc = GridOut1.variables['RC']
xc = rout.getField(Grid1, 'XC') # x coords tracer cells
yc = rout.getField(Grid1, 'YC') # y coords tracer cells

drF = GridOut1.variables['drF'] # vertical distance between faces
dxG = rout.getField(Grid1,'dxG')

MaskCan = rout.getMask(Grid1,'HFacC') 
hFacCCan = rout.getField(Grid1,'HFacC') 
rACan = rout.getField(Grid1,'rA') 
drFCan=GridOut1.variables['drF']


# In[ ]:




# In[10]:

# Load tracers 
Tr1 = rout.getField(Ptracers1,'Tr01')
#Tr2 = rout.getField(Ptracers1,'Tr02') 
#Tr3 = rout.getField(Ptracers1,'Tr03') 
#Tr4 = rout.getField(Ptracers1,'Tr04') 


# In[11]:

#Tr5 = rout.getField(Ptracers1,'Tr05') 
#Tr6 = rout.getField(Ptracers1,'Tr06') 
#Tr7 = rout.getField(Ptracers1,'Tr07') 
#Tr8 = rout.getField(Ptracers1,'Tr08') 


# In[12]:

Tr1ini = getProfile(Tr1[0,:,:,:],50,180) #Default is to get the whole column
#Tr2ini = getProfile(Tr2[0,:,:,:],50,180)
#Tr3ini = getProfile(Tr3[0,:,:,:],50,180)
#Tr4ini = getProfile(Tr4[0,:,:,:],50,180)
#Tr5ini = getProfile(Tr5[0,:,:,:],50,180)
#Tr6ini = getProfile(Tr6[0,:,:,:],50,180)
#Tr7ini = getProfile(Tr7[0,:,:,:],50,180)
#r8ini = getProfile(Tr8[0,:,:,:],50,180)


# 

# In[ ]:




# In[ ]:




# 

# In[15]:



(WatTr1, TrMassTr1) = howMuchWaterX(Tr1,MaskCan,30,rACan,hFacCCan,drFCan,227,30,50,180) 
#(WatTr2, TrMassTr2) = howMuchWaterX(Tr2,MaskCan,30,rACan,hFacCCan,drFCan,227,30,50,180) 
#(WatTr3, TrMassTr3) = howMuchWaterX(Tr3,MaskCan,30,rACan,hFacCCan,drFCan,227,30,50,180) 
#(WatTr4, TrMassTr4) = howMuchWaterX(Tr4,MaskCan,30,rACan,hFacCCan,drFCan,227,30,50,180) 
#(WatTr5, TrMassTr5) = howMuchWaterX(Tr5,MaskCan,30,rACan,hFacCCan,drFCan,227,30,50,180) 
#(WatTr6, TrMassTr6) = howMuchWaterX(Tr6,MaskCan,30,rACan,hFacCCan,drFCan,227,30,50,180) 
#(WatTr7, TrMassTr7) = howMuchWaterX(Tr7,MaskCan,30,rACan,hFacCCan,drFCan,227,30,50,180) 
#(WatTr8, TrMassTr8) = howMuchWaterX(Tr8,MaskCan,30,rACan,hFacCCan,drFCan,227,30,50,180) 
      
    


# In[32]:

def dumpFiles(filename,variable,form = 'dump'):
    
    '''Filename is a string with the path,filename and extension to write into; variable is the np array to save 
    and form is the file format to save to, it can be either 'dump' which uses np.ma.dump or 'txt' for a regular 
    text file. To load the arrays use np.load(filename)'''
     
    if form == 'dump':
        np.ma.dump(variable,filename)
    elif form == 'txt':
        np.savetxt(filename, variable)
    else:
        print('Format has to be dump or txt')
        
    


# In[30]:




# In[25]:




# In[26]:




# In[27]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# 

# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



