import os
import copy
from pydub import AudioSegment
import encoder

# define a data structure to hold intermediate results
class target:
    def __init__(self, n):
        self.size = n
        self.instances = 0
        self.changeSummary = {x: 0 for x in range(0, 31) if x % 3 == 0}

    def newChange(self, gain, newSize):
        if gain is 0:
            self.instances += 1
        self.changeSummary[gain] += (newSize - self.size)

    def getChangeSummary(self):
        processedList = copy.copy(self.changeSummary)
        for k, v in processedList.items():
            if self.instances > 0:
                processedList[k] = v // self.instances
            else:
                processedList[k] = 0
        return processedList

# initialize a list of the above structures, one for each packet size we expect to
# encounter in the wild
targetStorage = []
for packetSize in range(50, 400):
    packet = target(packetSize)
    targetStorage.append(packet)

# write the results to a file
def writeResults():
    analysis = open('analysis.txt', 'w')
    for t2 in targetStorage:
        analysis.write('\n' + str(t2.size) + ': ' + str(t2.instances) + '\n')
        changes = t2.getChangeSummary()
        keys = list(sorted(changes.keys()))
        for k in keys:
            analysis.write('+' + str(k) + ': ' + str(changes[k]) + '\n')
    analysis.close()

# go through the dataset and get the results
noise = AudioSegment.from_file('noises/20hzSinQuiet.pcm', format="raw", frame_rate=48000, channels=1, sample_width=2)
for dirName, subdirList, fileList in os.walk('voxforgeSmall'):
    for fname in fileList:
        if fname.endswith('.pcm'):
            tester = encoder.Encoder()
            print('opening {}'.format(fname))
            sampleWav = AudioSegment.from_file(os.path.join(dirName, fname), format="raw", frame_rate=48000, channels=1, sample_width=2)
            # do the mixing for each of the targets and gain levels
            for target in range((len(sampleWav) // 20) + 1):
                print('working on target {}'.format(target))
                # get the original packet size for this target frame while
                # giving a target range of 50-400 to make the encoder state save/update after this call
                oldSize = tester.opus_encode(sampleWav[(target * 20):(target * 20 + 20)].get_array_of_samples(), 50, 400)
                gains = [x for x in range(0, 31) if x % 3 == 0]
                for gain in gains:
                    # create the mixed frame
                    adjustedTarget = sampleWav[(target * 20):(target * 20 + 20)].overlay(noise + gain)
                    adjustedTargetArray = adjustedTarget.get_array_of_samples()
                    # encode the mixed frame with Opus, and make sure the encoder state doesn't update afterwards
                    # by giving it a target range of 1000-1001 which should not be hit
                    result = tester.opus_encode(adjustedTargetArray, 1000, 1001)
                    # store the results of the new packet size vs. the original
                    targetStorage[oldSize - 50].newChange(gain, result)
writeResults()
