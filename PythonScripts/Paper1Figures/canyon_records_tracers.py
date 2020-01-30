# This script sets up the records for all canyon runs
# Just run as: python canyon_records.py

# ------------------------------------------------------------
import numpy as np

def main():
    class run:
        pass

    #Define all runs, create empty run records
    BARKLEY_II_run01=run()
    PARAB_run01=run()
 
    records =   [BARKLEY_II_run01,
	             PARAB_run01] 

    expNames = ['BARKLEY_II_run01',
	        'PARAB_run01']

    expCodes = ['BARKLEY_II',
                'CNTDIFF_LOW_SR_7Tr']

    runNums  = ['run01',
                'run01',
                ]
    tracerLists = [['Tr01','Tr02','Tr03','Tr04','Tr05','Tr06','Tr07','Tr08','Tr09','Tr10'],
		   ['Tr1','Tr2','Tr3','Tr4','Tr5','Tr6','Tr7']]
    
    markerstyles = ['o','d']

   
    exp_labels = ['Barkley',
                  'Parabolic profiles',
                 ]
    
    tracerLabels = [['Lin','Sal','Oxy','Nit','Sil','Pho','NOx','Met','Alk', 'DIC'],
		           ['Tr1','Tr2','Tr3','Tr4','Tr5','Tr6','Tr7']]
    
  
    colours = [['purple','blue','green','gold','orange','red','orchid','teal','tan', 'olive'],
	          ['0.1','0.2','0.3','0.4','0.5','0.6','0.7']] 

  
    Nos = np.array([5.5E-3,5.5E-3,
                    ])

    fs = np.array([9.66E-5,9.66E-5,
                  ])

    Us = np.array([0.35,0.35,0.35,
                  ])

    Kvs = np.array([1E-5,1E-5,
                    ])
    Kbg = np.array([1E-5,1E-5,
                    ])




    # Fill the fields of the records
    for record,expName,expCode,runNum,No,fo,uo,kvo,kbgo,col,tracerList,tracerLabel,explabel,markstyle in zip(records,expNames,
                                                                                           expCodes,runNums,
                                                                                           Nos,fs,Us,Kvs,Kbg,
                                                                                           colours,tracerLists,tracerLabels,
                                                                                           exp_labels,
                                                                                           markerstyles):
        record.name = expName
        record.exp_code = expCode
        record.run_num = runNum
        record.label = explabel
        record.color = col
        record.tracerList = tracerList
        record.tracerLabel = tracerLabel
        record.mstyle = markstyle
        record.N = No
        record.f = fo
        record.u = uo
        record.kv = kvo
        record.kbg = kbgo

    return(records)