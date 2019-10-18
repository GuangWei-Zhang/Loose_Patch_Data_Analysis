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

## following is the stimulus matrix, and count start from 0

stimulus = np.array([[101,261,221,469,517,269,501,69,525,205,365,477,373,117,13,485,165,533,29,541,285,549,149,133,509,197,453,397,445,413,173,421,213,61,93,253,317,277,429,341,301,493,77,109,461,45,381,53,21,333,85,565,293,181,237,189,229,349,389,37,357,405,5,557,309,325,245,125,157,141,437],
[527,119,79,327,375,127,359,495,383,63,223,335,231,543,439,343,23,391,455,399,143,407,7,559,367,55,311,255,303,271,31,279,71,487,519,111,175,135,287,199,159,351,503,535,319,471,239,479,447,191,511,423,151,39,95,47,87,207,247,463,215,263,431,415,167,183,103,551,15,567,295],
[385,545,505,185,233,553,217,353,241,489,81,193,89,401,297,201,449,249,313,257,1,265,433,417,225,481,169,113,161,129,457,137,497,345,377,537,33,561,145,57,17,209,361,393,177,329,97,337,305,49,369,281,9,465,521,473,513,65,105,321,73,121,289,273,25,41,529,409,441,425,153],
[243,403,363,43,91,411,75,211,99,347,507,51,515,259,155,59,307,107,171,115,427,123,291,275,83,339,27,539,19,555,315,563,355,203,235,395,459,419,3,483,443,67,219,251,35,187,523,195,163,475,227,139,435,323,379,331,371,491,531,179,499,547,147,131,451,467,387,267,299,283,11],
[30,190,150,398,446,198,430,566,454,134,294,406,302,46,510,414,94,462,526,470,214,478,78,62,438,126,382,326,374,342,102,350,142,558,22,182,246,206,358,270,230,422,6,38,390,542,310,550,518,262,14,494,222,110,166,118,158,278,318,534,286,334,502,486,238,254,174,54,86,70,366],
[456,48,8,256,304,56,288,424,312,560,152,264,160,472,368,272,520,320,384,328,72,336,504,488,296,552,240,184,232,200,528,208,0,416,448,40,104,64,216,128,88,280,432,464,248,400,168,408,376,120,440,352,80,536,24,544,16,136,176,392,144,192,360,344,96,112,32,480,512,496,224],
[172,332,292,540,20,340,4,140,28,276,436,548,444,188,84,556,236,36,100,44,356,52,220,204,12,268,524,468,516,484,244,492,284,132,164,324,388,348,500,412,372,564,148,180,532,116,452,124,92,404,156,68,364,252,308,260,300,420,460,108,428,476,76,60,380,396,316,196,228,212,508],
[314,474,434,114,162,482,146,282,170,418,10,122,18,330,226,130,378,178,242,186,498,194,362,346,154,410,98,42,90,58,386,66,426,274,306,466,530,490,74,554,514,138,290,322,106,258,26,266,234,546,298,210,506,394,450,402,442,562,34,250,2,50,218,202,522,538,458,338,370,354,82]])


TRF_matrix = np.zeros((8,71))
Rec_timeWin = 1500

for i in range(len(spike_samp)):
    if spike_samp[i]%1500>200:
        position_matrix_temp = (stimulus == int(spike_samp[i]/1500))
        TRF_matrix = TRF_matrix + position_matrix_temp
   
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(TRF_matrix)
plt.show()



## plot the raw response data for each intensity
def Intensity_plot(input_data,intensity,stimulus):
    intensity_num = int((70-intensity)/10)
    order_in_stimulus = stimulus[intensity_num,:]
    intensity_data = []
    
    for i in range(len(order_in_stimulus)):
        temp_order = order_in_stimulus[i]
        temp_data = input_data[temp_order*1500+200:(temp_order+1)*1500]
        intensity_data = np.append(intensity_data,np.zeros(300))
        intensity_data = np.append(intensity_data,temp_data)
        #intensity_data = [[intensity_data,temp_data]]
    return intensity_data

fig, ax = plt.subplots(8,1)

for i in range(8):
    intensity_data = Intensity_plot(spike_data,i*10,stimulus)
    


    
    fig, ax = plt.subplots(8,1,i)
    ax.plot(8,i+1,intensity_data)

plt.show()





