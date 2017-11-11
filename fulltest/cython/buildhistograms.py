import os

rootDir = '.'

# recursively go through the directories to extract packet sizes from save-range
# files, bin the sizes, and write histograms to depict the distribution

for dirName, subdirList, fileList in os.walk(rootDir):
    print('Found directory: {}'.format(dirName))
    for fname in fileList:
        if fname.endswith('.range'):
            print('Parsing {}'.format(fname))
            rangefile = os.path.join(dirName, fname)
            outputfile = os.path.join(dirName, fname)[:-5] + 'hist'
            input = open(rangefile, 'r')
            output = open(outputfile, 'w')
            distribution = {'a': 0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0}
            totalPackets = 0
            for line in input:
                sizetoken = line[5:8]
                sizetoken = sizetoken.replace(',',' ')
                totalPackets += 1
                if 0 <= int(sizetoken) < 100:
                    distribution['a'] += 1
                elif 100 <= int(sizetoken) < 135:
                    distribution['b'] += 1
                elif 135 <= int(sizetoken) < 170:
                    distribution['c'] += 1
                elif 170 <= int(sizetoken) < 205:
                    distribution['d'] += 1
                elif 205 <= int(sizetoken) < 240:
                    distribution['e'] += 1
                elif 240 <= int(sizetoken) < 275:
                    distribution['f'] += 1
                elif 275 <= int(sizetoken) < 310:
                    distribution['g'] += 1
                elif 310 <= int(sizetoken):
                    distribution['h'] += 1
                else: pass
            output.write('{} total packets: {}\n\n'.format(fname, str(totalPackets)))
            for k, v in distribution:
                output.write('{}: {} '.format(k, str(v)) + 'x' * int(10 * v / totalPackets) + '\n')
            input.close()
            output.close()
