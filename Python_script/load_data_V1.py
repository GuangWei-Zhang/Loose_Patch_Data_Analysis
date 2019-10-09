#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 23:16:47 2019

@author: zhangguangwei
"""

# first we need to load the data from the .mat file recorded using HEKA, which exported in .mat

# first we gonna try scipy as https://scipy-cookbook.readthedocs.io/items/Reading_mat_files.html

from scipy.io import loadmat
# I will first try plot the signal using ggplot
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from scipy.signal import butter, lfilter

def filter_data(data,low, high,sf, order =2):
    nyq =sf/2 
    low = low/nyq
    high = high/nyq
    b,a = butter(order,[low, high],btype ='band')
    
    filtered_data = lfilter(b,a,data)
    return filtered_data

def get_spikes(data, spike_window=80, tf=5, offset=10, max_thresh=350):

    # Calculate threshold based on data mean
    thresh = np.mean(np.abs(data)) *tf

    # Find positions wherere the threshold is crossed
    pos = np.where(data > thresh)[0]
    pos = pos[pos > spike_window]

    # Extract potential spikes and align them to the maximum
    spike_samp = []
    wave_form = np.empty([1, spike_window*2])
    for i in pos:
        if i < data.shape[0] - (spike_window+1):
            # Data from position where threshold is crossed to end of window
            tmp_waveform = data[i:i+spike_window*2]

            # Check if data in window is below upper threshold (artifact rejection)
            if np.max(tmp_waveform) < max_thresh:
                # Find sample with maximum data point in window
                tmp_samp = np.argmax(tmp_waveform) +i

                # Re-center window on maximum sample and shift it by offset
                tmp_waveform = data[tmp_samp-(spike_window-offset):tmp_samp+(spike_window+offset)]

                # Append data
                spike_samp = np.append(spike_samp, tmp_samp)
                wave_form = np.append(wave_form, tmp_waveform.reshape(1, spike_window*2), axis=0)

    # Remove duplicates
    ind = np.where(np.diff(spike_samp) > 1)[0]
    spike_samp = spike_samp[ind]
    wave_form = wave_form[ind]

    return spike_samp, wave_form



file_path = '/Users/zhangguangwei/Documents/GitHub/Loose_Patch_Data_Analysis/Test_data/A1_L4_Py/3.mat'
  
mat_data = loadmat(file_path)

sf = 10000

# Determine duration of recording in seconds
#dur_sec = data.shape[0]/sf

# Create time vector
#time = np.linspace(0, dur_sec,data.shape[0])


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

fig,ax=plt.subplots()

raw_data =[]
i=0
for name,data in mat_data.items():
    i+=1
    #print(i)
    
    #print('the name of the dictionary is ', name)
    if i >3:
        #print('the data is', data)
        raw_data = np.concatenate([raw_data,data[:,1]])

spike_data = filter_data(raw_data,low = 300, high = 3000, sf=sf)
        
ax.plot(spike_data)
plt.show()
 
spike_samp, wave_form = get_spikes(spike_data, spike_window=50, tf=8, offset=20)       
        
        
np.random.seed(10)
fig, ax = plt.subplots(figsize=(15, 5))

for i in range(100):
    spike = np.random.randint(0, wave_form.shape[0])
    ax.plot(wave_form[spike, :])

ax.set_xlim([0, 90])
ax.set_xlabel('# sample', fontsize=20)
ax.set_ylabel('amplitude [uV]', fontsize=20)
ax.set_title('spike waveforms', fontsize=23)
plt.show()