
import numpy as np
import xarray as xr

convadj_file = '/data/kramosmu/results/TracerExperiments/CNTDIFF_DIAG_IVDC/run01/convadjGlob.nc'
ivdc = xr.open_dataset(convadj_file)

ind_tt = []
ind_kk = []
ind_jj = []
ind_ii = []

for tt in range(216):
    for ii in range(120,360):
        for jj in range(210,360):
            for kk in range(40):
                if ivdc.CONVADJ[tt,kk,jj,ii]>0.0:
                    ind_tt = ind_tt.append(tt)
                    ind_kk = ind_kk.append(kk)
                    ind_jj = ind_jj.append(jj)
                    ind_ii = ind_ii.append(ii)
    print(tt,kk,jj,ii)

print(tt,kk,jj,ii)                    

