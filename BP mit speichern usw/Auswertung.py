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
from scipy.stats import binom

#import plotly
#import plotly.plotly as py
#import plotly.tools as tls





nameVpn = ""



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
    os.chdir(_thisDir + os.sep + r'data/creating')
    
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
    location = _thisDir + os.sep + r'data/creating/' + file_name
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
def create_subdataset_for_participant (name, task):
    
    
    participant_data = subData.loc[subData['participant'] == name]
#    participant_data = participant_data.loc[participant_data['session'] == 2 ]
#    participant_data = participant_data.loc[participant_data['random_intensity'] == False]
    participant_data = participant_data.loc[participant_data['Task'] == task]
#    print(participant_data.sum())
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
        
def evaluationAndPlot (givenData, IFCnew,Task):
    
    
    count=[]
    correct_fit = []
    n_total_fit = []
    o = 0
#    print(dataframe_signalintensity.groupby('response').size())
    i=0
#    print("hier")
    list_of_intensitys = givenData['signal_intensity'].value_counts().index.tolist()
#    list_of_intensitys = [9.7,8.2,6.0,3.8,2.5,7.0,5.0,2.6]
    ## sortiere in Aufsteigender reihenfolge
    
    sortiert = np.sort(list_of_intensitys, axis=None)     # sort the flattened array
    print(Task)
    for x in sortiert:
        correct = 0
        wrong = 0
        noAnswer = 0
        dataframe_signalintensity = givenData[givenData['signal_intensity'] == x]
        if IFCnew == True:
            answers = dataframe_signalintensity.groupby('response_2IFCnew').size()
            answerOptions = dataframe_signalintensity['response_2IFCnew'].value_counts().index.tolist()
        else:  
            answers = dataframe_signalintensity.groupby('response').size()
            answerOptions = dataframe_signalintensity['response'].value_counts().index.tolist()
#        dataframe_signalintensity.groupby('response').size()
        
        if IFCnew == True:
            
            for y in answerOptions:
                if y == 0:
                    noAnswer = noAnswer + answers[0]
                if y == 1 :
                    correct = correct + answers[1]
                if y == 3 :
                    correct = correct + answers[3]
                if y == 5 :
                    correct = correct + answers[5]
                if y == 6 :
                    correct = correct + answers[6]                    
                if y == 2 :
                    wrong = wrong + answers[2]
                if y == 4 :
                    wrong = wrong + answers[4]
                if y == 7 :
                    wrong = wrong + answers[7]
                if y == 8 :
                    wrong = wrong + answers[8]                    
        else:
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
                    noAnswer = noAnswer + answers['No Answer']
                    ##### for fit 
                if y == "correct answer" :
                    correct = correct + answers['correct answer']
                if y == "wrong answer" :
                    wrong = wrong + answers['wrong answer']

            
        correct_fit.append(correct)
        n_total_fit.append(correct + wrong)

        count.append(float(correct) / float(correct + wrong))
        i = i+1
        

        print('Signalstärke' + str(x))
        print('Antwort Verpasst: ' + str(noAnswer))
        
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
    list_of_intensitys = datasetRel['signal_intensity'].value_counts().index.tolist()
    list_of_intensitys = np.sort(list_of_intensitys, axis=None)
    listRelHit = []
    listRelCorRej = []
    listRelMiss = []
    listRelFalseA = []
    listNGes = []
    
    
    for x in list_of_intensitys:
        relHit = 0
        relFalseA = 0
        relCorRej = 0
        relMiss = 0
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
                relCorRej = relCorRej + answers['Correct Rejection']
            if y == "Miss":
                relMiss = relMiss + answers['Miss']
#            if y == "No Answer" :
#                other = other + answers['No Answer']
                ##### for fit 

            
        listRelHit.append(relHit)
        listRelFalseA.append(relFalseA)
        listNGes.append(relHit + relFalseA)
        listRelCorRej.append(relCorRej)
        listRelMiss.append(relMiss)
    a = 0
    np.array(listRelHit)
    np.array(listRelFalseA)
    np.array(listNGes)
    np.array(listRelCorRej)
    np.array(listRelMiss)
#    print (list_of_intensitys)
    for p in listRelHit:
        print ('%s ratio Hits %s' % (a,float(listRelHit[a])/(listRelHit[a] + listRelMiss[a])))

        print('%s Anzahl Da %s' % (a,(float(listRelHit[a] + listRelMiss[a]))))
        print ('%s ratio FA %s' % (a,float(listRelFalseA[a]/(listRelFalseA[a]+ listRelCorRej[a]))))
        print('%s ratio CR %s' % (a,float(listRelCorRej[a]/(listRelCorRej[a]+ listRelFalseA[a]))))

        print('%s Anzahl nicht da %s' % (a,float(listRelCorRej[a]+ listRelFalseA[a])))
        a = a+1
        
    
def relProb2ifc(dataTwoIFC):
    
    list_of_intensitys = dataTwoIFC['signal_intensity'].value_counts().index.tolist()
    list_of_intensitys = np.sort(list_of_intensitys, axis=None)
#    listRelHit = []
#    listRelFalseA = []
#    listNGes = []
    print(list_of_intensitys)
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
                                              
        print('SignalstärkeNR:'+str(x))
        print (dataHit.shape[0])
        print (dataCorrectRejection.shape[0])
        print (dataFalseAlarm.shape[0])
        print (dataMiss.shape[0])
        
def relProb2IFCnew(dataTwoIFC):
    
    list_of_intensitys = dataTwoIFC['signal_intensity'].value_counts().index.tolist()
    list_of_intensitys = np.sort(list_of_intensitys, axis=None)
#    listRelHit = []
#    listRelFalseA = []
#    listNGes = []

    a=0
    for x in list_of_intensitys:
#        relTwoHit = 0
#        relTwoFalseA = 0
#        other = 0
        dataframe_signalintensity = dataTwoIFC[dataTwoIFC['signal_intensity'] == x]
        dataHit = dataframe_signalintensity[dataframe_signalintensity['response_2IFCnew'] == 1]
        dataHit2 = dataframe_signalintensity[dataframe_signalintensity['response_2IFCnew'] == 5]
#        dataHit = dataHit + dataHit2 
        dataMiss = dataframe_signalintensity[dataframe_signalintensity['response_2IFCnew'] == 4]
        dataMiss2 = dataframe_signalintensity[dataframe_signalintensity['response_2IFCnew'] == 8]
#        dataMiss = dataMiss + dataMiss2
        dataFA = dataframe_signalintensity[dataframe_signalintensity['response_2IFCnew'] == 2]
        dataFA2 = dataframe_signalintensity[dataframe_signalintensity['response_2IFCnew'] == 7]
#        pd.concat(dataFA + dataFA2)
        dataCR = dataframe_signalintensity[dataframe_signalintensity['response_2IFCnew'] == 3]
        dataCR2 = dataframe_signalintensity[dataframe_signalintensity['response_2IFCnew'] == 6]
#        dataCR = dataCR + dataCR2
                                              
#        print('SignalstärkeNR:'+str(x))
#        print (dataHit.shape[0]+ dataHit2.shape[0])
#        print (dataCR.shape[0]+dataCR2.shape[0])
#        print (dataFA.shape[0]+dataFA2.shape[0])
#        print (dataMiss.shape[0]+dataMiss2.shape[0])
        hit = dataHit.shape[0]+ dataHit2.shape[0]
        cr = dataCR.shape[0]+dataCR2.shape[0]
        fa = dataFA.shape[0]+dataFA2.shape[0]
        miss = dataMiss.shape[0]+dataMiss2.shape[0]
        
        hitProbability = float(hit)/(hit + miss)

        faProbability = float(fa)/(fa + cr)
        
        if hitProbability == 1:
            faProbability = float(fa + 0.5)/(fa + cr +1)
            hitProbability = float(hit + 0.5)/(hit + miss +1)
#            print('guess because infinit hit == 1')
        if faProbability == 0:
            faProbability = float(fa + 0.5)/(fa + cr +1)
            hitProbability = float(hit + 0.5)/(hit + miss +1)
#            print('guess because infinit FA == 0')
            
        dprime = scipy.stats.norm.ppf(hitProbability) - scipy.stats.norm.ppf(faProbability)
#        print ('%s DPRIME %s' % (a+1,dprime))
        dprimeString = str(dprime)
        printDprime = dprimeString[0:1]+','+dprimeString[2:len(dprimeString)-1]
        print(printDprime)
        a = a+1
        
#### achtung, verändert Reihenfolge, wenn funktion 1 ausgeführt dann funktion 2 ausführen 
        
def correct_dataset (data_set):

    change_answer_to = 0
    i=0
    k=0
    l=0
    exeption = False
    for index in range(0,len(data_set)):
         ### only for Leon
        
        
        
        
        
        if data_set.iat[index,5] != False:
            data_set.iat[index,5] = False
        ###### end         
            
        if data_set.iat[index,0] == '2IFCnew':
            change_answer_to = 0
            

            

            
            if data_set.iat[index,16] == -1 :
                data_set.iat[index,8] = -1
            
            ## time response -1
            if data_set.iat[index,16] != -1 :
                
                
                if data_set.iat[index,17] != 'HACA03':
                    ## überprüfung auf Zufall
                    if data_set.iat[index,5] == True:
                        exeption = True

                if data_set.iat[index,7] == 2 :
                    change_answer_to = 3
                if data_set.iat[index,7] == 3 :
                    change_answer_to = 2
                
                if change_answer_to != 0 and exeption == False:
                    data_set.iat[index,7] = change_answer_to
#                    l = l+1
                    
                exeption = False
            ####### for josu
                k = k+1
            if data_set.iat[index,4] =='JOSU26':
                if data_set.iat[index,5] == False:
                    l = l+1
                    
                    if data_set.iat[index,7] == 3:
                        data_set.iat[index,6] = 'Correct Rejection'
                    
                    if data_set.iat[index,7] == 4:
                        data_set.iat[index,6] = 'Miss'
                        
                
                
                    
                    if data_set.iat[index,7] == 5:
                        data_set.iat[index,6] = 'False Alarm'
                    if data_set.iat[index,7] == 6:
                        data_set.iat[index,6] = 'Miss'
                    if data_set.iat[index,7] == 7:
                        data_set.iat[index,6] = 'Hit'
                    if data_set.iat[index,7] == 8:
                        data_set.iat[index,6] = 'Correct Rejection'
    print(data_set.iat[index,4]) 
    print(l)
    print(i) 
    print(k)
#    print(data_set.sum)
    data_set.to_csv('CorrectedData2IFC.csv', index=False)
    
def deePrimeYesNo (dataPerson):
    ## 
    list_of_intensitys = dataPerson['signal_intensity'].value_counts().index.tolist()
    list_of_intensitys = np.sort(list_of_intensitys, axis=None)
    listHit = []
    listFA = []
    listCR = []
    listMiss = []
    listNGes = []
    relevantArray = np.empty([len(list_of_intensitys),4], dtype=float)
    count = 0
    for x in list_of_intensitys:
        Hits= 0
        FalseAlarm= 0
        Miss = 0
        CorrectR = 0
        other = 0
        dataframe_signalintensity = dataPerson[dataPerson['signal_intensity'] == x]
        answers = dataframe_signalintensity.groupby('response').size()
        answerOptions = dataframe_signalintensity['response'].value_counts().index.tolist()
#        dataframe_signalintensity.groupby('response').size()
        for y in answerOptions:
            
            if y == "Hit" :
                Hits= Hits+ answers['Hit']
            if y == "False Alarm":
                FalseAlarm= FalseAlarm+ answers['False Alarm']
            if y == "Correct Rejection":
                CorrectR = CorrectR + answers['Correct Rejection']
            if y == "Miss":
                Miss = Miss + answers['Miss']
            if y == "No Answer" :
                other = other + answers['No Answer']
                ##### for fit 

            
        listHit.append(Hits)
        listFA.append(FalseAlarm)
        listCR.append(CorrectR)
        listMiss.append(Miss)
        listNGes.append(Hits+ FalseAlarm+ other)
        relevantArray[count][0] = ((Hits + 0.5)/(Hits + Miss +1 ))
        relevantArray[count][1] = Hits + Miss + 1
        relevantArray[count][2] = (FalseAlarm + 0.5)/ (FalseAlarm + CorrectR +1) 
        relevantArray[count][3] = FalseAlarm + CorrectR + 1
        count = count +1 
    a = 0
    np.array(listHit)
    np.array(listFA)
    np.array(listCR)
    np.array(listMiss)
    np.array(listNGes)
    
    for p in listHit:
        hitProbability = float(listHit[a])/(listHit[a]+listMiss[a])

        faProbability = float(listFA[a])/(listFA[a]+listCR[a])

        if hitProbability == 1:
            faProbability = float(listFA[a]+ 0.5)/(listFA[a]+listCR[a]+1)
            hitProbability = float(listHit[a] + 0.5)/(listHit[a]+listMiss[a]+1)
#            print('guess because infinit hit == 1')
        if faProbability == 0:
            faProbability = float(listFA[a]+ 0.5)/(listFA[a]+listCR[a]+1)
            hitProbability = float(listHit[a] + 0.5)/(listHit[a]+listMiss[a]+1)
#            print('guess because infinit FA == 0')
            
        dprime = scipy.stats.norm.ppf(hitProbability) - scipy.stats.norm.ppf(faProbability)
#        print ('%s DPRIME %s' % (a+1,dprime))
        dprimeString = str(dprime)
        printDprime = dprimeString[0:1]+','+dprimeString[2:len(dprimeString)-1]
        print(printDprime)
        a = a+1
        printDprime = 0
    return (relevantArray)
        
    
def DeePrime2IFC (dataPerson):
    list_of_intensitys = dataPerson['signal_intensity'].value_counts().index.tolist() 
    listHit = []
    listFalseA = []
    listCorrectR = []
    listMiss = []
    smaltoBig = np.sort(list_of_intensitys, axis=None)
    listNGes = []
    #hits/ n ges da 1,2
    #fa / nges nicht da 3,4
#    np.empty([len(sortiert),3], dtype=float)
    relevantArray = np.empty([len(list_of_intensitys),4], dtype=int)
    count = 0
    # for each signal intensity
    for x in smaltoBig:
        Hit = 0
        FalseA = 0
        CorrectR = 0
        Miss = 0
        other = 0
        # filters only specific signal intensity
        dataframe_signalintensity = dataPerson[dataPerson['signal_intensity'] == x]
        # filters only trials where stimulus was on position 1 (hits & misses)
        dataStimOnOne = dataframe_signalintensity[dataframe_signalintensity['signal_on_stimuluspos1'] == True]
        # filters only trials where stimulus was on position 2 (false as & correct rs)
        dataStimOnTwo = dataframe_signalintensity[dataframe_signalintensity['signal_on_stimuluspos1'] == False]
        # gets the amount of correct and wrong answers with stimulus on position one
        answersOnOne = dataStimOnOne.groupby('response').size()

        # gets the amount of correct and wrong answers with stimulus on position two
        answersOnTwo = dataStimOnTwo.groupby('response').size()
        # correct answer & wrong answer
#        answerOptions = dataframe_signalintensity['response'].value_counts().index.tolist()
        
        firstInterval =dataStimOnOne['response'].value_counts().index.tolist()
        secondInterval = dataStimOnTwo['response'].value_counts().index.tolist()
        

        for y in firstInterval:
            
            if y == "correct answer" :
 
                Hit = Hit + answersOnOne['correct answer']
            if y == "wrong answer":

                Miss = Miss + answersOnOne['wrong answer']
        for y in secondInterval:
            
            if y == "correct answer" :
                
                CorrectR = CorrectR + answersOnTwo['correct answer']
                
            if y == "wrong answer":
               
                FalseA = FalseA + answersOnTwo['wrong answer']
              
        listHit.append(Hit)
        listFalseA.append(FalseA)
        listCorrectR.append(CorrectR)
        listMiss.append(Miss)
        listNGes.append(Hit + FalseA + CorrectR + Miss + other)
        print()
        relevantArray[count][0] = Hit /(Hit + Miss)
        relevantArray[count][1] = Hit + Miss
        relevantArray[count][2] = FalseA /(FalseA + CorrectR)
        relevantArray[count][3] = FalseA + CorrectR
        count = count +1  
    a = 0
    np.array(listHit)
    np.array(listFalseA)
    np.array(listNGes)
    
    #gibt DeePrime aus, beginnend mit dem d' zur kleiner Signalintensität
    for p in listHit:
        hitProbability = float(listHit[a])/(listHit[a]+listMiss[a])

        faProbability = float(listFalseA[a])/(listFalseA[a]+listCorrectR[a])

        
        if hitProbability == 1:
            faProbability = float(listFalseA[a]+ 0.5)/(listFalseA[a]+listCorrectR[a]+1)
            hitProbability = float(listHit[a] + 0.5)/(listHit[a]+listMiss[a]+1)
#            print('guess because infinit hit == 1')
        if faProbability == 0:
            faProbability = float(listFalseA[a]+ 0.5)/(listFalseA[a]+listCorrectR[a]+1)
            hitProbability = float(listHit[a] + 0.5)/(listHit[a]+listMiss[a]+1)
#            print('guess because infinit FA == 0')
            
        dprime = scipy.stats.norm.ppf(hitProbability) - scipy.stats.norm.ppf(faProbability)
#        print ('%s DPRIME %s' % (a+1,dprime))
        #print mit komma
        dprimeString = str(dprime)
        printDprime = dprimeString[0:1]+','+dprimeString[2:len(dprimeString)-1]
        print(printDprime)
        a = a+1
    return relevantArray
    
def reactionTime (data):
    timeHit=0
    timeCR=0
    timeMiss=0
    timeFA =0
    answers = data.groupby('response').size()
    answerOptions = data['response'].value_counts().index.tolist()
    for y in answerOptions:
            
        if y == "Hit" :

            reactionTimeHitdata= data[data['response'] == 'Hit']
            reactionTimeHit = reactionTimeHitdata['time_response'].value_counts().index.tolist()
            for elem in reactionTimeHit:
                timeHit = elem + timeHit
            meanTimeHit = timeHit/reactionTimeHitdata.shape[0]
        if y == "False Alarm":
            reactionTimeFAdata= data[data['response'] == 'False Alarm']
            reactionTimeFA = reactionTimeFAdata['time_response'].value_counts().index.tolist()
            for elem in reactionTimeFA:
                timeFA = elem + timeFA
            meanTimeFA = timeFA/reactionTimeFAdata.shape[0]
        if y == "Correct Rejection":
            reactionTimeCRdata= data[data['response'] == 'Correct Rejection']
            reactionTimeCR = reactionTimeCRdata['time_response'].value_counts().index.tolist()
            for elem in reactionTimeCR:
                timeCR = elem + timeCR
            meanTimeCR = timeCR/reactionTimeCRdata.shape[0]
        if y == "Miss":
            reactionTimeMissdata= data[data['response'] == 'Miss']
            reactionTimeMiss = reactionTimeMissdata['time_response'].value_counts().index.tolist()
            for elem in reactionTimeMiss:
#                if elem != -1:
                timeMiss = elem + timeMiss
#                else: 
#                    noCount = noCount +1
            meanTimeMiss = timeMiss/reactionTimeMissdata.shape[0]

    print(meanTimeHit)
    print(meanTimeFA)
    print(meanTimeCR)
    print(meanTimeMiss)
    
def reactionTime2IFCnew (data):
    time1=0
    time2=0
    time3=0
    time4 =0
    time5=0
    time6=0
    time7=0
    time8 =0
#    meanTime1=0
#    meanTime2=0
#    meanTime3=0
#    meanTime4 =0
#    meanTime5=0
#    meanTime6=0
#    meanTime7=0
#    meanTime8 =0
    
    answers = data.groupby('response_2IFCnew').size()
    answerOptions = data['response_2IFCnew'].value_counts().index.tolist()
    for y in answerOptions:
            
        if y == 1 :

            reactionTime1data= data[data['response_2IFCnew'] == 1]
            reactionTime1 = reactionTime1data['time_response'].value_counts().index.tolist()
            for elem in reactionTime1:
                time1 = elem + time1
            meanTime1 = time1/reactionTime1data.shape[0]
        if y == 2:
            reactionTime2data= data[data['response_2IFCnew'] == 2]
            reactionTime2 = reactionTime2data['time_response'].value_counts().index.tolist()
            for elem in reactionTime2:
                time2 = elem + time2
            meanTime2 = time2/reactionTime2data.shape[0]
        if y == 3:
            reactionTime3data= data[data['response_2IFCnew'] == 3]
            reactionTime3 = reactionTime3data['time_response'].value_counts().index.tolist()
            for elem in reactionTime3:
                time3 = elem + time3
            meanTime3 = time3/reactionTime3data.shape[0]
        if y == 4:
            reactionTime4data= data[data['response_2IFCnew'] == 4]
            reactionTime4 = reactionTime4data['time_response'].value_counts().index.tolist()
            for elem in reactionTime4:
#                if elem != -1:
                time4 = elem + time4
#                else: 
#                    noCount = noCount +1
            meanTime4 = time4/reactionTime4data.shape[0]
        if y == 5 :

            reactionTime5data= data[data['response_2IFCnew'] == 5]
            reactionTime5 = reactionTime5data['time_response'].value_counts().index.tolist()
            for elem in reactionTime5:
                time5 = elem + time5
            meanTime5 = time5/reactionTime5data.shape[0]
        if y == 6 :

            reactionTime6data= data[data['response_2IFCnew'] == 6]
            reactionTime6 = reactionTime6data['time_response'].value_counts().index.tolist()
            for elem in reactionTime6:
                time6 = elem + time6
            meanTime6 = time6/reactionTime6data.shape[0]
        if y == 7 :

            reactionTime7data= data[data['response_2IFCnew'] == 7]
            reactionTime7 = reactionTime7data['time_response'].value_counts().index.tolist()
            for elem in reactionTime7:
                time7 = elem + time7
            meanTime7 = time7/reactionTime7data.shape[0]
        if y == 8 :

            reactionTime8data= data[data['response_2IFCnew'] == 8]
            reactionTime8 = reactionTime8data['time_response'].value_counts().index.tolist()
            for elem in reactionTime8:
                time8 = elem + time8
            
            meanTime8 = time8/reactionTime8data.shape[0]
            
    print(meanTime1)
    print(meanTime2)
    print(meanTime3)
    print(meanTime4)  
    print(meanTime5)
    print(meanTime6)
    print(meanTime7)
    print(meanTime8)      
    
def bootstrap(array):
#    print(scipy.stats.binom.rvs(30,36))
    counter = 0
    dPrime = np.empty([8,1000])
    dPrimeTrue = 0
    dPrimeBox = np.empty([3,8])
    stimulus = [ 1.4 , 3.8 , 5.8 , 7.5 , 9.1 ,10.7, 12.4 ,14.3]
    # so oft wie arraylänge
    for x in array:
#        print(array[counter,1])
        r = binom.rvs(int(array[counter,1]), array[counter,0], size=1000)
    #    r = scipy.stats.binom.rvs()
        fa = binom.rvs(int(array[counter,3]), array[counter,2], size=1000)
    
        dPrimeTrue = scipy.stats.norm.ppf((array[counter][1]*array[counter][0])/array[counter][1]) - scipy.stats.norm.ppf((array[counter][3]*array[counter][2])/array[counter][3])
        local = 0
        
#        r.sort()
#        r=r[:974]
#        r=r[24:]
#        plt.hist(r)

        for z in r :
             
            dPrime[counter][local] = scipy.stats.norm.ppf(r[local]/array[counter][1]) - scipy.stats.norm.ppf(fa[local]/array[counter][3])
#            print(dPrime[counter][local])

    #        print ('%s DPRIME %s' % (a+1,dprime))
#            dprimeString = str(dprime)
#            printDprime = dprimeString[0:1]+','+dprimeString[2:len(dprimeString)-1]
            local = local +1
        stepBetween = dPrime[counter,:]
        stepBetween.sort()
        h=0
        ## finding point of no inf berchnung 2,5 bzw 97,5 prozent
        percentil975 = 974
        percentil025 = 24

        for l in stepBetween:
#            print(stepBetween[h])
            if stepBetween[h] == math.inf:

                stepBetween =  stepBetween[0:(h-1)]
                percentil975 = round((len(stepBetween)*0.975),0)
                percentil025 = round((len(stepBetween)*0.025),0)
#                print(percentil975)
                break
#                print(percentil025)
#                searching = False
#            
#            if h > len(stepBetween)-2:
#                searching = False
            if h > len (stepBetween)-2:
#                searching = False
                break
            h = h+1
#        print(printDprime)
#        r.sort()
        np.array(stepBetween)
#        print(len(stepBetween))
        print(str(counter)+ 'signalstärke')
        print(dPrimeTrue)
        print(stepBetween[int(percentil025)])
        print(stepBetween[int(percentil975)])
        dPrimeBox[0][counter]=stepBetween[int(percentil025)]
        dPrimeBox[1][counter]=stepBetween[int(percentil975)]
        dPrimeBox[2][counter]= dPrimeTrue
#        print(dPrime[counter][percentil975])
#        plt.hist(fa)
#        print(r[24],r[974])
        
    
        
        counter = counter +1
    
    df = pd.DataFrame(dPrimeBox, columns=stimulus)
    df.plot.box(grid='True')
#    df = pd.DataFrame(np.random.rand(10, 5), columns=['A', 'B', 'C', 'D', 'E'])
#    print(np.random.rand(10, 5))
#    df.plot.box(grid='True')
#    print(r)
#################### 
    
# eine Funktion noch die Josua26 macht          
        
#        print (data_set.iat[index,2])
    
#        print(data_set.loc[data_set['time_response_second']!= -1].index[6].values)
#        for i in data_set.iteritems():
       
        
#            data_set.at[i, 'ifor'] = x
#        else:
#            data_set.at[i, 'ifor'] = y
#    for x in subData2IFCnew.iteritems():
#        print(data_set.loc[data_set['time_response_second']!= -1].index[1])

#        if x['time_response_second'] != -1:
#            change_answer_to = 0
#            if x['response_2IFCnew'] == 2 :
#                change_answer_to = 3
#            if x['response_2IFCnew'] == 3 :
#                change_answer_to = 2
#            print(x['response_2IFCnew'])
#            if change_answer_to != 0 :
#                x.set_value['response_2IFCnew'] == change_answer_to
#            print(x['response_2IFCnew'])
#            break
#    subData2IFCnew.to_csv('CorrectedData.csv', index=False)
                
                
            
        

#def 
###################### Execution ######################

### PREPARATION OF DATA###
 
### a list of filenames in Dictionary 
FileNames=createListOfAllFilesInDic()

# Create a list of all Dataframes in Dicrionary
df_list = [GetFile(fname) for fname in FileNames]

# Combine all of the dataframes into one big Dataframe

############
big_df = pd.concat(df_list)
#############


# delet whatever is unnecessary 
#del big_df['trials.thisTrialN']
#del big_df['trials.thisN']
#del big_df['trials.thisIndex']
#
#big_df.to_csv('CorrectedData2IFC.csv', index=False)

### fuctions above work with subData
### File einlesen 

dataInload = GetFile('CorrectedData2IFC.csv')
#print(dataInload.shape)

subData = dataInload[dataInload['trials.thisRepN'] > 4]
#g=subData.corr(method='pearson')
#print(g)

#print(subData.shape)
### aktuell nicht benutzt
#subData = big_df.loc[big_df['expName'] == "Yes-No Task"]
#subData = big_df.loc[big_df['expName'] == "2IFC"]
subData2IFC = subData.loc[subData['expName'] == "2IFCnew"]
subData2IFCnew = big_df.loc[big_df['expName'] == "2IFCnew"]

#reactionTime2IFCnew(subData2IFC)

########## Ausführungsbereich

#### plot für versuchsperson

nameVpn = 'WOAN27'
#print(DeePrime2IFC (create_subdataset_for_participant(nameVpn,"2IFC")))
#print(deePrimeYesNo (create_subdataset_for_participant(nameVpn,"Yes-No Task")))
bootstrap(deePrimeYesNo (create_subdataset_for_participant(nameVpn,"Yes-No Task")))
bootstrap(deePrimeYesNo (create_subdataset_for_participant(nameVpn,"2IFCnew")))
#
#VPNs = ['RORE28','JOSU26','WOAN27','KLRU16','DIAN07','MIJA04','TOSY08','HACA03']
#
#
#for nameVpn in VPNs:
#    print(nameVpn)
#    print('yesNo')
#    deePrimeYesNo (create_subdataset_for_participant(nameVpn,"Yes-No Task")) 
#    print('2IFCnew1Intervall')
#    deePrimeYesNo (create_subdataset_for_participant(nameVpn,"2IFCnew"))
#    print('2IFC')
#    DeePrime2IFC (create_subdataset_for_participant(nameVpn,"2IFC"))
#    print('2IFCnew')
#    relProb2IFCnew (create_subdataset_for_participant(nameVpn,"2IFCnew"))
#RelativePropabilityYesNo(create_subdataset_for_participant(nameVpn,"Yes-No Task"))
#RelativePropabilityYesNo(create_subdataset_for_participant(nameVpn,"2IFCnew"))
#relProb2ifc(create_subdataset_for_participant(nameVpn,"2IFC"))
#relProb2IFCnew(create_subdataset_for_participant(nameVpn,"2IFCnew"))
#dataOne = evaluationAndPlot (create_subdataset_for_participant (nameVpn,"2IFCnew"),True,"2IFCnew")
#options             = dict() 
#options['expType']     = 'nAFC'   # choose 2-AFC as the experiment type  
#options['expN']          = 2 
##options['threshPC']   = 0.5 # 0.75
#resultOne = ps.psignifit(dataOne, options)
#ps.psigniplot.plotPsych(resultOne, dataColor=[0.2,0.1,1],lineColor=[0.2,0.1,1])
#
#
#dataTwo = evaluationAndPlot(create_subdataset_for_participant(nameVpn,"2IFCnew"),False,"1IFCnew")
#resultTwo = ps.psignifit(dataTwo, options)
#ps.psigniplot.plotPsych(resultTwo, dataColor=[0.8,0.5,0],lineColor=[0.8,0.5,0])
#
#
#dataThree = evaluationAndPlot (create_subdataset_for_participant(nameVpn,"Yes-No Task"),False,"Yes-No Task")
#resultThree = ps.psignifit(dataThree, options)
#ps.psigniplot.plotPsych(resultThree, dataColor=[0.2,0.5,0],lineColor=[0.2,0.5,0])
#
#dataFour = evaluationAndPlot (create_subdataset_for_participant(nameVpn,"2IFC"),False,"2IFC")
#resultFour = ps.psignifit(dataFour, options)
#ps.psigniplot.plotPsych(resultFour, dataColor=[0.4,0.3,0.2],lineColor=[0.4,0.3,0.2])

############

#########



####### datei einlesen Collumns löschen
#corrected = GetFile('CorrectedData2IFC.csv')

############


#########
#corrected = big_df
##
#del corrected['trials.thisTrialN']
#del corrected['trials.thisN']
#del corrected['trials.thisIndex']
#del corrected['Unnamed: 17']
#del corrected['Unnamed: 18']
#del corrected['Unnamed: 20']
#del corrected['Unnamed: 21']
##del corrected['Unnamed: 8']
#corrected.to_csv('ControllFeddich.csv', index=False)
##
#### creats deleted frame
#correct_dataset (corrected)
#########################



#correct_josu26 (subData2IFCnew)
#print (big_df)
##big_df.to_csv('BigData.csv', index=False)
###subData.to_csv('DataYesNo.csv', index=False)
#creating a subdata set with only "yes-No Task


### 2IFC + Suggestion start
#
#dataOne = evaluationAndPlot (create_subdataset_for_participant (nameVpn))
#dataTwo = calc2AFCSuggestion(create_subdataset_for_participant (nameVpn))
#dataThree = evaluationAndPlot2IFC (create_subdataset_for_participant2IFC(nameVpn))
#options             = dict() 
#options['expType']     = 'nAFC'   # choose 2-AFC as the experiment type  
#options['expN']          = 2 
#resultOne = ps.psignifit(dataOne, options)
#result = dict()
#resultTwo = ps.psignifit(dataTwo, options)
#ps.psigniplot.plotPsych(resultOne)
#ps.psigniplot.plotPsych(resultTwo, dataColor=[0.8,0.9,0],lineColor=[0.8,0.9,0])
#resultThree = ps.psignifit(dataThree, options)
#ps.psigniplot.plotPsych(resultThree, dataColor=[0.2,0.5,0],lineColor=[0.2,0.5,0])
### 2IFC + Suggestion end

###### create psychometric function for VPN

##############
#dataOne = evaluationAndPlot (create_subdataset_for_participant (nameVpn))
##dataOne = evaluationAndPlot (big_df)
##dataOne = evaluationAndPlot (subData)
#options             = dict() 
#options['expType']     = 'nAFC'   # choose 2-AFC as the experiment type  
#options['expN']          = 2 
#options2             = dict() 
#options2['expType']     = 'nAFC'   # choose 2-AFC as the experiment type  
#options2['expN']          = 2 
#options3             = dict() 
#options3['expType']     = 'nAFC'   # choose 2-AFC as the experiment type  
#options3['expN']          = 2 
#options4             = dict() 
#options4['expType']     = 'nAFC'   # choose 2-AFC as the experiment type  
#options4['expN']          = 2 
#options5             = dict() 
#options5['expType']     = 'nAFC'   # choose 2-AFC as the experiment type  
#options5['expN']          = 2 
#options6             = dict() 
#options6['expType']     = 'nAFC'   # choose 2-AFC as the experiment type  
#options6['expN']          = 2 
#options7             = dict() 
#options7['expType']     = 'nAFC'   # choose 2-AFC as the experiment type  
#options7['expN']          = 2 
#options8             = dict() 
#options8['expType']     = 'nAFC'   # choose 2-AFC as the experiment type  
#options8['expN']          = 2 
# 
###### IMMER EINS AUSKOMMENTIEREN ERSTEN WERT ABLESEN UND NOCHMAL RUN ########
#
#options['threshPC']   = 0.1 # 0.55
#options2['threshPC']   = 0.2 # 0.60
#options3['threshPC']   = 0.3 # 0.65
#options4['threshPC']   = 0.4 # 0.7
#options5['threshPC']   = 0.5 # 0.75
#options6['threshPC']   =  0.6 #0.8
#options7['threshPC']   =  0.7 #0.85
#options8['threshPC']   = 0.8 # 0.9
#
#
#######
#
#resultOne = ps.psignifit(dataOne, options)
#resultTwo = ps.psignifit(dataOne, options2)
#resultThree = ps.psignifit(dataOne, options3)
#resultFour = ps.psignifit(dataOne, options4)
#resultFive = ps.psignifit(dataOne, options5)
#resultSix = ps.psignifit(dataOne, options6)
#resultSeven = ps.psignifit(dataOne, options7)
#resultEight = ps.psignifit(dataOne, options8)
#
#result = dict()
#
##result['conf_Intervals']
#ps.psigniplot.plotPsych(resultFour)
#ps.psigniplot.plotPsych(resultTwo)
#ps.psigniplot.plotPsych(resultOne)
#ps.psigniplot.plotPsych(resultThree)
#
#ps.psigniplot.plotPsych(resultFive)
#ps.psigniplot.plotPsych(resultSix)
#
#ps.psigniplot.plotPsych(resultSeven)
#ps.psigniplot.plotPsych(resultEight)
#
#
#print("Hier den Wert ablesen 0.55%:")
#print(resultOne['Fit'][0])
#print("Hier den Wert ablesen 0.60%:")
#print(resultTwo['Fit'][0])
#print("Hier den Wert ablesen 0.65%:")
#print(resultThree['Fit'][0])
#print("Hier den Wert ablesen 0.70%:")
#print(resultFour['Fit'][0])
#print("Hier den Wert ablesen 0.75%:")
#print(resultFive['Fit'][0])
#print("Hier den Wert ablesen 0.80%:")
#print(resultSix['Fit'][0])
#print("Hier den Wert ablesen 0.85%:")
#print(resultSeven['Fit'][0])
#print("Hier den Wert ablesen 0.90%:")
#print(resultEight['Fit'][0])
###################




##########



##### OLD SHIT DONT DELETE
##### get the rel Propability of VPN (YES NO TASK)
#RelativePropabilityYesNo(create_subdataset_for_participant('felixtest'))
#ps.psigniplot.plotPsych(lineColor=[0,0.4,0.7])
##### get the rel Propability of VPN (2IFC)
#dataTwo = evaluationAndPlot (create_subdataset_for_participant (nameVpn))


#calc2AFCSuggestion(create_subdataset_for_participant (nameVpn))
