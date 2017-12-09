#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 19:42:33 2017

@author: gtabor
"""

biggerdic = {}


#add = np.load('my_file.npy').item()
import os
import numpy as np

files = os.listdir("new")
files.sort()

total = 0
for file in files:
    if file.endswith(".npy") and not file.endswith("combine.npy"):
        
        #print(os.path.join("../AI-Final", file))
        add = np.load('new/'+file).item()
        last = file
        print(file)
        print(len(biggerdic))
        total += len(add)
        for state_pair in add.keys():
            #print(state_pair)
            if state_pair in biggerdic:
                old = biggerdic[state_pair]
                biggerdic[state_pair] = (old[0] + add[state_pair][0],old[1] + add[state_pair][1])
            else:
                biggerdic[state_pair] = (add[state_pair][0],add[state_pair][1])
         
np.save('new/'+last[:-4]+'-combine'+'.npy',biggerdic)

print(len(biggerdic))
print(total)
