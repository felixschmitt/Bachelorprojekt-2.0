# -*- coding: utf-8 -*-
"""
Created on Sun Dec 09 17:17:11 2018

@author: Leon
"""

from psychopy.misc import fromFile
from psychopy import data
import pandas as pd
import sys 
import os 
import numpy

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
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())

#filename_for_panda = _thisDir + os.sep + r'data\acker\Yes-No Task_2018_Dec_11_1409.csv'
#filename_for_panda_to_extend = _thisDir + os.sep + r'data\jolle\Yes-No Task_2018_Dec_11_1527.csv'
#df = pd.read_csv(filename_for_panda)
#print (df)
#### Plott numerical data
#df['signal_intensity'].plot()

#### Automatically find all dataframes and put the name in FileNames

# List to hold file names
FileNames = []

# Your path will be different, please modify the path below.
os.chdir(_thisDir + os.sep + r'data')

# Find any file that ends with ".xlsx"
for files in os.listdir("."):
    if files.endswith(".csv"):
        FileNames.append(files)
        
FileNames

print FileNames

#### Funktioniert 



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



# Create a list of dataframes
df_list = [GetFile(fname) for fname in FileNames]

# Combine all of the dataframes into one
big_df = pd.concat(df_list)
del big_df['trials.thisTrialN']
del big_df['trials.thisN']
del big_df['trials.thisIndex']
print (big_df)
subData = big_df.loc[big_df['expName'] == "Yes-No Task"]


big_df.response.value_counts().plot(kind='barh')
big_df.to_csv('BigData.csv', index=False)
subData.to_csv('DataYesNo.csv', index=False)



