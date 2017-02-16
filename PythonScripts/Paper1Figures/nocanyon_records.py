# This script sets up the records for all no canyon runs
# Just run as: python nocanyon_records.py

# ------------------------------------------------------------
import numpy as np

def main():

  # Create an empty class to save information of every run
  class run:
      pass

  #Define all no canyon runs, create empty run records
  CNTDIFF_kv7NoC = run()  
  CNTDIFF_baseNoC = run()
  CNTDIFF_kv4NoC = run()
  CNTDIFF_kv3NoC= run()
  CNTDIFF_N63NoC = run()
  CNTDIFF_N39NoC = run()
  CNTDIFF_N30NoC = run()
  CNTDIFF_N74NoC = run()
  CNTDIFF_N45NoC = run()
  CNTDIFF_f100NoC = run()
  CNTDIFF_f76NoC = run()
  CNTDIFF_f48NoC = run()
  CNTDIFF_f86NoC = run()
  CNTDIFF_f64NoC = run()
  DIFF3D_run04NoC = run()
  DIFF3D_run05NoC = run()
  DIFF3D_run06NoC = run()
  DIFF3D_run07NoC = run()
  #LOW_BF_u20NoC = run()
  LOWER_BF_u25NoC = run()

  recordsNoC =   [CNTDIFF_kv7NoC,
		  CNTDIFF_baseNoC, 
		  CNTDIFF_kv4NoC, 
		  CNTDIFF_kv3NoC,
		  CNTDIFF_N63NoC, 
		  CNTDIFF_N39NoC,
		  CNTDIFF_N30NoC,
		  CNTDIFF_N74NoC,
		  CNTDIFF_N45NoC,
		  CNTDIFF_f100NoC,
		  CNTDIFF_f76NoC,
		  CNTDIFF_f48NoC,
		  CNTDIFF_f86NoC,
		  CNTDIFF_f64NoC,
		  DIFF3D_run04NoC,
		  DIFF3D_run05NoC,
		  DIFF3D_run06NoC,
		  DIFF3D_run07NoC,
		  #LOW_BF_u20NoC,
		  LOWER_BF_u25NoC]

  expNamesNoC = ['CNTDIFF_run64',
	      'CNTDIFF_run42',
	      'CNTDIFF_run65',
	      'CNTDIFF_run66',
	      'CNTDIFF_run48',
	      'CNTDIFF_run47',
	      'CNTDIFF_run49',
	      'CNTDIFF_run74',
	      'CNTDIFF_run76',
	      'CNTDIFF_run68',
	      'CNTDIFF_run53',
	      'CNTDIFF_run54',
	      'CNTDIFF_run70',
	      'CNTDIFF_run72',
	      'CNTDIFF_run42',
	      'CNTDIFF_run42',
	      'CNTDIFF_run64',
	      'CNTDIFF_run64',
	      #'LOW_BF_run02',
	      'LOWER_BF_run02']

  expCodesNoC = ['CNTDIFF',
	      'CNTDIFF',
	      'CNTDIFF',
	      'CNTDIFF',
	      'CNTDIFF',
	      'CNTDIFF',
	      'CNTDIFF',
	      'CNTDIFF',
	      'CNTDIFF',
	      'CNTDIFF',
	      'CNTDIFF',
	      'CNTDIFF',
	      'CNTDIFF',
	      'CNTDIFF',
	      'CNTDIFF',
	      'CNTDIFF',
	      'CNTDIFF',
	      'CNTDIFF',
	      #'LOW_BF',
	      'LOWER_BF']

  runNumsNoC  = ['run64',
	      'run42',
	      'run65',
	      'run66',
	      'run48',
	      'run47',
	      'run49',
	      'run74',
	      'run76',
	      'run68',
	      'run53',
	      'run54',
	      'run70',
	      'run72',
	      'run42',
	      'run42',
	      'run64',
	      'run64',
	      #'run02',
	      'run02']


  markersizes = [15,13,11,9,13,13,11,11,9,13,13,11,11,9,14,14,11,11,11,11]
  markerstyles = ['o','o','o','o','d',"d","d",'d','d','p','p','p','p','p','^','^','^','^','*']

  exp_labelsNoC = ['$\kappa$=10$^{-7}$',
		  '$N_0$=5.5x10$^{-3}$,$\kappa$=10$^{-5}$,f=9.66x10$^{-5}$,U=0.34 m/s',
		  '$\kappa$=10$^{-4}$',
		  '$\kappa$=10$^{-3}$',
		  '$N_0$=6.3x10$^{-3}$',
		  '$N_0$=3.9x10$^{-3}$',
		  '$N_0$=3.0x10$^{-3}$',
		  '$N_0$=7.4x10$^{-3}$',
		  '$N_0$=4.5x10$^{-3}$',
		  'f=1.0x$10^{-4}$',
		  'f=7.68x10$^{-5}$',
		  'f=4.84x10$^{-5}$',
		  'f=8.6x10$^{-5}$',
		  'f=6.4x10$^{-5}$',
		  '$\kappa_o$=10$^{-7}$',
		  '$\kappa_o$=10$^{-7}$',
		  '$\kappa_o$=10$^{-5}$',
		  '$\kappa_o$=10$^{-5}$',
		  #'U=0.20 m/s',
		  'U=0.25 m/s',
		]

  colours = ["pine",
	      "emerald",#
	      "tealish",
	      "teal blue",# 
	      "slate grey",
	      "black",
	      "grey",
	      'light grey',
	      'steel',
	      "navy blue",
	      "blue",
	      "cerulean",
	      "light blue",
	      'sky blue',
	      "deep rose",
	      "cherry red",
	      "brown",
	      "gold",
	      #"red",
	      "dark red"]# 


  Nos = np.array([5.5E-3,5.5E-3,5.5E-3,5.5E-3,
		    6.3E-3,3.9E-3,3.0E-3,7.4E-3,4.5E-3,
		    5.5E-3,5.5E-3,5.5E-3,5.5E-3,5.5E-3,
		    5.5E-3,5.5E-3,5.5E-3,5.5E-3,
		    5.5E-3])

  fs = np.array([9.66E-5,9.66E-5,9.66E-5,9.66E-5,
		  9.66E-5,9.66E-5,9.66E-5,9.66E-5,9.66E-5,
		  1.0E-4,7.68E-5,4.84E-5,8.6E-5,6.4E-5,
		  9.66E-5,9.66E-5,9.66E-5,9.66E-5,
		  9.66E-5])

  Us = np.array([0.34,0.34,0.34,0.34,
		  0.34,0.34,0.34,0.34,0.34,
		  0.34,0.34,0.34,0.34,0.34,
		  0.34,0.34,0.34,0.34,
		  0.25])

  KvsNoC = np.array([1E-7,1E-5,1E-4,1E-3,
		    1E-5,1E-5,1E-5,1E-5,1E-5,
		    1E-5,1E-5,1E-5,1E-5,1E-5,
		    1E-7,1E-7,1E-5,1E-5,
		    1E-5])




  # Fill the fields of the records
  for record,expName,expCode,runNum,No,fo,uo,kvo,col,explabel,marksize,markstyle in zip(recordsNoC,expNamesNoC,
											  expCodesNoC,runNumsNoC,
											  Nos,fs,Us,KvsNoC,
											  colours,exp_labelsNoC,
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
  
  return(recordsNoC)
