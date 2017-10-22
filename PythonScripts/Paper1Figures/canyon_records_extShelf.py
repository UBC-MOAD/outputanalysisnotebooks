# This script sets up the records for all canyon runs
# Just run as: python canyon_records.py

# ------------------------------------------------------------
import numpy as np

def main():
    class run:
        pass

    #Define all runs, create empty run records
    CNTDIFF_Ext2x = run()  
   
 
    records =   [CNTDIFF_Ext2x
                ] 

    expNames = ['CNTDIFF_Ext2x_run01'
                ]

    expCodes = ['CNTDIFF_EXT_SHELF'
               ]

    runNums  = ['run01'
                ]


    markersizes = [13]
    markerstyles = ['o']

    exp_labels = [ 'ext 2x',
                 ]
    
    
    exp_labels2 = [ 'ext 2x'
                  ]
    colours = ['kelley green'
               ]# 

    colours2 = ["kelley green"
               ]# 


    Nos = np.array([5.5E-3])

    fs = np.array([9.66E-5])

    Us = np.array([0.358])

    Kvs = np.array([1E-5])
    Kbg = np.array([1E-5])




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