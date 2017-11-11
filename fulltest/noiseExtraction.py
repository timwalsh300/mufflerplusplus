import os
from pydub import AudioSegment

sample = AudioSegment.from_file('sci0222.wav')

targets = [18, 30]

for target in targets:
        extractedFrame = sample[(target * 20):(target * 20 + 20)]
        print(str(len(extractedFrame)))
        savedFile = 'workspace/' + str(target) + 'fromSCI0222.wav'
        extractedFrame.export(savedFile, format="wav")
        # encode the mixed files with Opus
        rangeFile = savedFile[:-3] + 'range'
        opusFile = savedFile[:-3] + 'opus'
        os.system('opusenc --save-range {} {} {}'.format(rangeFile, savedFile, opusFile))
