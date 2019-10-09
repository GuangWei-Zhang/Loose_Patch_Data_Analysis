#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 23:16:47 2019

@author: zhangguangwei
"""

# first we need to load the data from the .mat file recorded using HEKA, which exported in .mat

# first we gonna try scipy as https://scipy-cookbook.readthedocs.io/items/Reading_mat_files.html

from scipy.io import loadmat
from tkinter.filedialog import askopenfilenames
from tkinter import Tk
import os

file_path = '/Users/zhangguangwei/Documents/GitHub/Loose_Patch_Data_Analysis/Test_data/A1_L4_Py/3.mat'
  
mat_data = loadmat(file_path)