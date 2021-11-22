'''import sounddevice as sd


duration = 1  # seconds
fs = 44100
print(sd.query_devices())
sd.default.device = 0, 1
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)  
print(sum(myrecording[0]))
sd.play(myrecording, fs)'''  

import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

fs=44100
duration = 5  # seconds
myrecording = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
print(sd.query_devices())
sd.default.device = 0, 1
print("Recording Audio")
sd.wait()
print("Audio recording complete , Play Audio")
sd.play(myrecording, fs)
sd.wait()
print("Play Audio Complete")