

import os
import re
import toolbox


os.chdir('c:/tmp/cg1290')
filelist = os.listdir('.')

extobject = re.compile('.jpe*g$')
filelist = [file for file in filelist if fileobject.findall(file)] # cull jpg file list

replaceobejct = re.compile('[._](\d+).pts')
splitobject = re.compile('[._]+')
replaceobject.match('thisis.0005.pts')


splitlist = [splitobject.split(file)[-2:] for file in filelist]

frameList = [int(i[-2]) for i in splitlist]

frames = frameList

frames.sort()
lowestframe = frames[0]

newFrameList = [(frame-lowestframe+1) for frame in frameList]
print newFrameList
test
padnum = toolkit.checkPadnumFromList(newFrameList)
paddedFrameList = [toolkit.padding(frame, padnum) for frame in newFrameList]

newset = zip(paddedFrameList, filelist)

newList = []
for newframe, eachfile in newset:
    newname = frameobject.sub(newframe, eachfile)
    newList.append(newname)

# print newList