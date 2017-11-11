import os
from pydub import AudioSegment
import encoder

# go through the dataset and create .dat files that contain abcdefghabcegabgh... etc.
for dirName, subdirList, fileList in os.walk('voxforge'):
    for fname in fileList:
        if fname.endswith('.pcm'):
            tester = encoder.Encoder()
            print('opening {}'.format(fname))
            sampleWav = AudioSegment.from_file(os.path.join(dirName, fname), format="raw", frame_rate=48000, channels=1, sample_width=2)
            filename = fname[:-3] + 'dat'
            outputFile = open('voxforge/' + filename, 'w')
            # isolate each 20 ms frame
            for target in range((len(sampleWav) // 20) + 1):
                print('working on target {}'.format(target))
                # get the packet size for this target frame while
                # giving a target range of 50-400 to make the encoder state save/update after this call
                oldSize = tester.opus_encode(sampleWav[(target * 20):(target * 20 + 20)].get_array_of_samples(), 50, 400)
                if oldSize <= 100:
                    outputFile.write('a')
                elif 100 < oldSize <= 140:
                    outputFile.write('b')
                elif 140 < oldSize <= 180:
                    outputFile.write('c')
                elif 180 < oldSize <= 220:
                    outputFile.write('d')
                elif 220 < oldSize <= 260:
                    outputFile.write('e')
                elif 260 < oldSize <= 300:
                    outputFile.write('f')
                elif 300 < oldSize <= 340:
                    outputFile.write('g')
                elif 340 < oldSize:
                    outputFile.write('h')
            outputFile.close()
