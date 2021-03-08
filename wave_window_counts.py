#needs to run in spyder, not RStudio

# import required libraries 
from pydub import AudioSegment  
from pydub.playback import play  
  
# Import an audio file  
# Format parameter only 
# for readability  
wav_file = AudioSegment.from_file(file = "C:\\Users\\hahla\\Desktop\\github\\waveform-discovery\\data\\testgtr.mp3",format = "mp3" )  
x = wav_file.get_array_of_samples()
import matplotlib.pyplot as plt 
plt.plot(x[10000:20010])
plt.show()

play(wav_file)
 
type(x) 
len(x)

# data type fo the file 
print(type(wav_file))  

#  To find frame rate of song/file 
print(wav_file.frame_rate)    

# To know about channels of file 
print(wav_file.channels)  

# Find the number of bytes per sample  
print(wav_file.sample_width )  

# Find Maximum amplitude  
print(wav_file.max) 

# To know length of audio file 
print(len(wav_file)) 

''' 
We can change the attrinbutes of file by  
changeed_audio_segment = audio_segment.set_ATTRIBUTENAME(x)  
'''
wav_file_new = wav_file.set_frame_rate(50)  
print(wav_file_new.frame_rate) 


x = wav_file.get_array_of_samples()
import matplotlib.pyplot as plt 
plt.plot(x[0:100000])
plt.show()
plt.close()
