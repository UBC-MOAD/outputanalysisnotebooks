# This script sets up the records for all canyon runs
# Just run as: python canyon_records.py

# ------------------------------------------------------------
import numpy as np

def main():
    class run:
        pass

    #Define all runs, create empty run records
    CNTDIFF_run38 = run()  
    CNTDIFF_run37 = run() 
 
    records =   [CNTDIFF_run38,CNTDIFF_run37
                ] 

    expNames = ['CNTDIFF_run38','CNTDIFF_run37'
                ]

    expCodes = ['CNTDIFF_n','CNTDIFF_n'
               ]

    runNums  = ['run38','run37'
                ]


    markersizes = [13,13]
    markerstyles = ['o','o']

    exp_labels = [ 'base','kv 1E-4'
                 ]
    
    
    exp_labels2 = [ 'base', 'kv 1E-4'
                  ]
    colours = ['kelley green','green'
               ]# 

    colours2 = ["kelley green", 'green'
               ]# 


    Nos = np.array([5.5E-3, 5.5E-3])

    fs = np.array([9.66E-5, 9.66E-5])

    Us = np.array([0.370, 0.370])

    Kvs = np.array([1E-5,1E-4])
    Kbg = np.array([1E-5, 1E-4])




    # Fill the fields of the records
    for record,expName,expCode,runNum,No,fo,uo,kvo,kbgo,col,col2,lab2,explabel,marksize,markstyle in zip(records,expNames,
                                                                                           expCodes,runNums,
                                                                                           Nos,fs,Us,Kvs,Kbg,
                                                                                           colours,colours2,exp_labels2,
                                                                                           exp_labels,
                                                                                           markersizes,markerstyles):
        record.name = expName
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
        record.kv = kvo
        record.kbg = kbgo

    return(records)