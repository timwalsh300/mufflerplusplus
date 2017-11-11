import os
import random
from pydub import AudioSegment

sample = AudioSegment.from_file('20hzSinLoud.wav')
newSample = sample[:1]

for target in range(len(sample) // 20):
    adjustedTarget = sample[(target * 20):(target * 20 + 20)]
    newSample = newSample + adjustedTarget
savedFile = 'sliced20hz.wav'
newSample.export(savedFile, format="wav")
