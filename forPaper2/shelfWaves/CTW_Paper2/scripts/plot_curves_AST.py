import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

g = 9.81  # gravitational accel. m/s^2
Hs = 200  # m shelf break depth
f = 1.0E-4  # inertial frequency

data_mode0 = pd.read_csv('dispc_mode0_AST.dat', delim_whitespace=True,
                         header=None, names=['wavenum', 'freq', 'perturbation'])
data_mode1 = pd.read_csv('dispc_mode1_AST.dat', delim_whitespace=True,
                         header=None, names=['wavenum', 'freq', 'perturbation'])
data_mode2 = pd.read_csv('dispc_mode2_AST.dat', delim_whitespace=True,
                         header=None, names=['wavenum', 'freq', 'perturbation'])

omega0 = data_mode0['freq']
omega1 = data_mode1['freq'][:-3]
omega2 = data_mode2['freq']

k0 = data_mode0['wavenum']*100
k1 = data_mode1['wavenum'][:-3]*100
k2 = data_mode2['wavenum']*100

fig1, (ax0, ax1) = plt.subplots(1, 2, figsize=(8, 4))
ax0.plot(k0*1E5, omega0*1E4, 'k.-', label='mode 0')
ax0.plot(k1*1E5, omega1*1E4, '.-', color='0.4', label='mode 1')
ax0.plot(k2*1E5, omega2*1E4, '.-', color='0.8', label='mode 2')
ax0.plot(k1*1E5, (k1*(g*Hs)**0.5)*1E4, 'r-', label=r'$\omega=k(gH_s)^{1/2}$')
ax0.axhline(f*1E4, linestyle='--', color='0.6', label='$f$')
ax1.plot(k0*1E5, omega0/k0, 'k.-',
         label='$c_0=$%1.2f m/s' % (np.mean(omega0/k0)))
ax1.plot(k1*1E5, omega1/k1, '.-', color='0.4',
         label='$c_1=$%1.2f m/s' % (np.mean(omega1/k1)))
ax1.plot(k2*1E5, omega2/k2, '.-', color='0.8',
         label='$c_2=$%1.2f m/s' % (np.mean(omega2/k2)))
ax1.axhline((g*Hs)**0.5, linestyle='-', color='red', label='$(gH_s)^{1/2}$')

ax0.set_xlabel(r'$k$ / $10^{-5}$ rad m$^{-1}$', labelpad=0.1)
ax1.set_xlabel(r'$k$ / $10^{-5}$ rad m$^{-1}$', labelpad=0.1)
ax0.set_ylabel(r'$\omega$ / $10^{-5}$ rad s$^{-1}$', labelpad=0.1)
ax1.set_ylabel(r'$c$ / m s$^{-1}$', labelpad=-0.1)
ax0.set_ylim(0, f*2*1E4)
ax0.legend()
ax1.legend()

plt.savefig('disp_curve_AST.png', format='png', bbox_inches='tight')
