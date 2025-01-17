# This script sets up the records for all canyon runs
# Just run as: python canyon_records.py

# ------------------------------------------------------------
import numpy as np

def main():
    class run:
        pass

    #Define all runs, create empty run records
    CNTDIFF_run42 = run()  
    CNTDIFF_run41 = run()
 
    records =   [CNTDIFF_run42,CNTDIFF_run41]

    expNames = ['CNTDIFF_run42','CNTDIFF_run41'
                ]

    expCodes = ['CNTDIFF_n','CNTDIFF_n'
               ]

    runNums  = [
                'run42','run41'
                ]


    markersizes = [13,13]
    markerstyles = ['o','o']

    exp_labels = [ 'base nc','1E-4 nc'
                 ]
    
    
    exp_labels2 = [  'base nc','1E-4 nc'
                  ]
    colours = ['kelley green', 'green'
               ]# 

    colours2 = ["kelley green", 'green'
               ]# 


    Nos = np.array([5.5E-3, 5.5E-3])

    fs = np.array([9.66E-5, 9.66E-5])

    Us = np.array([0.370, 0.370])

    Kvs = np.array([1E-5, 1E-4])
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