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
for dirName, subdirList, fileList in os.walk('voxforge'):
    for fname in fileList:
        if fname.endswith('.wav'):
            sampleWav = AudioSegment.from_file(os.path.join(dirName, fname))
            sampleRange = open(os.path.join(dirName, fname[:-3] + 'range')).readlines()
            # mix the whole sample with noise at a range of amplitudes
            for i in range(21):
                adjustedNoise = (noise + i) * (len(sampleWav) // 20)
                newSample = sampleWav.overlay(adjustedNoise)
                outmix = 'workspace/' + fname[:-4] + '+18sci0222+' + str(i) + '.wav'
                newSample.export(outmix, format="wav")
                # encoded the newly mixed file
                rangefile = outmix[:-3] + 'range'
                encodedfile = outmix[:-3] + 'opus'
                os.system('opusenc --save-range {} {} {}'.format(rangefile, outmix, encodedfile))
                # compare the new packet sizes with those of the original sample
                newRange = open(rangefile, 'r')
                lineCounter = 0
                for line in newRange:
                    if lineCounter < len(sampleRange):
                        oldSize = int(sampleRange[lineCounter][5:8].replace(',',' '))
                        newSize = int(line[5:8].replace(',',' '))
                        if oldSize >= 100:
                            targetStorage[oldSize - 100].newChange(i, newSize)
                    lineCounter += 1
                # clean up so we don't run out of disk space
                os.system('rm {}'.format(rangefile))
                os.system('rm {}'.format(outmix))
                os.system('rm {}'.format(encodedfile))
                newRange.close()
                writeResults()
