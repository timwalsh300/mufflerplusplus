import os

rootDir = '.'
for dirName, subdirList, fileList in os.walk(rootDir):
    print('Found directory: {}'.format(dirName))
    for fname in fileList:
        if fname.endswith('.wav'):
            print('Encoding {}'.format(fname))
            inputfile = os.path.join(dirName, fname)
            outputfile = os.path.join(dirName, fname)[:-3] + 'pcm'
            os.system('ffmpeg -i {} -f s16le {}'.format(inputfile, outputfile))
