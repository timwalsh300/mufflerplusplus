sampleRange = open('sci0222.range', 'r')
packets = open('sci0222.packets', 'w')

for line in sampleRange:
    oldSize = int(line[5:8].replace(',',' '))
    packets.write(str(oldSize) + '\n')
