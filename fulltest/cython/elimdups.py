import os

rootDir = '.'
for dirName, subdirList, fileList in os.walk(rootDir):
    print('Found directory: {}'.format(dirName))
    for fname in fileList:
        if fname.endswith('_1.wav'):
            newfname = fname[0:2] + 'x' + fname[2:-6] + '.wav'
            os.system('mv {} {}'.format(fname, newfname))
