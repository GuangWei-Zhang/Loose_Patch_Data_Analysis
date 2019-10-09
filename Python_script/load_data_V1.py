#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 23:16:47 2019

@author: zhangguangwei
"""

# first we need to load the data from the .mat file recorded using HEKA, which exported in .mat

# first we gonna try scipy as https://scipy-cookbook.readthedocs.io/items/Reading_mat_files.html

from scipy.io import loadmat

file_path = '/Users/zhangguangwei/Documents/GitHub/Loose_Patch_Data_Analysis/Test_data/A1_L4_Py/3.mat'
  
mat_data = loadmat(file_path)

# now the mat_data is a dict data type
# in this mat_data, the first three items would be the header
# 1. the name of the dictionary is  __header__
# the dictionary looks like  b'MATLAB 5.0 MAT-file, Created by PatchMaster on: 06-May-2015 11:46:04.437'

##
#the name of the dictionary is  __version__
#the dictionary looks like  1.0


#the name of the dictionary is  __globals__
#the dictionary looks like  []

#Thus the data start from the 4th one, in python the count start from 0, thus the [3] one.


i=0
for name,data in mat_data.items():
    i+=1
    #print(i)
    if i == 4:
        print('the name of the dictionary is ', name)
        print('the data is', data)
        
        