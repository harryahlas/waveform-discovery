#needs to run in spyder, not RStudio
# import os
# os.chdir("C:/Users/hahla/Desktop/github/waveform-discovery")

# import required libraries 
from pydub import AudioSegment  
from pydub.playback import play  
import numpy as np
# Import an audio file  
# Format parameter only 
# for readability  
audio_file = AudioSegment.from_file(file = "data/testgtr.mp3",format = "mp3")  
x = audio_file.get_array_of_samples()
import matplotlib.pyplot as plt 
plt.plot(x[10000:20010])

#play(wav_file)
 

type(x) 
len(x)

x1 = np.zeros(len(x))
x2 = np.zeros(len(x))
x3 = np.zeros(len(x))
x4 = np.zeros(len(x))
x5 = np.zeros(len(x))
x1[0:(len(x) - 1)] = np.diff(x)
x2[0:(len(x) - 2)] = x1[1:(len(x) - 1)]
x3[0:(len(x) - 4)] = x1[2:(len(x) - 2)]
x4[0:(len(x) - 6)] = x1[3:(len(x) - 3)]
x5[0:(len(x) - 8)] = x1[4:(len(x) - 4)]

# 3 steps (x is value, x1 is 2-1, x2 is 3-2)
y = np.column_stack((x1, x2))
unique, frequency = np.unique(y,
                              axis = 0,
                              return_counts = True) 
plt.hist(frequency, 100)
len(unique[frequency == 5,]) # not good

# 2 steps (x is value, x1 is 2-1)
#y = np.column_stack((x1))
unique, frequency = np.unique(x1,
                              axis = 0,
                              return_counts = True) 
plt.hist(frequency, 100)
len(unique[frequency > 3,])

## This is telling - 2 step drops that occur 3+ times
plt.hist(unique[frequency >= 3,], 100)


# General use
y = np.column_stack((x, x1, x2, x3, x4, x5))
unique, frequency = np.unique(y,
                              axis = 0,
                              return_counts = True) 

