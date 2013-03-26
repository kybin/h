# coding=utf-8
import os
import re
import shutil
import posixpath as path
import filecmp
from itertools import count as itercount


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

def incBackup(inputpath, backupdirname ='backup', move=False):
    # check input
    src = convertToUnixpath(inputpath)
    
    if not path.exists(src):
        print('file not exists : {0}'.format(src))
        return False

    srcd, srcf = path.split(src)

    # check backup dir, path
    dstd = path.join(srcd, backupdirname)
    dstp = path.join(dstd, srcf)

    # create backup dir
    if not path.isdir(dstd):
        os.makedirs(dstd)
        print('create directory : {0}'.format(dstd))

    # inc filename
    dstl = incFromLastFile(dstp)

    if move:
        shutil.move(src, dstl)
    else:
        if path.isfile(src):
            shutil.copy(src, dstl)
        else:
            shutil.copytree(src, dstl)


def incFromLastFile(filepath):
    '''
    if file exist increment filename
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

