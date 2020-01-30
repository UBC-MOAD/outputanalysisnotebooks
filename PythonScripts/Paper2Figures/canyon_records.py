# This script sets up the records for all canyon runs
# Just run as: python canyon_records.py

# ------------------------------------------------------------
import numpy as np

def main():
    class run:
        pass

    #Define all runs, create empty run records
    base = run()
    argo = run()
    kv01 = run()
    kv02 = run()
    kv03 = run()
    kv04 = run()
    
    records = [base,
               argo,
               kv01,
               kv02,
               kv03,
               kv04,
               ] 

    expNames = ['base',
               'argo',
               'kv01',
               'kv02',
               'kv03',
               'kv04',
               ]

    paperNames = [
                'Base',
                'ARGO',
                'highest\_Kv_step',
                'highest\_Kv_$\epsilon$25',
                'high\_Kv_step',
                'high\_Kv_$\epsilon$25',
                ]


    expCodes = ['UPW_10TR_BF2_AST',
                'UPW_10TR_BF2_AST',
                'UPW_10TR_BF2_KV3D_AST',
                'UPW_10TR_BF2_KV3D_AST',
                'UPW_10TR_BF2_KV3D_AST',
                'UPW_10TR_BF2_KV3D_AST',
                ]

    runNums  = ['01_Ast03',
                '02_Ast03_NoCny',
                '01_eps5_kv1E-2',
                '02_eps25_kv1E-2',
                '03_eps5_kv5E-3',
                '04_eps25_kv5E-3',
               ]


    markersizes = [11,11,11,11,11,11]
    markerstyles = ['o','^','d','v','D','*']
                  
    exp_labels = ['Base',
                  'ARGO',
                  'highest\_Kv_step',
                  'highest\_Kv_$\epsilon$25',
                  'high\_Kv_step',
                  'high\_Kv_$\epsilon$25',
                  ]

    colours = ['black',#
                'silver',
                'cerulean',
                'kelly green',
                'pastel orange',
                'turquoise',
                ]# 


    Nos = np.array([0.0055, 
                    0.0099,  
                    0.0055 , 
                    0.0055 , 
                    0.0055 , 
                    0.0055 , 
                    ])

    fs = np.array([1E-4,
                   1.08E-4,
                   1E-4,
                   1E-4,
                   1E-4,
                   1E-4,
                   ])

    Us = np.array([0.3,0.329,0.269,0.268,0.269,0.268])

    Kvs = np.array([1E-5,1E-5,1E-2,1E-2,5E-3,5E-5])
  
    Kbg = np.array([1E-5,1E-5,1E-5,1E-5,1E-5,1E-5])

    epsilon = np.array([5,5,5,25,5,25])
    
    Hhs = np.array([97.5,97.5,97.5,97.5,97.5,97.5]) 
    
    Hinds = np.array([20,20,20,20,20,20])
            
    Hrs = np.array([120,120,120,120,120,120])
    
    Ls = np.array([21800,21800,21800,21800,21800,21800]) 
    
    Rs = np.array([4500,4500,4500,4500,4500,4500])
    
    Wisos = np.array([8900,8900,8900,8900,8900,8900])
   
    # Fill the fields of the records
    for record,expName,paperName,expCode,runNum,No,fo,uo,kvo,kbgo,col,explabel,marksize,markstyle, eps, Hh, Hr, L ,R, Wiso, Hind in zip(records,expNames,paperNames,expCodes,runNums,Nos,fs,Us,Kvs,Kbg,colours,exp_labels,                                                                                                                            markersizes,markerstyles, epsilon, Hhs,Hrs,Ls, Rs, Wisos, Hinds):
        record.name = expName
        record.paperName = paperName        
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
        record.epsilon = eps
        record.L = L
        record.Hh = Hh
        record.Hr = Hr
        record.R = R
        record.Wiso = Wiso
        record.Hind = Hind
      
    return(records)