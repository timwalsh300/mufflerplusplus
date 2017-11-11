import os
import random
from pydub import AudioSegment

sample = AudioSegment.from_file('sci0222.wav')
noise = AudioSegment.from_file('20hzSinQuiet.wav')
newSample = AudioSegment.empty()

for target in range(len(sample) // 20):
    gain = random.randint(0, 30)
    if gain == 0:
        adjustedTarget = sample[(target * 20):(target * 20 + 20)]
    else:
        adjustedTarget = sample[(target * 20):(target * 20 + 20)].overlay(noise + gain)
    newSample = newSample + adjustedTarget
savedFile = 'sci0222+random20hzQuiet.wav'
newSample.export(savedFile, format="wav")
