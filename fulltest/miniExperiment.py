import os
from pydub import AudioSegment

sample = AudioSegment.from_file('sci0222.wav')
sampleRange = open('sci0222.range', 'r').readlines()
noise = AudioSegment.from_file('noises/18fromSCI0222.wav')

# targets are the 20 ms frames in the .wav file that we will mix with
# 20 ms frames of some other noise
targets = [10, 30, 43, 55, 70]

precisionPacketSizes = []

# do the mixing as described above for each of the targets and
# save the mixed .wav files
for target in targets:
        adjustedTarget = sample[(target * 20):(target * 20 + 20)].overlay(noise)
        newSample = sample[:(target * 20)] + adjustedTarget + sample[(target * 20 + 20):]
        savedFile = 'workspace/' + str(target) + '+18sci0222.wav'
        newSample.export(savedFile, format="wav")
        # encode the mixed files with Opus
        rangeFile = savedFile[:-3] + 'range'
        opusFile = savedFile[:-3] + 'opus'
        os.system('opusenc --save-range {} {} {}'.format(rangeFile, savedFile, opusFile))
        # read the range files and store target packet sizes
        adjustedRange = open(rangeFile).readlines()
        lineCounter = 0
        for line in sampleRange:
            if lineCounter is target:
                oldSize = int(line[5:8].replace(',',' '))
                newSize = int(adjustedRange[lineCounter][5:8].replace(',',' '))
                precisionPacketSizes.append((oldSize, newSize))
            lineCounter += 1

repeatedNoisePacketSizes = []

# now mix the entire sample with the white noise
longerNoise = noise * (len(sample) // 20)
adjustedSample = sample.overlay(longerNoise)
anotherSavedFile = 'workspace/repeatedNoiseSample.wav'
adjustedSample.export(anotherSavedFile, format="wav")
rangeFile = anotherSavedFile[:-3] + 'range'
opusFile = anotherSavedFile[:-3] + 'opus'
os.system('opusenc --save-range {} {} {}'.format(rangeFile, anotherSavedFile, opusFile))
# read the range files and store target packet sizes
adjustedRange = open(rangeFile).readlines()
lineCounter = 0
for line in sampleRange:
            if lineCounter in targets:
                oldSize = int(line[5:8].replace(',',' '))
                newSize = int(adjustedRange[lineCounter][5:8].replace(',',' '))
                repeatedNoisePacketSizes.append((oldSize, newSize))
            lineCounter += 1

# output results
analysis = open('miniAnalysis3.txt', 'w')
analysis.write('Precision approach...\n')
for p in precisionPacketSizes:
    analysis.write(str(p[0]) + '->' + str(p[1]) + '\n')
analysis.write('Repeated approach...\n')
for p in repeatedNoisePacketSizes:
    analysis.write(str(p[0]) + '->' + str(p[1]) + '\n')
