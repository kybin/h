import os
import shutil
import filebox
reload(filebox)

def checkPadnumFromList(inputlist, minpad=4):
    #if list of numbers in, this function calculate best padnum with that list"
    lenlist = [len(str(i)) for i in inputlist]
    lenlist.sort()
    pad = inputlist[-1]+1
        
    if pad < minpad:
        pad = minpad
    
    return pad

def padding(numstring, padnum = 4):
    if type(numstring) == int:
        numstring = str(numstring)
        
    newstring = ''.join(["0"*(padnum - len(numstring)), numstring])
    return newstring
    


def opendir(path):
    try:
        openDir = os.listdir(path)
        os.system("expolorer "+path)
    except:
        pass








##################################################
# These functions are moved on filebox. DEPRECATED
##################################################
def createdir(inputpath):
    if '/' in inputpath:
        filepath = filebox.path(inputpath)
        if filepath.existDir() == False:
            print('\n'+filepath.directory)
            os.makedirs(filepath.directory)



##################################################
# These functions are moved on filebox. DEPRECATED
##################################################
def incBackup(filepath, backupfolder ="backup"):
    
    source = filebox.path(filepath)
    sourcename = source.nameWithoutExtension
    sourceext = source.extension
    sourcepath = source.path
    sourcedir = source.directory
    backuppath = "/".join([sourcedir, backupfolder])

    success = 0
    if source.existParentDir():
        if not source.existDir(): 
            os.makedirs(sourcedir)
        if not source.exist():
            open(sourcepath, 'w').close()
        if not os.path.isdir(backuppath):
            os.makedirs(backuppath)
        success = 1
    else:
        print("don't have parent path")

    if success == 1:
        backupfiles = [file for file in os.listdir(backuppath) if file.startswith("{filename}_backup".format(filename=sourcename))]    
        if len(backupfiles)==0:
            shutil.copyfile(sourcepath, "/".join([backuppath, "{filename}_backup1.{ext}".format(filename=sourcename, ext=sourceext)]))        
        else:
            backupfiles.sort()
            lastfile = backupfiles[-1]
            lastfilename = lastfile.rstrip(".{0}".format(sourceext)) 
            lastfilepath = "/".join([backuppath, lastfile])
            lastdigit = int(lastfilename.lstrip("{filename}_backup".format(filename=sourcename, ext=sourceext)))
            destfilename = "".join([sourcename, "_backup", str(lastdigit+1), ".", sourceext])
            destfilepath = "/".join([backuppath, destfilename])

            if (os.path.getsize(sourcepath) != os.path.getsize(lastfilepath)) or (open(sourcepath,'r').read() != open(lastfilepath,'r').read()):
                shutil.copyfile(sourcepath, destfilepath)        
            else:
                pass # Do Nothing

