# -*- coding: utf-8 -*-
"""
Created on Wed May 08 15:59:43 2019

@author: Felix
"""
import random


wert1 = 1
wert2 = 2
wert3 = 3
wert4 = 4
wert5 = 5
wert6 = 6
wert7 = 7
wert8 = 8

trials_per_intensity = 3

list_of_intensitys = []

i = 0

while i < trials_per_intensity:
    list_of_intensitys.extend([wert1,wert2,wert3,wert4,wert5,wert6,wert7,wert8])
    i += 1

    
print(list_of_intensitys)

random.shuffle(list_of_intensitys)
    
print(list_of_intensitys)

new_intensity = list_of_intensitys[0]

list_of_intensitys.pop(0)

print(list_of_intensitys)
print(new_intensity)
