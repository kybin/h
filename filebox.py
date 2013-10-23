# coding=utf-8
import os
import re
import shutil
import os.path as path
import filecmp
from itertools import count as itercount

def clearScreen():
	if os.name == 'posix':
		os.system('clear')
	elif os.name == 'nt':
		os.system('cls')

def convertToUnixpath(inputpath):
    return inputpath.replace('\\', '/')

def prefix(filename):
    filename = re.sub('[_.]?v?\d*[.]\w+$', '', filename)
    return filename

def createdir(inputpath):
    if '/' in inputpath:
        filepath = path(inputpath)
        if filepath.existDir() == False:
            print('\n'+filepath.directory)
            os.makedirs(filepath.directory)

def opendir(dirpath):
    try:
        os.system('explorer '+dirpath)
    except:
        pass

def incBackup(inputpath, backupdir ='backup', move=False):
    if not path.exists(inputpath):
        print('file not exists : {0}'.format(inputpath))
        return False
    srcdir, srcfile = path.split(inputpath)
    backupdirpath = path.join(srcdir, backupdir)
    backupfile = path.join(backupdirpath, srcfile)

    if not path.isdir(backupdirpath):
        os.makedirs(backupdirpath)
        print('create directory : {0}'.format(backupdirpath))

    dstlast = incFromLastFile(backupfile)

    if move:
        shutil.move(inputpath, dstlast)
    else:
        if path.isfile(inputpath):
            shutil.copy(inputpath, dstlast)
        else: # dir
            shutil.copytree(inputpath, dstlast)


def incFromLastFile(filepath):
    '''
    if file exists increment filename
    '''
    if path.exists(filepath):
        base, ext = path.splitext(filepath)
        for v in itercount(1):
            newpath = base+'_'+str(v)+ext
            if not path.exists(newpath):
                return newpath
    return filepath

def mkdirSilent(d):
    try:
        os.makedirs(d)
    except OSError as err:
        if err.errno == 17:
            pass
        else:
            print("OS error({0}): {1}".format(e.errno, e.strerror))








# not completed
def __sortsequence(filelist):
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

