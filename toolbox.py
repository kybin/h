import os
import shutil
import filebox

def checkPadFromFiles(files, minpad=4):
    #if list of numbers in, this function calculate best padnum with that list"
    lenlist = [len(str(i)) for i in files]
    lenlist.sort()
    pad = inputlist[-1] + 1
        
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

