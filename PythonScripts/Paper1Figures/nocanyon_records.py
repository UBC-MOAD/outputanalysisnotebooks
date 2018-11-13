# This script sets up the records for all no canyon runs
# Just run as: python nocanyon_records.py

# ------------------------------------------------------------
import numpy as np

def main():
    
    # Create an empty class to save information of every run
    class run:
        pass

    #Define all no canyon runs, create empty run records
    #CNTDIFF_kv7NoC = run()  
    CNTDIFF_baseNoC = run()
    CNTDIFF_kv4NoC = run()
    CNTDIFF_kv3NoC= run()
    CNTDIFF_N63NoC = run()
    CNTDIFF_N74NoC = run()
    CNTDIFF_N45NoC = run() 
    CNTDIFF_N50NoC = run() 
    CNTDIFF_f100NoC = run()
    CNTDIFF_f76NoC = run()
    CNTDIFF_f86NoC = run()
    CNTDIFF_f64NoC = run()
    VISC3D_run01NoC = run()
    VISC3D_run02NoC = run()
    VISC3D_run03NoC = run()
    VISC3D_run04NoC = run()
    VISC3D_run05NoC = run()
    VISC3D_run06NoC = run()
    LOWER_BF_u32NoC = run()
    LOW_BF_u26NoC = run()
    LOWEST_BF_u13NoC = run()
    LOWEST_BF_N45NoC = run()
    LOWEST_BF_N74NoC = run()
    LOWEST_BF_f70NoC = run()
    LOWEST_BF_kv3NoC = run()
    REALKV_MTY_botNoC = run()
    REALKV_EEL_botNoC = run()
    REALKV_MTY_rimNoC = run()
    #REALKV_EEL_rimNoC = run()
    REALKV_ASC_botNoC = run()
    REALKV_ASC_rimNoC = run()
    REALKV_e10NoC = run()
    REALKV_e25NoC = run()
    REALKV_e50NoC = run()
    REALKV_e100NoC = run()
    REALKV_e05NoC = run()
    REALKV_e15NoC = run()
    REALKV_e75NoC = run()
    REALKV_e150NoC = run()
    REALKV_e5step1E2NoC = run()
    REALKV_e5step5E3NoC = run()
    REALKV_e5step1E3NoC = run()
    REALKV_step1E2NoC = run()
    REALKV_e25_kv1E3NoC = run()
    REALKV_e100_kv1E3NoC = run()
    REALKV_e25_kv5E3NoC = run()
    REALKV_e100_kv5E3NoC = run()
    REALKV_e05_kv8E3NoC = run()
    REALKV_e05_kv1p2E2NoC = run()
    REALKV_e05_kv2p5E3NoC = run()
    REALKV_e05_kv5E4NoC = run()
    REALKV_e05_kv1E2_nosmoothNoC = run()
    REALKV_kv1E2_correctZNoC = run()
    CNTDIFF_N47NoC = run() 
    LONGER_CNY_run01NoC = run()
    LONGER_CNY_LOWEST_Urun01NoC = run()
    LONGER_CNY2_run01NoC = run()

    recordsNoC =   [CNTDIFF_baseNoC, 
                    CNTDIFF_kv4NoC, 
                    CNTDIFF_kv3NoC,
                    CNTDIFF_N63NoC, 
                    CNTDIFF_N74NoC,
                    CNTDIFF_N45NoC,
                    CNTDIFF_N50NoC,
                    CNTDIFF_f100NoC,
                    CNTDIFF_f76NoC,
                    CNTDIFF_f86NoC,
                    CNTDIFF_f64NoC,
                    VISC3D_run01NoC,
                    VISC3D_run02NoC,
                    VISC3D_run03NoC,
                    VISC3D_run04NoC,
                    VISC3D_run05NoC,
                    VISC3D_run06NoC,        
                    LOWER_BF_u32NoC,
                    LOW_BF_u26NoC,
                    LOWEST_BF_u13NoC,
                    LOWEST_BF_N45NoC,
                    LOWEST_BF_N74NoC,
                    LOWEST_BF_f70NoC,
                    LOWEST_BF_kv3NoC,
                    REALKV_MTY_botNoC,
                    REALKV_EEL_botNoC,
                    REALKV_MTY_rimNoC,
                    #REALKV_EEL_rimNoC,
                    REALKV_ASC_botNoC,
                    REALKV_ASC_rimNoC,
                    REALKV_e10NoC, 
                    REALKV_e25NoC,
                    REALKV_e50NoC, 
                    REALKV_e100NoC,
                    REALKV_e15NoC, 
                    REALKV_e75NoC,
                    REALKV_e150NoC, 
                    REALKV_e05NoC,
                    REALKV_e5step1E2NoC,
                    REALKV_e5step1E3NoC,
                    REALKV_e5step5E3NoC, 
                    REALKV_step1E2NoC,
                    REALKV_e25_kv1E3NoC,
                    REALKV_e100_kv1E3NoC,
                    REALKV_e25_kv5E3NoC,
                    REALKV_e100_kv5E3NoC,
                    REALKV_e05_kv8E3NoC,
                    REALKV_e05_kv1p2E2NoC,
                    REALKV_e05_kv2p5E3NoC,
                    REALKV_e05_kv5E4NoC,
                    REALKV_e05_kv1E2_nosmoothNoC,
                    REALKV_kv1E2_correctZNoC,
                    CNTDIFF_N47NoC,
                    LONGER_CNY_run01NoC ,
                    LONGER_CNY_LOWEST_Urun01NoC,
                    LONGER_CNY2_run01NoC ,] 

    expNamesNoC =['CNTDIFF_run42',
                  'CNTDIFF_run41',
                  'CNTDIFF_run40',
                  'CNTDIFF_run48',
                  'CNTDIFF_run74',
                  'CNTDIFF_run76',
                  'CNTDIFF_run80',
                  'CNTDIFF_run68',
                  'CNTDIFF_run53',
                  'CNTDIFF_run70',
                  'CNTDIFF_run72',
                  'CNTDIFF_run50',
                  'CNTDIFF_run50',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'LOWER_BF_run02',
                  'LOW_BF_run02',
                  'LOWEST_BF_run02',
                  'LOWEST_BF_run04',
                  'LOWEST_BF_run06',
                  'LOWEST_BF_run08',
                  'LOWEST_BF_run12',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run42',
                  'CNTDIFF_run82',
                  'CNTDIFF_run42',
                  'LOWEST_BF_run02',
                  'CNTDIFF_run42',
                   ]

    expCodesNoC =['CNTDIFF',
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
                  'LOWER_BF',
                  'LOW_BF',
                  'LOWEST_BF',
                  'LOWEST_BF',
                  'LOWEST_BF',
                  'LOWEST_BF',
                  'LOWEST_BF',
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
                  'LOWEST_BF',
                  'CNTDIFF',
                  ]

    runNumsNoC  =['run42',
                  'run41',
                  'run40',
                  'run48',
                  'run74',
                  'run76',
                  'run80',
                  'run68',
                  'run53',
                  'run70',
                  'run72',
                  'run50',
                  'run50',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run02',
                  'run02',
                  'run02',
                  'run04',
                  'run06',
                  'run08',
                  'run12',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run42',
                  'run82',
                  'run42',
                  'run02',
                  'run42',
                  ]


 
    markersizes = [13,11,9,13,11,9,13,13,11,9,14,14,11,11,11,11,11,11,11,11,11,11,
                   11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,
                   11,11,11,11,11,11,11,11,11,11,11,11,11]
    markerstyles = ['o','o','o','d','d','d','p','p','p','p','^','^','^','^','^', 
                    '^','*','*','*','*','*','*','*','^','^','^','^','^','^','^',
                    '^','^','^','^','^','^','^','^',
                   '^','^','^','^','^','^','^','^','^','^','^','^','^','^','^','*','o', 'o','o']#'o']

    exp_labels = [  'base',#'$N_0$=5.5x10$^{-3}$,$\kappa$=10$^{-5}$,f=9.66x10$^{-5}$,U=0.34 m/s',
                    '$\kappa$=10$^{-4}$',
                    '$\kappa$=10$^{-3}$',
                    '$N_0$=6.3x10$^{-3}$',
                    '$N_0$=7.4x10$^{-3}$',
                    '$N_0$=4.5x10$^{-3}$',
                    '$N_0$=5.0x10$^{-3}$',
                    'f=1.0x$10^{-4}$',
                    'f=7.68x10$^{-5}$',
                    'f=8.6x10$^{-5}$',
                    'f=6.4x10$^{-5}$',
                    '$\kappa$=10$^{-3}$,$\kappa_{bg}$=10$^{-7}$',
                    '$\kappa$=10$^{-4}$,$\kappa_{bg}$=10$^{-7}$',
                    '$\kappa$=10$^{-3}$,$\kappa_{bg}$=10$^{-5}$',
                    '$\kappa$=10$^{-4}$,$\kappa_{bg}$=10$^{-5}$',
                    '$\kappa$=5x10$^{-3}$,$\kappa_{bg}$=10$^{-5}$',
                    '$\kappa$=10$^{-2}$,$\kappa_{bg}$=10$^{-5}$',
                    'U=0.296 m/s',
                    'U=0.243 m/s',
                    'U=0.124 m/s',
                    '$N_0$=4.5x10$^{-3}$',
                    '$N_0$=7.4x10$^{-3}$',
                    'f=7.0x$10^{-5}$',
                    '$\kappa$=10$^{-3}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$\kappa$=10$^{-5}$',
                    '$N$=4.7$^{-3}$',
                    'longer cny',
                    'longer cny, lowest u',
                    'longer2 cny',
                    ]


    colours = [ "emerald",#
                "tealish",
                "teal blue",# 
                'slate grey',
                'light grey',
                'steel',
                'grey',
                "navy blue",
                "blue",
                "light blue",
                'cerulean',
                "deep rose",
                "cherry red",
                "brown",
                "gold",
                'orchid',
                "tan",
                "dark red",
                'red',
                'light red',
                'light grey',
                'steel',
                'cerulean',
                'teal blue',
                'yellow',
                'gold',
                'light brown',
                'yellow',
                'gold',
                'light brown',
                'yellow',
                'gold',
                'light brown',
                'yellow',
                'gold',
                'light brown',
                'yellow',
                'gold',
                'light brown',
                'yellow',
                'gold',
                'light brown',
                'yellow',
                'gold',
                'light brown',
                'yellow',
                'gold',
                'light brown',
                'yellow',
                'gold',
                'light brown',
                'yellow',
                'gold',
                'light brown',
                'dull pink',
                'brown',
                'brown',
                'brown',
                ]# 


    Nos = np.array([5.5E-3,5.5E-3,5.5E-3,
                    6.3E-3,
                    7.4E-3,4.5E-3,5.0E-3,
                    5.5E-3,5.5E-3,5.5E-3,5.5E-3,
                    5.5E-3,5.5E-3,5.5E-3,5.5E-3,5.5E-3,5.5E-3,
                    5.5E-3,5.5E-3,5.5E-3,
                    4.5E-3,7.4E-3,
                    5.5E-3,5.5E-3,
                    5.5E-3,5.5E-3,5.5E-3,
                    5.5E-3,5.5E-3,5.5E-3,
                    5.5E-3,5.5E-3,5.5E-3,
                    5.5E-3,5.5E-3,5.5E-3,
                    5.5E-3,5.5E-3,5.5E-3,
                    5.5E-3,5.5E-3,5.5E-3,
                    5.5E-3,5.5E-3,5.5E-3,
                    5.5E-3,5.5E-3,5.5E-3,
                    5.5E-3,5.5E-3,5.5E-3,
                    5.5E-3,5.5E-3,5.5E-3,4.7E-3,5.5E-3,5.5E-3,5.5E-3,


                    ])

    fs = np.array([9.66E-5,9.66E-5,9.66E-5,
                   9.66E-5,9.66E-5,9.66E-5,9.66E-5,
                   1.0E-4,7.68E-5,
                   8.6E-5,6.4E-5,
                   9.66E-5,9.66E-5,9.66E-5,9.66E-5,9.66E-5,9.66E-5,
                   9.66E-5,9.66E-5,9.66E-5,
                   9.66E-5,9.66E-5,
                   7.0E-5,9.66E-5,
                   9.66E-5,9.66E-5,9.66E-5,
                   9.66E-5,9.66E-5,9.66E-5,
                   9.66E-5,9.66E-5,9.66E-5,
                   9.66E-5,9.66E-5,9.66E-5,
                   9.66E-5,9.66E-5,9.66E-5,
                   9.66E-5,9.66E-5,9.66E-5,
                   9.66E-5,9.66E-5,9.66E-5,
                   9.66E-5,9.66E-5,9.66E-5,
                   9.66E-5,9.66E-5,9.66E-5,
                   9.66E-5,9.66E-5,9.66E-5,9.66E-5,9.66E-5,9.66E-5,9.66E-5,
                   ])

    Us = np.array([0.360,0.360,0.360,
                   0.360,0.360,0.360,0.360,#0.358,0.358,
                   0.360,0.360,0.360,0.360,#0.358,
                   0.360,0.360,0.360,0.360,0.360,0.360,
                   0.309,0.256,
                   0.134,
                   0.134,0.134,
                   0.134,0.134,
                   0.370,0.370,0.370,
                   0.370,0.370,0.370,
                   0.370,0.370,0.370,
                   0.370,0.370,0.370,
                   0.370,0.370,0.370,
                   0.370,0.370,0.370,
                   0.370,0.370,0.370,
                   0.370,0.370,0.370,
                   0.370,0.370,0.370,
                   0.370,0.370,0.370,0.370,0.370,0.134,0.370,
                   ])

    Kvs = np.array([1E-5,1E-4,1E-3,
                    1E-5,1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,1E-5,
                    1E-3,1E-4,1E-3,1E-4,5E-3,1E-2,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,
                    1E-5,1E-3,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,1E-5,1E-5,1E-5,1E-5,
                    ])

    Kbg = np.array([1E-5,1E-4,1E-3,
                    1E-5,1E-5,1E-5,1E-5,#1E-5,1E-5,
                    1E-5,1E-5,1E-5,1E-5,#1E-5,
                    1E-7,1E-7,1E-5,1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,
                    1E-5,1E-3,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,1E-5,1E-5,1E-5,1E-5,
                    ])




    # Fill the fields of the records
    for record,expName,expCode,runNum,No,fo,uo,kvo,kbgo,col,explabel,marksize,markstyle in zip(
        recordsNoC,expNamesNoC,expCodesNoC,runNumsNoC,Nos,fs,Us,Kvs,Kbg,colours,exp_labels,markersizes,markerstyles):
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
        record.kbg = kbgo

    return(recordsNoC)
