import os
import random
from pydub import AudioSegment

sample = AudioSegment.from_file('20hzSinLoud.wav')
savedFile = 'untouched20hz.wav'
sample.export(savedFile, format="wav")
