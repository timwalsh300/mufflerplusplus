import os
import random
from pydub import AudioSegment

sample = AudioSegment.from_file('20hzSinLoud.wav')
newSample = sample[:1]

for target in range(len(sample) // 20):
    gain = random.randint(-100, 100)
    adjustedTarget = sample[(target * 20):(target * 20 + 20)] + gain
    newSample = newSample + adjustedTarget
savedFile = 'randomlyAdjusted20hz.wav'
newSample.export(savedFile, format="wav")
