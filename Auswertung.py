# -*- coding: utf-8 -*-
"""
Created on Sun Dec 09 17:17:11 2018

@author: Leon
"""

from psychopy.misc import fromFile
from psychopy import data
import sys 
import os 
import numpy

_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
filename_trial = _thisDir + os.sep + u'data/acker/trialdata1.psydat'
datFile = fromFile(filename_trial)
#get info (added when the handler was created)
print (datFile.extraInfo)
#get data
#print (datFile._getAllParamNames())
print (datFile.data['response'])
#datFile.getExp()
#print (datFile.getAllEntries())
#get list of conditions
conditions = datFile.trialList
#for condN, condition in enumerate(conditions):
#    print condition, datFile.data['response'][condN], numpy.mean(datFile.data['response'][condN])
#print(conditions)
print(datFile.getExp())


#### Experimenthandler 
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
filename_trial = _thisDir + os.sep + u'data/acker/Yes-No Task_2018_Dec_11_1409.psydat'
datFile = fromFile(filename_trial)

#print (datFile.extraInfo)
print (datFile.dataFileName)
print (datFile.dataNames)
print (datFile.entries[1][u'response'])
#print (datFile.get('response', default=None))
#print (datFile.entries[2].items())

#first = datFile.entries[2]

#print (datFile.data['response'])

#print(datFile._getAllParamNames())
#dataread=datFile._getAllParamNames()
#print(dataread[1][2])

#print(data_read[2])