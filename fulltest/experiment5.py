import os
from pydub import AudioSegment

# define a data structure to hold intermediate results
class target:
    def __init__(self, n):
        self.size = n
        self.instances = 0
        self.changeSummary = []
        for i in range(21):
            self.changeSummary.append(0)

    def newChange(self, gain, newSize):
        if gain is 0:
            self.instances += 1
        self.changeSummary[gain] += (newSize - self.size)

    def getChangeSummary(self):
        processedList = []
        for i in range(21):
            if self.instances is 0:
                processedList.append(0)
            else:
                processedList.append(self.changeSummary[i] // self.instances)
        return processedList

# initialize a list of the above structures, one for each packet size we expect to
# encounter in the wild
targetStorage = []
for packetSize in range(100, 350):
    x = target(packetSize)
    targetStorage.append(x)

# write the results to a file
def writeResults():
    analysis = open('analysis.txt', 'w')
    for t2 in targetStorage:
        analysis.write('\n' + str(t2.size) + ': ' + str(t2.instances) + '\n')
        changes = t2.getChangeSummary()
        gain = 0
        for change in changes:
            analysis.write('+' + str(gain) + ': ' + str(change) + '\n')
            gain += 1
    analysis.close()

# go through the dataset and fill up the above list
noise = AudioSegment.from_file('noises/quiet18sci0222.wav')
for dirName, subdirList, fileList in os.walk('voxforgeSmall'):
    for fname in fileList:
        if fname.endswith('.wav'):
            print('opening {}'.format(fname))
            sampleWav = AudioSegment.from_file(os.path.join(dirName, fname))
            sampleRange = open(os.path.join(dirName, fname[:-3] + 'range')).readlines()
            # do the mixing for each of the targets and save the mixed .wav files
            for target in range((len(sampleWav) // 20) + 1):
                print('working on target {}'.format(target))
                for gain in range(21):
                    adjustedTarget = sampleWav[(target * 20):(target * 20 + 20)].overlay(noise + gain)
                    newSample = sampleWav[:(target * 20)] + adjustedTarget + sampleWav[(target * 20 + 20):]
                    savedFile = 'workspace/' + str(target) + fname + '+18sci0222.wav'
                    newSample.export(savedFile, format="wav")
                    # encode the mixed file with Opus
                    rangeFile = savedFile[:-3] + 'range'
                    opusFile = savedFile[:-3] + 'opus'
                    os.system('opusenc --save-range {} {} {}'.format(rangeFile, savedFile, opusFile))
                    # compare the new packet sizes with those of the original sample
                    newRange = open(rangeFile, 'r').readlines()
                    oldSize = int(sampleRange[target][5:8].replace(',',' '))
                    newSize = int(newRange[target][5:8].replace(',',' '))
                    targetStorage[oldSize - 100].newChange(gain, newSize)
                    # clean up so we don't run out of disk space
                    os.system('rm {}'.format(rangeFile))
                    os.system('rm {}'.format(savedFile))
                    os.system('rm {}'.format(opusFile))
writeResults()
