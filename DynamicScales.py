# Calculate dynamic scales from Allen and Hickey 2010 for Tracer experiments
# KRM 11-feb-2016

from math import *
#import numpy as np
#import pandas as pd
#import pylab as pl
#import scipy.io
#import scipy as spy

# Define constants
f   = 1E-4     # 1/s
N   = 5.28E-3 #3.54E-3  # 1/s for linear tracer profile
Rup = 5000.0   # m Curvature radus upstream isobath
L   = 6400     # m Length of canyon
U   = 0.1858   # m/s Strength of flow upstream of canyon (on shelf average after day 3)
Wsb = 13000.0  # m Canyon width at shelf break


# Calculate non dim numbers
Ro = U/(f*Rup)
RL = U/(f*L)
F  = Ro/(0.9+Ro)
Dh = (f*L)/N

# Calculate upwelling features scales from Allen and Hickey 2010.
Z   = 1.4*(U/N)*(L/Rup)**2 # Depth of upwelling
Phi = 1.2*(U**3*Wsb*L**(1/2))/(N*f*Rup**(3/2))                         #Upwelling Flux
Z2 = Dh*(F*RL)**(1/2)

# Upwelling scales
Ustar = Z**2/((Dh**2)*(RL**(1/2))) # Horizontal strength of upwelling current
Omega = (Z*Ustar)/L

Ustar2 = Z2**2/((Dh**2)*(RL**(1/2))) # Horizontal strength of upwelling current
Omega2 = (Z2*Ustar)/L

print('Z= %s, U*= %s, Omega= %s, Phi= %s' %(Z,Ustar,Omega,Phi))
print('Z2= %s, U2*= %s, Omega2= %s' %(Z2,Ustar2,Omega2))
