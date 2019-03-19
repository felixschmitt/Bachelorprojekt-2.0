# -*- coding: utf-8 -*-
"""
Created on Sun Dec 09 17:17:11 2018

@author: Leon
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
#from psychopy.misc import fromFile
#from psychopy import data
import pandas as pd
import matplotlib.pyplot as plt
import sys 
import os 
import struct
import numpy as np
import scipy
import math
from scipy.misc import logsumexp
import psignifit as ps



nameVpn = "JO14BA"



#_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
#filename_trial = _thisDir + os.sep + u'data/acker/trialdata1.psydat'
#datFile = fromFile(filename_trial)
##get info (added when the handler was created)
#print (datFile.extraInfo)
##get data
##print (datFile._getAllParamNames())
#print (datFile.data['response'])
##datFile.getExp()
##print (datFile.getAllEntries())
##get list of conditions
#conditions = datFile.trialList
##for condN, condition in enumerate(conditions):
##    print condition, datFile.data['response'][condN], numpy.mean(datFile.data['response'][condN])
##print(conditions)
#print(datFile.getExp())


##### Experimenthandler 
#_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
#filename_trial = _thisDir + os.sep + u'data/acker/Yes-No Task_2018_Dec_11_1409.psydat'
#filename_for_panda = _thisDir + os.sep + u'data/acker/Yes-No Task_2018_Dec_11_1409'
#datFile = fromFile(filename_trial)
#
##print (datFile.extraInfo)
#print (datFile.dataFileName)
#print (datFile.dataNames)
#print (datFile.entries[1][u'response'])

######### Panda ##########
### getting path
#_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
_thisDir = os.path.dirname(os.path.abspath(__file__))
#filename_for_panda = _thisDir + os.sep + r'data\acker\Yes-No Task_2018_Dec_11_1409.csv'
#filename_for_panda_to_extend = _thisDir + os.sep + r'data\jolle\Yes-No Task_2018_Dec_11_1527.csv'
#df = pd.read_csv(filename_for_panda)
#print (df)
#### Plott numerical data
#df['signal_intensity'].plot()
def createListOfAllFilesInDic ():

    #### Automatically find all dataframes and put the name in FileNames
    
    # List to hold file names
    FileNames = []
    
    # Your path will be different, please modify the path below.
    os.chdir(_thisDir + os.sep + r'data')
    
    # Find any file that ends with ".xlsx"
    for files in os.listdir("."):
        if files.endswith(".csv"):
            FileNames.append(files)
            
    return FileNames

#print FileNames

#### Funktioniert 


# get all Files in Given Dictonary
def GetFile(file_name):

    # Path to excel file
    # Your path will be different, please modify the path below.
    location = _thisDir + os.sep + r'data/' + file_name
    # Parse the excel file
    # 0 = first sheet
    df = pd.read_csv(location)
    
    # Tag record to file name
    df['File'] = file_name
    
    # Make the "File" column the index of the df
    return df.set_index(['File'])

#FileNames=createListOfAllFilesInDic() 
#
## Create a list of dataframes
#df_list = [GetFile(fname) for fname in FileNames]
#
## Combine all of the dataframes into one
#big_df = pd.concat(df_list)
#
## delet whatever is unnecessary
#del big_df['trials.thisTrialN']
#del big_df['trials.thisN']
#del big_df['trials.thisIndex']
##print (big_df)
#
##creating a subdata set 
#subData = big_df.loc[big_df['expName'] == "Yes-No Task"]
#
#
## diagram
##big_df.response.value_counts().plot(kind='barh')
#
##save the data to csv
#
###### creat subset !!!!!!!!!!!!!!!
#
#big_df.to_csv('BigData.csv', index=False)
#subData.to_csv('DataYesNo.csv', index=False)

###############

    ## and plot
def create_subdataset_for_participant (name):
    
    participant_data = subData.loc[subData['participant'] == name]
#    participant_data = participant_data.loc[participant_data['session'] == 2 ]
    
    return participant_data

def create_subdataset_for_participant2IFC (name):
    
    participant_data2IFC = subData2IFC.loc[subData2IFC['participant'] == name]
    participant_data2IFC = participant_data2IFC.loc[participant_data2IFC['session'] == 2 ]
    
    return participant_data2IFC
    ########## search for the signal Intensitys
    ########## calculate the propability of a correct answer for each signal Intesnity
    ########## Plots the Data-Points
    ########## Plots a Fiting curve
    
    
def evaluationAndPlot2IFC (dataPlot):
    list_of_intensitys = dataPlot['signal_intensity'].value_counts().index.tolist()

    correct_fit = []
    n_total_fit = []
#    listRelHit = []
#    listRelFalseA = []
#    listNGes = []
    for x in list_of_intensitys:
#        relTwoHit = 0
#        relTwoFalseA = 0
#        other = 0
        dataframe_signalintensity = dataPlot[dataPlot['signal_intensity'] == x]
        dataStimOnOne    = dataframe_signalintensity[dataframe_signalintensity['signal_on_stimuluspos1'] == True]
        dataHit = dataStimOnOne[dataStimOnOne['response'] == 'correct answer']
        dataMiss = dataStimOnOne[dataStimOnOne['response'] == 'wrong answer']
        
        dataNoStim = dataframe_signalintensity[dataframe_signalintensity['signal_on_stimuluspos1'] == False]
        dataCorrectRejection = dataNoStim[dataNoStim['response'] == 'correct answer']
        dataFalseAlarm =dataNoStim[dataNoStim['response'] == 'wrong answer']
        correct_fit.append(dataHit.shape[0] + dataCorrectRejection.shape[0])
        n_total_fit.append(dataCorrectRejection.shape[0] + dataFalseAlarm.shape[0] + dataHit.shape[0] + dataMiss.shape[0])
        print(dataHit.shape[0])
        print(dataCorrectRejection.shape[0])

        
    data2IFC = np.empty([len(list_of_intensitys),3], dtype=float)

    sorted_ar = np.array(list_of_intensitys)
    #### data for fit
    correct_psyfit = np.array(correct_fit)
    n_total_psyfit = np.array(n_total_fit)
    o=0
    
    for k in sorted_ar:
        
        
        data2IFC[o][0] = sorted_ar[o]
        data2IFC[o][1] = correct_psyfit[o]
        data2IFC[o][2] = n_total_psyfit[o]
#        print (data[o][0])
#        print (data[o][1])
#        print (data[o][2])
        o = o+1
    return (data2IFC)
        
def evaluationAndPlot (givenData):
    
    
    count=[]
    correct_fit = []
    n_total_fit = []
    o = 0
#    print(dataframe_signalintensity.groupby('response').size())
    i=0
#    print("hier")
    list_of_intensitys = givenData['signal_intensity'].value_counts().index.tolist()
    ## sortiere in Aufsteigender reihenfolge
    sortiert = np.sort(list_of_intensitys, axis=None)     # sort the flattened array
    for x in sortiert:
        correct = 0
        wrong = 0
        dataframe_signalintensity = givenData[givenData['signal_intensity'] == x]
        answers = dataframe_signalintensity.groupby('response').size()
        answerOptions = dataframe_signalintensity['response'].value_counts().index.tolist()
#        dataframe_signalintensity.groupby('response').size()
        for y in answerOptions:
            
            if y == "Hit" :
                correct = correct + answers['Hit']
            if y == "False Alarm":
                wrong = wrong + answers['False Alarm']
            if y == "Correct Rejection":
                correct = correct + answers['Correct Rejection']
            if y == "Miss":
                wrong = wrong + answers['Miss']
            if y == "No Answer" :
                wrong = wrong + answers['No Answer']
                ##### for fit 
            if y == "correct answer" :
                correct = correct + answers['correct answer']
            if y == "wrong answer" :
                wrong = wrong + answers['wrong answer']

            
        correct_fit.append(correct)
        n_total_fit.append(correct + wrong)

        count.append(float(correct) / float(correct + wrong))
        i = i+1
        
    data = np.empty([len(sortiert),3], dtype=float)
    
#    D = np.array(count)
    sorted_ar = np.array(sortiert)
    #### data for fit
    correct_psyfit = np.array(correct_fit)
    n_total_psyfit = np.array(n_total_fit)
    
    
    for k in sorted_ar:
        
        
        data[o][0] = sorted_ar[o]
        data[o][1] = correct_psyfit[o]
        data[o][2] = n_total_psyfit[o]
#        print (data[o][0])
#        print (data[o][1])
#        print (data[o][2])
        o = o+1
    

    
#    options             = dict() 
##    options['sigmoidName'] = 'weibull'   # choose a cumulative Gauss as the sigmoid  
#    options['expType']     = 'nAFC'   # choose 2-AFC as the experiment type  
##    options['plotAsymptote']  = False
#    options['expN']          = 2                       # this sets the guessing rate to .5 (fixed)
##    options['threshPC'] = 0.75
##    options['cuts']= 0.75
##    options[''] = 0.5
##    options['CImethod'] = 'stripes'
##    options['betaPrior'] = 10
#    
#    
#    ## options borders threshold,width,upper asymptote,lower asymptote,variance, scale
##    options['borders'] = np.array([[1,2],[0.05,5],[0.05,0.05], [.1,0.95],[0.2,.2]],dtype=float)
##    options['borders'] = np.array([[1,12],[0.05,2],[0.05,0.3], [.1,0.95],[0.2,.2]],dtype=float)
##    options['borders'] = np.array([[1,12],[0.05,2],[0.1,0.45], [.1,0.95],[0.6,.2]],dtype=float)
##    options['borders'] = np.array([[1,2],[0.05,5],[0.05,0.005], [0,0.5],[0.6,.2]],dtype=float)
#    
#
#    print ("ready1")
##    options['maxBorderValue']= 0.05
##    options['setBordersType']= 0.5
##    options['instantPlot'] = True
#
#    
##    options['moveBorders'] = 0
#    result = ps.psignifit(data)
##    result.round(2)
#    print ("ready2")
#    result['Fit']
#
#    result['conf_Intervals']
#    print ("ready3")
    
#    ps.psigniplot.plotPsych(result)
    return (data)
 ##############
####################    
#by the √2 rule d'2AFC = √2 d'Yes/No
def calc2AFCSuggestion (dataPerson):
    list_of_intensitys = dataPerson['signal_intensity'].value_counts().index.tolist()
    
    listRelHit = []
    listRelFalseA = []
    listNCoFa = []
    listNHiMi = []
    listIntensitys = []
    smaltoBig = np.sort(list_of_intensitys, axis=None)
    suggestionData = np.empty([len(list_of_intensitys),3], dtype=float)
    for x in smaltoBig:
        relHit = 0
        relFalseA = 0
        other = 0
        NCo = 0
        NMi = 0
        dataframe_signalintensity = dataPerson[dataPerson['signal_intensity'] == x]
        answers = dataframe_signalintensity.groupby('response').size()
        answerOptions = dataframe_signalintensity['response'].value_counts().index.tolist()
#        dataframe_signalintensity.groupby('response').size()
        for y in answerOptions:
            
            if y == "Hit" :
                relHit = relHit + answers['Hit']
            if y == "False Alarm":
                relFalseA = relFalseA + answers['False Alarm']
            if y == "Correct Rejection":
                NCo = NCo + answers['Correct Rejection']
            if y == "Miss":
                NMi = NMi + answers['Miss']
            if y == "No Answer" :
                other = other + answers['No Answer']
                ##### for fit 

            
        listRelHit.append(relHit)
#        print(relHit)
        listRelFalseA.append(relFalseA)
        listNCoFa.append(relFalseA + NCo)
        listNHiMi.append(relHit + NMi)
        listIntensitys.append(x)
        
    a = 0
    np.array(listRelHit)
    np.array(listRelFalseA)
    np.array(listNHiMi)
    np.array(listNCoFa)
    np.array(listIntensitys)
    o = 0
    for p in listRelHit:
#        print ('%s ratio Hits %s' % (a,float(listRelHit[a])/listNGes[a]))
        relHitForIntensity=float(listRelHit[a]/listNHiMi[a])

#        print ('%s ratio False Alarms %s' % (a,float(listRelFalseA[a])/listNGes[a]))
        relFaForIntensity=float(listRelFalseA[a]/listNCoFa[a])
#        print(relFaForIntensity)
        DYesNo = scipy.stats.norm.ppf(relHitForIntensity) - scipy.stats.norm.ppf(relFaForIntensity)
#        print(DYesNo)
        D2IFC = (2*DYesNo) / math.sqrt(2)
        a = a+1
#        print(D2IFC)
        criterium = D2IFC/2
        WsHitAFC = scipy.stats.norm.cdf(((D2IFC - criterium)/math.sqrt(2)))

        NegD2IFC = 0-D2IFC
        WsFAAFC = scipy.stats.norm.cdf(((NegD2IFC - criterium)/math.sqrt(2)))

        
        
        smaltoBig = np.sort(listIntensitys, axis=None)
        
        
    
    
        suggestionData[o][0] = smaltoBig[o]
        nGes = listNCoFa[o] + listNHiMi[o]
        numberOfHits = (nGes/2) * WsHitAFC
#        print (numberOfHits)
        numberOfCA = ((nGes/2) * (1 - WsFAAFC))
#        print (numberOfCA)
        suggestionData[o][1] = numberOfCA + numberOfHits
#        print(nGes)
        suggestionData[o][2] = nGes
#        print (data[o][0])
#        print (data[o][1])
#        print (data[o][2])
        o = o+1
    return suggestionData 
#        
#    ts.plot()
#    plt.plot(sortiert, D)
#    plt.ylim(0, 1)
#    plt.show()


## treffer + false alarm
def RelativePropabilityYesNo (datasetRel):
#    list_of_intensitys = givenData['signal_intensity'].value_counts().index.tolist()
    list_of_intensitys = [3,5,7]
    listRelHit = []
    listRelFalseA = []
    listNGes = []
    for x in list_of_intensitys:
        relHit = 0
        relFalseA = 0
        other = 0
        dataframe_signalintensity = datasetRel[datasetRel['signal_intensity'] == x]
        answers = dataframe_signalintensity.groupby('response').size()
        answerOptions = dataframe_signalintensity['response'].value_counts().index.tolist()
#        dataframe_signalintensity.groupby('response').size()
        for y in answerOptions:
            
            if y == "Hit" :
                relHit = relHit + answers['Hit']
            if y == "False Alarm":
                relFalseA = relFalseA + answers['False Alarm']
            if y == "Correct Rejection":
                other = other + answers['Correct Rejection']
            if y == "Miss":
                other = other + answers['Miss']
            if y == "No Answer" :
                other = other + answers['No Answer']
                ##### for fit 

            
        listRelHit.append(relHit)
        print(relHit)
        listRelFalseA.append(relFalseA)
        listNGes.append(relHit + relFalseA + other)
        
    a = 0
    np.array(listRelHit)
    np.array(listRelFalseA)
    np.array(listNGes)
    for p in listRelHit:
        print ('%s ratio Hits %s' % (a,float(listRelHit[a])/listNGes[a]))
        print ('%s ratio False Alarms %s' % (a,float(listRelFalseA[a])/listNGes[a]))
        a = a+1
    
        
    
def relProb2ifc(dataTwoIFC):
    
    list_of_intensitys = [3,5,7]
#    listRelHit = []
#    listRelFalseA = []
#    listNGes = []
    for x in list_of_intensitys:
#        relTwoHit = 0
#        relTwoFalseA = 0
#        other = 0
        dataframe_signalintensity = dataTwoIFC[dataTwoIFC['signal_intensity'] == x]
        dataStimOnOne    = dataframe_signalintensity[dataframe_signalintensity['signal_on_stimuluspos1'] == True]
        dataHit = dataStimOnOne[dataStimOnOne['response'] == 'correct answer']
        dataMiss = dataStimOnOne[dataStimOnOne['response'] == 'wrong answer']
        
        dataNoStim = dataframe_signalintensity[dataframe_signalintensity['signal_on_stimuluspos1'] == False]
        dataCorrectRejection = dataNoStim[dataNoStim['response'] == 'correct answer']
        dataFalseAlarm =dataNoStim[dataNoStim['response'] == 'wrong answer']
                                              
        print('durchgang Beendet')
        print (dataHit.shape)
        print (dataCorrectRejection.shape)
        print (dataFalseAlarm.shape)
        print (dataMiss.shape)


#def 
###################### Execution ######################

### PREPARATION OF DATA###
 
### a list of filenames in Dictionary 
FileNames=createListOfAllFilesInDic() 

# Create a list of all Dataframes in Dicrionary
df_list = [GetFile(fname) for fname in FileNames]

# Combine all of the dataframes into one big Dataframe
big_df = pd.concat(df_list)

# delet whatever is unnecessary 
del big_df['trials.thisTrialN']
del big_df['trials.thisN']
del big_df['trials.thisIndex']


subData = big_df.loc[big_df['expName'] == "Yes-No Task"]
#subData = big_df.loc[big_df['expName'] == "2IFC"]
subData2IFC = big_df.loc[big_df['expName'] == "2IFC"]
#print (big_df)
##big_df.to_csv('BigData.csv', index=False)
###subData.to_csv('DataYesNo.csv', index=False)
#creating a subdata set with only "yes-No Task


### 2IFC + Suggestion start

dataOne = evaluationAndPlot (create_subdataset_for_participant (nameVpn))
dataTwo = calc2AFCSuggestion(create_subdataset_for_participant (nameVpn))
dataThree = evaluationAndPlot2IFC (create_subdataset_for_participant2IFC(nameVpn))
options             = dict() 
options['expType']     = 'nAFC'   # choose 2-AFC as the experiment type  
options['expN']          = 2 
resultOne = ps.psignifit(dataOne, options)
result = dict()
resultTwo = ps.psignifit(dataTwo, options)
ps.psigniplot.plotPsych(resultOne)
ps.psigniplot.plotPsych(resultTwo, dataColor=[0.8,0.9,0],lineColor=[0.8,0.9,0])
resultThree = ps.psignifit(dataThree, options)
ps.psigniplot.plotPsych(resultThree, dataColor=[0.2,0.5,0],lineColor=[0.2,0.5,0])
## 2IFC + Suggestion end

###### create psychometric function for VPN


#dataOne = evaluationAndPlot (create_subdataset_for_participant (nameVpn))
#options             = dict() 
#options['expType']     = 'nAFC'   # choose 2-AFC as the experiment type  
#options['expN']          = 2 
#options2             = dict() 
#options2['expType']     = 'nAFC'   # choose 2-AFC as the experiment type  
#options2['expN']          = 2 
#options3             = dict() 
#options3['expType']     = 'nAFC'   # choose 2-AFC as the experiment type  
#options3['expN']          = 2 
###### IMMER EINS AUSKOMMENTIEREN ERSTEN WERT ABLESEN UND NOCHMAL RUN ########
#
#options['threshPC']   = 0.3
#options2['threshPC']   = 0.5
#options3['threshPC']   = 0.7
#
#######
#
#resultOne = ps.psignifit(dataOne, options)
#resultTwo = ps.psignifit(dataOne, options2)
#resultThree = ps.psignifit(dataOne, options3)
#result = dict()
#
##result['conf_Intervals']
#ps.psigniplot.plotPsych(resultOne)
#
#print("Hier den Wert ablesen 0.65%:")
#print(resultOne['Fit'][0])
#print("Hier den Wert ablesen 0.75%:")
#print(resultTwo['Fit'][0])
#print("Hier den Wert ablesen 0.85%:")
#print(resultThree['Fit'][0])




##########



##### OLD SHIT DONT DELETE
##### get the rel Propability of VPN (YES NO TASK)
#RelativePropabilityYesNo(create_subdataset_for_participant('felixtest'))
#ps.psigniplot.plotPsych(lineColor=[0,0.4,0.7])
##### get the rel Propability of VPN (2IFC)
#dataTwo = evaluationAndPlot (create_subdataset_for_participant (nameVpn))


#calc2AFCSuggestion(create_subdataset_for_participant (nameVpn))
