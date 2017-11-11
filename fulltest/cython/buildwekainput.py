import os

rootDir = 'voxforge'

# recursively go through directories and encode each .wav file with the option
# to save-range to a text file of the same name as the encoded sample

#for dirName, subdirList, fileList in os.walk(rootDir):
#    print('Found directory: {}'.format(dirName))
#    for fname in fileList:
#        if fname.endswith('.wav'):
#            print('Encoding {}'.format(fname))
#            rangefile = os.path.join(dirName, fname)[:-3] + 'range'
#            inputfile = os.path.join(dirName, fname)
#            outputfile = os.path.join(dirName, fname)[:-3] + 'opus'
#            os.system('opusenc --save-range {} {} {}'.format(rangefile, inputfile, outputfile))

# recursively go through the directories to extract packet sizes from save-range
# files, bin the sizes, and output .dat files with aabcaabcddefgghaae...

#for dirName, subdirList, fileList in os.walk(rootDir):
#    print('Found directory: {}'.format(dirName))
#    for fname in fileList:
#        if fname.endswith('.range'):
#            print('Parsing {}'.format(fname))
#            rangefile = os.path.join(dirName, fname)
#            outputfile = os.path.join(dirName, fname)[:-5] + 'dat'
#            input = open(rangefile, 'r')
#            output = open(outputfile, 'w')
#            for line in input:
#                sizetoken = line[5:8]
#                sizetoken = sizetoken.replace(',',' ')
#                if 0 <= int(sizetoken) < 100:
#                   output.write('0')
#                elif 100 <= int(sizetoken) < 135:
#                    output.write('1')
#                elif 135 <= int(sizetoken) < 170:
#                    output.write('2')
#                elif 170 <= int(sizetoken) < 205:
#                    output.write('3')
#                elif 205 <= int(sizetoken) < 240:
#                    output.write('4')
#                elif 240 <= int(sizetoken) < 275:
#                    output.write('5')
#                elif 275 <= int(sizetoken) < 310:
#                    output.write('6')
#                elif 310 <= int(sizetoken):
#                    output.write('7')
#                else: pass
#            input.close()
#            output.close()

# recursively go through the directories and create .csv files with unigrams, bigrams,
# and trigrams taken from the .dat files to be fed into Weka

wekafile = open('wekainput.csv', 'w')
for dirName, subdirList, fileList in os.walk(rootDir):
    print('Found directory: {}'.format(dirName))
    for fname in fileList:
        if fname.endswith('.dat'):
            print('Parsing {}'.format(fname))
            datfile = os.path.join(dirName, fname)
            input = open(datfile, 'r')
            total_count = 0
            unigrams = {x: 0 for x in range(8)}
            bigrams = {}
            trigrams = {}
            for x in range(8):
                for y in range(8):
                    key = str(x) + str(y)
                    bigrams[key] = 0
            for x in range(8):
                for y in range(8):
                    for z in range(8):
                        key = str(x) + str(y) + str(z)
                        trigrams[key] = 0
            last_lastch = '0'
            lastch = '0'
            for ch in input.read():
                    total_count += 1
                    unigrams[int(ch)] += 1
                    bigrams[lastch + ch] += 1
                    trigrams[last_lastch + lastch + ch] += 1
                    last_lastch = lastch
                    lastch = ch
            for i in range(8):
                wekafile.write(str(unigrams[i] / total_count) + ',')
            for k, v in bigrams.items():
                wekafile.write(str(v / total_count) + ',')
            for k, v in trigrams.items():
                wekafile.write(str(v / total_count) + ',')
            wekafile.write(fname[0:3] + '\n')
            input.close()
wekafile.close()
