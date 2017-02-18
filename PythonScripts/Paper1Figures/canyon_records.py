# This script sets up the records for all canyon runs
# Just run as: python canyon_records.py

# ------------------------------------------------------------
import numpy as np

def main():
  class run:
    pass

  #Define all runs, create empty run records
  CNTDIFF_kv7 = run()  
  CNTDIFF_base = run()
  CNTDIFF_kv4 = run()
  CNTDIFF_kv3= run()
  CNTDIFF_N63 = run()
  #CNTDIFF_N39 = run()
  #CNTDIFF_N30 = run()
  CNTDIFF_N74 = run()
  CNTDIFF_N45 = run()
  CNTDIFF_f100 = run()
  CNTDIFF_f76 = run()
  #CNTDIFF_f48 = run()
  CNTDIFF_f86 = run()
  CNTDIFF_f64 = run()
  DIFF3D_run04 = run()
  DIFF3D_run05 = run()
  DIFF3D_run06 = run()
  DIFF3D_run07 = run()
  LOW_BF_u20 = run()
  LOWER_BF_u25 = run()

  records = [CNTDIFF_kv7,
	    CNTDIFF_base, 
	    CNTDIFF_kv4, 
	    CNTDIFF_kv3,
	    CNTDIFF_N63, 
	    #CNTDIFF_N39,
	    #CNTDIFF_N30,
	    CNTDIFF_N74,
	    CNTDIFF_N45,
	    CNTDIFF_f100,
	    CNTDIFF_f76,
	    #CNTDIFF_f48,
	    CNTDIFF_f86,
	    CNTDIFF_f64,
	    DIFF3D_run04,
	    DIFF3D_run05,
	    DIFF3D_run06,
	    DIFF3D_run07,
	    #LOW_BF_u20,
	    LOWER_BF_u25]

  expNames = ['CNTDIFF_run43',
	    'CNTDIFF_run38',
	    'CNTDIFF_run37',
	    'CNTDIFF_run36',
	    'CNTDIFF_run45',
	    #'CNTDIFF_run44',
	    #'CNTDIFF_run46',
	    'CNTDIFF_run73',
	    'CNTDIFF_run75',
	    'CNTDIFF_run67',
	    'CNTDIFF_run51',
	    #'CNTDIFF_run52',
	    'CNTDIFF_run69',
	    'CNTDIFF_run71',
	    '3DDIFF_run04',
	    '3DDIFF_run05',
	    '3DDIFF_run06',
	    '3DDIFF_run07',
	    #'LOW_BF_run01',
	    'LOWER_BF_run01']

  expCodes = ['CNTDIFF',
	    'CNTDIFF',
	    'CNTDIFF',
	    'CNTDIFF',
	    #'CNTDIFF',
	    #'CNTDIFF',
	    'CNTDIFF',
	    'CNTDIFF',
	    'CNTDIFF',
	    'CNTDIFF',
	    #'CNTDIFF',
	    'CNTDIFF',
	    'CNTDIFF',
	    'CNTDIFF',
	    '3DDIFF',
	    '3DDIFF',
	    '3DDIFF',
	    '3DDIFF',
	    #'LOW_BF',
	    'LOWER_BF']

  runNums  = ['run43',
	    'run38',
	    'run37',
	    'run36',
	    'run45',
	    #'run44',
	    #'run46',
	    'run73',
	    'run75',
	    'run67',
	    'run51',
	    #'run52',
	    'run69',
	    'run71',
	    'run04',
	    'run05',
	    'run06',
	    'run07',
	    #'run01',
	    'run01']


  markersizes = [15,13,11,9,13,11,9,13,13,11,9,14,14,11,11,11]
  markerstyles = ['o','o','o','o','d','d','d','p','p','p','p','^','^','^','^','*']

  exp_labels = ['$\kappa$=10$^{-7}$',
		'base',#'$N_0$=5.5x10$^{-3}$,$\kappa$=10$^{-5}$,f=9.66x10$^{-5}$,U=0.34 m/s',
		'$\kappa$=10$^{-4}$',
		'$\kappa$=10$^{-3}$',
		'$N_0$=6.3x10$^{-3}$',
		#'$N_0$=3.9x10$^{-3}$',
		#'$N_0$=3.0x10$^{-3}$',
		'$N_0$=7.4x10$^{-3}$',
		'$N_0$=4.5x10$^{-3}$',
		'f=1.0x$10^{-4}$',
		'f=7.68x10$^{-5}$',
		#'f=4.84x10$^{-5}$',
		'f=8.6x10$^{-5}$',
		'f=6.4x10$^{-5}$',
		'$\kappa$=10$^{-3}$,$\kappa_o$=10$^{-7}$',
		'$\kappa$=10$^{-4}$,$\kappa_o$=10$^{-7}$',
		'$\kappa$=10$^{-3}$,$\kappa_o$=10$^{-5}$',
		'$\kappa$=10$^{-4}$,$\kappa_o$=10$^{-5}$',
		#'U=0.20 m/s',
		'U=0.25 m/s',
	      ]

  colours = ["pine",
	    "emerald",#
	    "tealish",
	    "teal blue",# 
	    "slate grey",
	    #"black",
	    #"grey",
	    'light grey',
	    'steel',
	    "navy blue",
	    "blue",
	    #"cerulean",
	    "light blue",
	    'sky blue',
	    "deep rose",
	    "cherry red",
	    "brown",
	    "gold",
	    #"red",
	    "dark red"]# 


  Nos = np.array([5.5E-3,5.5E-3,5.5E-3,5.5E-3,
		  6.3E-3,#3.9E-3,3.0E-3
		  7.4E-3,4.5E-3,
		  5.5E-3,5.5E-3,5.5E-3,5.5E-3,#5.5E-3,
		  5.5E-3,5.5E-3,5.5E-3,5.5E-3,
		  5.5E-3])

  fs = np.array([9.66E-5,9.66E-5,9.66E-5,9.66E-5,
		9.66E-5,9.66E-5,9.66E-5,#9.66E-5,9.66E-5,
		1.0E-4,7.68E-5,#4.84E-5,
		8.6E-5,6.4E-5,
		9.66E-5,9.66E-5,9.66E-5,9.66E-5,
		9.66E-5])

  Us = np.array([0.34,0.34,0.34,0.34,
		0.34,0.34,0.34,#0.34,0.34,
		0.34,0.34,0.34,0.34,#0.34,
		0.34,0.34,0.34,0.34,
		0.25])

  Kvs = np.array([1E-7,1E-5,1E-4,1E-3,
		  1E-5,1E-5,1E-5,#1E-5,1E-5,
		  1E-5,1E-5,1E-5,1E-5,#1E-5,
		  1E-3,1E-4,1E-3,1E-4,
		  1E-5])




  # Fill the fields of the records
  for record,expName,expCode,runNum,No,fo,uo,kvo,col,explabel,marksize,markstyle in zip(records,expNames,
											expCodes,runNums,
											Nos,fs,Us,Kvs,
											colours,exp_labels,
											markersizes,markerstyles):
      record.name = expName
      record.exp_code = expCode
      record.run_num = runNum
      record.label = explabel
      record.color = col
      record.msize = marksize
      record.mstyle = markstyle
      record.N = No
      record.f = fo
      record.u = uo
      record.kv = kvo

  return(records)