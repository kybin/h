# coding=utf-8
import os
import sys
import re
import shutil
import os.path as ospath
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
		filepath = ospath(inputpath)
		if filepath.existDir() == False:
			print('\n'+filepath.directory)
			os.makedirs(filepath.directory)

def opendir(d):
	if sys.platform=='win32':
		subprocess.Popen(['start', d], shell=True)
	elif sys.platform=='darwin':
		subprocess.Popen(['open', d])
	else:
		try:
			# xdg-open should be supported by recent Linux
			subprocess.Popen(['xdg-open', d])
		except OSError:
			raise OSError("cannot find your file manager, sorry.")


def incBackup(inputpath, backupdirname ='backup', move=False):
	if not ospath.exists(inputpath):
		raise OSError('file not exists : {0}'.format(inputpath))
	indir, infile = ospath.split(inputpath)
	backupdir = ospath.join(indir, backupdirname)
	backupfile = ospath.join(backupdir, infile)

	if not ospath.isdir(backupdir):
		os.makedirs(backupdir)
		print('create directory : {0}'.format(backupdir))
		raw_input()

	lastf = incFromLastFile(backupfile)
	if move:
		shutil.move(inputpath, lastf)
	else:
		if ospath.isfile(inputpath):
			shutil.copy(inputpath, lastf)
		else: # dir
			shutil.copytree(inputpath, lastf)


def incFromLastFile(filepath):
	'''
	if file exists increment filename
	'''
	if ospath.exists(filepath):
		base, ext = ospath.splitext(filepath)
		for v in itercount(1):
			newpath = base+'_'+str(v)+ext
			if not ospath.exists(newpath):
				return newpath
	return filepath

def mkdirSilent(d):
	try:
		os.makedirs(d)
	except OSError as err:
		if err.errno == 17:
			pass
		else:
			raise OSError("OS error({0}): {1}".format(e.errno, e.strerror))








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

