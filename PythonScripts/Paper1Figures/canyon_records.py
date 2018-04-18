# This script sets up the records for all canyon runs
# Just run as: python canyon_records.py

# ------------------------------------------------------------
import numpy as np

def main():
    class run:
        pass

    #Define all runs, create empty run records
    CNTDIFF_base = run()
    CNTDIFF_kv4 = run()
    CNTDIFF_kv3= run()
    CNTDIFF_N63 = run()
    CNTDIFF_N74 = run()
    CNTDIFF_N45 = run()
    CNTDIFF_f100 = run()
    CNTDIFF_f76 = run()
    CNTDIFF_f86 = run()
    CNTDIFF_f64 = run()
    VISC3D_run01 = run()
    VISC3D_run02 = run()
    VISC3D_run03 = run()
    VISC3D_run04 = run()
    VISC3D_run06 = run()
    LOWER_BF_u32 = run()
    LOW_BF_u26 = run()
    LOWEST_BF_u13 = run()
    LOWEST_BF_N45 = run()
    LOWEST_BF_N74 = run()
    LOWEST_BF_f70 = run()
    LOWEST_BF_kv3 = run()
    VISC3D_run05 = run()
    REALKV_MTY_bot = run()
    REALKV_EEL_bot = run()
    REALKV_MTY_rim = run()
    REALKV_EEL_rim = run()
    REALKV_ASC_bot = run()
    REALKV_ASC_rim = run()
    
 
    records =   [
                CNTDIFF_base, 
	            CNTDIFF_kv4, 
                CNTDIFF_kv3,
                CNTDIFF_N63, 
                CNTDIFF_N74,
                CNTDIFF_N45,
                CNTDIFF_f100,
                CNTDIFF_f76,
                CNTDIFF_f86,
                CNTDIFF_f64,
                VISC3D_run01,
                VISC3D_run02,
                VISC3D_run04,
                VISC3D_run03,
                VISC3D_run05,
                VISC3D_run06,
                LOWER_BF_u32,
                LOW_BF_u26,
                LOWEST_BF_u13,
                LOWEST_BF_N45,
                LOWEST_BF_N74, 
                LOWEST_BF_f70,
                LOWEST_BF_kv3,
                REALKV_MTY_bot,
                REALKV_EEL_bot,
                REALKV_MTY_rim,
                REALKV_EEL_rim,
                REALKV_ASC_bot,
                REALKV_ASC_rim,
                ] 

    expNames = [
                'CNTDIFF_run38',
                'CNTDIFF_run37',
                'CNTDIFF_run36',
                'CNTDIFF_run45',
                'CNTDIFF_run73',
                'CNTDIFF_run75',
                'CNTDIFF_run67',
                'CNTDIFF_run51',
                'CNTDIFF_run69',
                'CNTDIFF_run71',
                '3DVISC_run01',
                '3DVISC_run02',
                '3DVISC_run04',
                '3DVISC_run03',
                '3DVISC_run05',
                '3DVISC_run06',
                'LOWER_BF_run01',
                'LOW_BF_run01',
                'LOWEST_BF_run01',
                'LOWEST_BF_run03',
                'LOWEST_BF_run05',
                'LOWEST_BF_run07',
                'LOWEST_BF_run11',
                '3DVISC_REALISTIC_run01' ,
                '3DVISC_REALISTIC_run02' ,
                '3DVISC_REALISTIC_run03' ,
                '3DVISC_REALISTIC_run04',
                '3DVISC_REALISTIC_run05',
                '3DVISC_REALISTIC_run06',
                ]

    paperNames = [
                'Base',
                'higher\_Kbg',
                'highest\_Kbg',
                'higher\_N',
                'highest\_N',
                'lower\_N',
                'higher\_f',
                'low\_f',
                'lower\_f',
                'lowest\_f',
                'highestKc\_lowKbg',
                'higherKc\_lowKbg',
                'higher\_Kc',
                'high\_Kc',
                'high2\_Kc',
                'highest\_Kc',
                'low\_U',
                'lower\_U',
                'lowest\_U',
                'lowestU\_lowestN',
                'lowestU\_highestN',
                'lowestU\_lowestf',
                'lowestU\_highestKbg',
                'realKv_Mty',
                'realKv_Eel',
                'realKv_Mty_rim',
                'realKv_Eel_rim',
                'realKv_Asc',
                'realKv_Asc_rim',
                ]


    expCodes = ['CNTDIFF',
                'CNTDIFF',
                'CNTDIFF',
                'CNTDIFF',
                'CNTDIFF',
                'CNTDIFF',
                'CNTDIFF',
                'CNTDIFF',
                'CNTDIFF',
                'CNTDIFF',
                '3DVISC',
                '3DVISC',
                '3DVISC',
                '3DVISC',
                '3DVISC',
                '3DVISC',
                'LOWER_BF',
                'LOW_BF',
                'LOWEST_BF',
                'LOWEST_BF',
                'LOWEST_BF',
                'LOWEST_BF',
                'LOWEST_BF',
                '3DVISC_REALISTIC',
                '3DVISC_REALISTIC',
                '3DVISC_REALISTIC',
                '3DVISC_REALISTIC',
                '3DVISC_REALISTIC',
                '3DVISC_REALISTIC',
                ]

    runNums  = ['run38',
                'run37',
                'run36',
                'run45',
                'run73',
                'run75',
                'run67',
                'run51',
                'run69',
                'run71',
                'run01',
                'run02',
                'run04',
                'run03',
                'run05',
                'run06',
                'run01',
                'run01',
                'run01',
                'run03',
                'run05',
                'run07',
                'run11',
                'run01',
                'run02',
                'run03',
                'run04',
                'run05',
                'run06',
                ]


    markersizes = [13,11,9,13,11,9,13,13,11,9,14,14,11,11,11,11,11,11,11,11,11,11,
                   11,11,11,11, 11,11,11]
    markerstyles = ['o','^','d','^','d','v','^','v','*','P','v','*','d','^','D',
                    'p','v','*','*','d','P','D','p','D','d','^','v','*','P']

    exp_labels = [  #'$\kappa$=10$^{-7}$',
                    'base',#'$N_0$=5.5x10$^{-3}$,$\kappa$=10$^{-5}$,f=9.66x10$^{-5}$,U=0.34 m/s',
                    'higher $\kappa_{bg}$',
                    'highest $\kappa_{bg}$',
                    'higher $N$',
                    #'$N_0$=3.9x10$^{-3}$',
                    #'$N_0$=3.0x10$^{-3}$',
                    'highest $N$',
                    'lower $N$',
                    'higher $f$',
                    'lower $f$',
                    #'f=4.84x10$^{-5}$',
                    'low $f$',
                    'lowest $f$',
                    'high $\kappa_{can}$, lower $\kappa_{bg}$',
                    'higher $\kappa_{can}$, lower $\kappa_{bg}$',
                    'higher $\kappa_{can}$',
                    'high $\kappa_{can}$',
                    'high2 $\kappa_{can}$',
                    'highest $\kappa_{can}$',
                    'lower $U$',
                    'low $U$',
                    'lowest $U$',
                    'lowest $U$, lowest $N$',
                    'lowest $U$, highest $N$',
                    'lowest $U$, lowest $f$',
                    'lowest $U$, highest $\kappa_{bg}$',
                    '$\kappa_{can}$ Mty, bottom',
                    '$\kappa_{can}$ Eel, bottom',
                    '$\kappa_{can}$ Mty, rim',
                    '$\kappa_{can}$ Eel, rim',
                    '$\kappa_{can}$ Asc, bottom',
                    '$\kappa_{can}$ Asc, rim',
                    ]
    
    
    exp_labels2 = [  'base case',
                    r'$\uparrow$ $\kappa_{bg}$',
                    r'$\Uparrow$ $\kappa_{bg}$',
                    r'$\uparrow$ $N_0$',
                    r'$\Uparrow$ $N_0$',
                    r'$\downarrow$ $N_0$',
                    r'$\uparrow$ $f$',
                    r'$\Downarrow$ $f$',
                    r'$\downarrow$ $f$',
                    r'$\Downarrow \Downarrow$ $f$',
                    r'$\Uparrow$ $\kappa_{can}$,$\downarrow$$\kappa_{bg}$',
                    r'$\uparrow$ $\kappa_{can}$,$\downarrow$$\kappa_{bg}$',
                    r'$\uparrow \uparrow$  $\kappa_{can}$',
                    r'$\Uparrow$ $\kappa_{can}$',
                    r'$\uparrow$ $\kappa_{can}$',
                    r'$\Uparrow \Uparrow$  $\kappa_{can}$',
                    r'$\downarrow$ U',
                    r'$\downarrow \downarrow$ U',
                    r'$\Downarrow$ U',
                    r'$\Downarrow$ U', 
                    r'$\Downarrow$ U, $\Downarrow$ $N_0$',
                    r'$\Downarrow$ U, $\Uparrow$ $N_0$',
                    r'$\Downarrow$ U, $\Downarrow$ $f$',
                    r'$\Downarrow$ U, $\Uparrow \kappa_{can}$',
                    r'$\kappa_{can}$ Mty, bottom',
                    r'$\kappa_{can}$ Eel, bottom',
                    r'$\kappa_{can}$ Mty, rim',
                    r'$\kappa_{can}$ Eel, rim',
                    r'$\kappa_{can}$ Asc, bottom',
                    r'$\kappa_{can}$ Asc, rim',
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
                'orchid',
                "tan",
                "red",
                'dark red',
                'burgundy',
                'light grey',
                'steel',
                'cerulean',
                'teal blue',
                'olive',
                'olive',
                'olive',
                'olive',
                'olive',
                'olive',
                ]# 

    colours2 = ["black",#
                "silver",
                "slate grey",# 
                "magenta",
                'magenta',
                'magenta',
                "light eggplant", 
                "light eggplant",
                "light eggplant",
                "light eggplant", 
                "apple",
                "apple",
                "apple",
                "apple",
                "apple",
                "apple",
                'pale red',
                'pale red',
                'pale red',
                'pastel orange',
                'pastel orange',
                'pastel orange',
                'pastel orange',
                'french blue',
                'french blue',
                'bright sky blue',
                'bright sky blue',
                'french blue',
                'bright sky blue',
                ]# 


    Nos = np.array([0.0055, 
                    0.0055,  
                    0.0055 , 
                    0.0063 , 
                    0.0074 , 
                    0.0046 , 
                    0.0055 , 
                    0.0055 , 
                    0.0055 , 
                    0.0055 , 
                    0.0055 , 
                    0.0055 , 
                    0.0055 , 
                    0.0055 , 
                    0.0055 , 
                    0.0055 , 
                    0.0055 , 
                    0.0055 , 
                    0.0055 , 
                    0.0046 , 
                    0.0074 , 
                    0.0055 , 
                    0.0055 , 
                    0.0055 ,
                    0.0055 ,
                    0.0055 ,
                    0.0055 ,
                    0.0055 ,
                    0.0055 ,
                    ])

    fs = np.array([9.66E-5,9.66E-5,9.66E-5,
                   9.66E-5,9.66E-5,9.66E-5,#9.66E-5,9.66E-5,
                   1.0E-4,7.68E-5,#4.84E-5,
                   8.6E-5,6.4E-5,
                   9.66E-5,9.66E-5,9.66E-5,9.66E-5,9.66E-5,9.66E-5,
                   9.66E-5,9.66E-5,9.66E-5,
                   9.66E-5,9.66E-5,
                   7.0E-5,9.66E-5,
                   #9.66E-5,9.66E-5
                   9.66E-5,9.66E-5,9.66E-5,
                   9.66E-5,9.66E-5,9.66E-5,
                   ])

    Us = np.array([0.360,0.360,0.360,
                   0.360,0.360,0.360,#0.358,0.358,
                   0.360,0.360,0.360,0.360,#0.358,
                   0.360,0.360,0.360,0.360,0.360,0.360,
                   0.309,0.256,
                   0.134,
                   0.134,0.134,
                   0.134,0.134,
                   #0.370,#0.370,
                   0.360, 0.360, 0.360,
                   0.360, 0.360, 0.360,
                   ])

    Us_model = np.array([0.360,
                         0.357, 
                         0.320,
                         0.375,
                         0.394,
                         0.342,
                         0.356,
                         0.387,
                         0.374,
                         0.406,
                         0.352,
                         0.356,
                         0.357,
                         0.352,
                         0.345,
                         0.345,
                         0.309,
                         0.256,
                         0.134,
                         0.129,
                         0.145,
                         0.145,
                         0.113,
                         0.360,0.360,0.360,
                         0.360,0.360,0.360])

    Us_HA = np.array([0.364,   
                      0.361,
                      0.321 ,
                      0.379 ,
                      0.399 ,
                      0.344 ,
                      0.359 ,
                      0.392 ,
                      0.378 ,
                      0.414 ,
                      0.354 ,
                      0.359 ,
                      0.359 , 
                      0.354 ,
                      0.346 ,
                      0.347 ,
                      0.312 , 
                      0.258 ,
                      0.137 , 
                      0.132 , 
                      0.153 , 
                      0.150 ,  
                      0.114 ,
                      0.364,0.364,0.364,
                      0.364,0.364,0.364])

    Kvs = np.array([1E-5,1E-4,1E-3,
                    1E-5,1E-5,1E-5,#1E-5,1E-5,
                    1E-5,1E-5,1E-5,1E-5,#1E-5,
                    1E-3,1E-4,1E-4,1E-3,5E-3,1E-2,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,
                    1E-5,1E-3,
                    #1E-5,#1E-5,
                    2.54E-3,9.40E-4,6.63E-4,
                    8.25E-5,4.41E-3,4.73E-3,
                    ])
    Kbg = np.array([1E-5,1E-4,1E-3,
                    1E-5,1E-5,1E-5,#1E-5,1E-5,
                    1E-5,1E-5,1E-5,1E-5,#1E-5,
                    1E-7,1E-7,1E-5,1E-5,1E-5,1E-5,
                    1E-5,1E-5,1E-5,
                    1E-5,1E-5,
                    1E-5,1E-3,
                    #1E-5, #1E-5
                    1.11E-3,8.04E-5,3.79E-4,
                    1.04E-5,2.19E-3,1.70E-3,
                    ])




    # Fill the fields of the records
    for record,expName,paperName,expCode,runNum,No,fo,uo,um,uha,kvo,kbgo,col,col2,lab2,explabel,marksize,markstyle in    zip(records,expNames,paperNames,expCodes,runNums,Nos,fs,Us,Us_model,Us_HA,Kvs,Kbg,colours,colours2,exp_labels2,exp_labels,
                                                                                           markersizes,markerstyles):
        record.name = expName
        record.paperName = paperName        
        record.exp_code = expCode
        record.run_num = runNum
        record.label = explabel
        record.color = col
        record.color2 = col2
        record.label2 = lab2
        record.msize = marksize
        record.mstyle = markstyle
        record.N = No
        record.f = fo
        record.u = uo
        record.u_mod = um
        record.u_ha = uha
        record.kv = kvo
        record.kbg = kbgo

    return(records)