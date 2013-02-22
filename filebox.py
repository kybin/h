# coding=utf-8

import os
import re
import shutil

class path:
    def __init__(self, inputpath):
        self.inputpath = inputpath
        self.path = inputpath.replace('\\', '/')
        lastpath = self.path.split('/')[-1]

        if '.' in lastpath:
            self.name = lastpath
            self.nameWithoutExtension = '.'.join(lastpath.split('.')[:-1])
            self.extension = lastpath.split('.')[-1]
            self.directory = '/'.join(self.path.split('/')[:-1])
            self.parentdir = '/'.join(self.path.split('/')[:-2])
        else: # if input is a directory path
            self.name = ''
            self.extension = ''
            self.nameWithoutExtension = ''
            self.directory = self.path
            self.parentdir = '/'.join(self.path.split('/')[:-1])
    def exist(self):
        return os.path.isfile(self.path)

    def existDir(self):
        return os.path.isdir(self.directory)

    def existParentDir(self):
        return os.path.isdir(self.parentdir)

def unixpath(inputpath):
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


def opendir(path):
    try:
        # openDir = os.listdir(path)
        os.system('explorer '+path)
    except:
        pass

def incBackup(inputpath, backupDirectory ='backup', backupName=None):
    # input : file path for backup
    # results : save file incrementally

    filepath = unixpath(inputpath)
    dirpath = path(filepath).directory
    basename = path(filepath).nameWithoutExtension
    ext = path(filepath).extension

    backupdir = '/'.join([dirpath, backupDirectory])

    if not os.path.isfile(filepath):
        print('file not exists : {path}'.format(path=filepath))
        return False

    if not os.path.isdir(backupdir):
        os.makedirs(backupdir)
        print('create directory : {backupdir}'.foramt(backupdir=backupdir))

    backupfiles = [f for f in os.listdir(backupdir) if f.startswith('{filename}_backup'.format(filename=basename))]
    try:
        backupfiles.sort()
        lastfile = backupfiles.pop()
        lastpath = '/'.join([backupdir, lastfile])
        lastdigit = int(re.findall('(\d+)[.]\w+$', lastfile)[0])
    except:
        lastfile = None
        lastdigit = 0
  
    incname = '{basename}_backup{num}.{ext}'.format(basename=basename, num=str(lastdigit+1), ext=ext)
    incpath = '/'.join([backupdir, incname])

    if lastfile and (os.path.getsize(filepath) != os.path.getsize(lastpath)) or (open(filepath,'r').read() != open(lastpath,'r').read()):
        shutil.copyfile(filepath, incpath)

