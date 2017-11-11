import os
import random
from pydub import AudioSegment

sample = AudioSegment.from_file('sci0222.pcm', format="raw", sample_width=2, channels=1, frame_rate=48000)
noise = AudioSegment.from_file('20hzSinQuiet.pcm', format="raw", sample_width=2, channels=1, frame_rate=48000)
newSample = AudioSegment.empty()

for target in range(len(sample) // 20):
    gain = random.randint(0, 30)
    adjustedTarget = sample[(target * 20):(target * 20 + 20)].overlay(noise + gain)
    newSample = newSample + adjustedTarget
savedFile = 'sci0222+random20hzQuiet.wav'
newSample.export(savedFile, format="wav")
