# This script sets up the records for all canyon runs
# Just run as: python canyon_records.py

# ------------------------------------------------------------
import numpy as np

def main():
    class run:
        pass

    #Define all runs, create empty run records
    #CNTDIFF_kv7 = run()  
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
    VISC3D_run01 = run()
    VISC3D_run02 = run()
    VISC3D_run03 = run()
    VISC3D_run04 = run()
    VISC3D_run06 = run()
    #LOW_BF_u26 = run()
    #LOWER_BF_u32 = run()
    #LOWEST_BF_u13 = run()
    #LOWEST_BF_N45 = run()
    #LOWEST_BF_N74 = run()
    #LOWEST_BF_f70 = run()
    #LOWEST_BF_kv3 = run()
    VISC3D_run05 = run()
 
 
    records =   [#CNTDIFF_kv7,
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
                VISC3D_run01,
                VISC3D_run02,
                VISC3D_run03,
                VISC3D_run04,
                VISC3D_run06,
                #LOW_BF_u26,
                #LOWER_BF_u32,
                #LOWEST_BF_u13,
                #LOWEST_BF_N45,
                #LOWEST_BF_N74, 
                #LOWEST_BF_f70,
                #LOWEST_BF_kv3,
                VISC3D_run05,
    ] 

    expNames = [#'CNTDIFF_run43',
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
                '3DVISC_run01',
                '3DVISC_run02',
                '3DVISC_run03',
                '3DVISC_run04',
                '3DVISC_run06',
                #'LOW_BF_run01',
                #'LOWER_BF_run01',
                #'LOWEST_BF_run01',
                #'LOWEST_BF_run03',
                #'LOWEST_BF_run05',
                #'LOWEST_BF_run07',
                #'LOWEST_BF_run11',
                '3DVISC_run05']

    expCodes = [#'CNTDIFF',
                'CNTDIFF',
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
                '3DVISC',
                '3DVISC',
                '3DVISC',
                '3DVISC',
                '3DVISC',
                #'LOW_BF',
                #'LOWER_BF',
                #'LOWEST_BF',
                #'LOWEST_BF',
                #'LOWEST_BF',
                #'LOWEST_BF',
                #'LOWEST_BF',
                '3DVISC']

    runNums  = [#'run43',
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
                'run01',
                'run02',
                'run03',
                'run04',
                'run06',
                #'run01',
                #'run01',
                #'run01',
                #'run03',
                #'run05',
                #'run07',
                #'run11',
                'run05']


    markersizes = [13,11,9,13,11,9,13,13,11,9,14,14,11,11,11,#11,11,11,11,11,11,11,
                   11]
    markerstyles = ['o','o','o','d','d','d','p','p','p','p','^','^','^','^','^',#'*','*','*','*','*','*','*',
                    '^']

    exp_labels = [  #'$\kappa$=10$^{-7}$',
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
                    '$\kappa$=10$^{-2}$,$\kappa_o$=10$^{-5}$',
                    #'U=0.243 m/s',
                    #'U=0.296 m/s',
                    #'U=0.124 m/s',
                    #'$N_0$=4.5x10$^{-3}$',
                    #'$N_0$=7.4x10$^{-3}$',
                    #'f=7.0x$10^{-5}$',
                    #'$\kappa$=10$^{-3}$',
                    '$\kappa$=5x10$^{-3}$,$\kappa_o$=10$^{-5}$',
                     ]

    colours = [ #"pine",
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
                #"sky blue",
                "light blue",
                'cerulean',
                "deep rose",
                "cherry red",
                "brown",
                "gold",
                "tan",
                #"red",
                #'dark red',
                #'burgundy',
                #'light grey',
                #'steel',
                #'cerulean',
                #'teal blue',
                'orchid'
                ]# 


    Nos = np.array([5.5E-3,5.5E-3,5.5E-3,
                    6.3E-3,#3.9E-3,3.0E-3
                    7.4E-3,4.5E-3,
                    5.5E-3,5.5E-3,5.5E-3,5.5E-3,#5.5E-3,
                    5.5E-3,5.5E-3,5.5E-3,5.5E-3,5.5E-3,
                    #5.5E-3,5.5E-3,5.5E-3,
                    #4.5E-3,7.4E-3,5.5E-3,5.5E-3,
                    5.5E-3])

    fs = np.array([9.66E-5,9.66E-5,9.66E-5,
                   9.66E-5,9.66E-5,9.66E-5,#9.66E-5,9.66E-5,
                   1.0E-4,7.68E-5,#4.84E-5,
                   8.6E-5,6.4E-5,
                   9.66E-5,9.66E-5,9.66E-5,9.66E-5,9.66E-5,
                   #9.66E-5,9.66E-5,9.66E-5,
                   #9.66E-5,9.66E-5,7.0E-5,9.66E-5,
                   9.66E-5])

    Us = np.array([0.358,0.358,0.358,
                   0.358,0.358,0.358,#0.358,0.358,
                   0.358,0.358,0.358,0.358,#0.358,
                   0.358,0.358,0.358,0.358,0.358,
                   #0.243,0.296,0.124,
                   #0.124,0.124,0.124,0.124,
                   0.358])

    Kvs = np.array([1E-5,1E-4,1E-3,
                    1E-5,1E-5,1E-5,#1E-5,1E-5,
                    1E-5,1E-5,1E-5,1E-5,#1E-5,
                    1E-3,1E-4,1E-3,1E-4,1E-2,
                    #1E-5,1E-5,1E-5,
                    #1E-5,1E-5,1E-5,1E-3,
                    5E-3])




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