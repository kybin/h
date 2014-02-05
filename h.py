#!/usr/bin/python
# coding:utf-8

import os
import sys
import re
import os.path as ospath
import time
import pickle
import shutil
import itertools
from subprocess import call

#import env
import maketree
import filebox
import softwareinfo
from OrderedDict import OrderedDict

class shotdata:
	def __init__(self, user, part, rootpath):
		self.version = '0.02'
		self.part = part
		self.user = user
		self.rootpath = rootpath
		self.workingdir = rootpath
		self.software = softwareinfo.softwareinfo
		self.use = 'houdini'
		self.renderdir = 'render'
		self.structfile = '.showinfo'
		self.lastrundir = ''
		self.lastruntask = ''
		self.lastrunfile = ''
		self.items=[]
		self.log = ''
		self.showlog=True
		self.initStruct()


	# struct
	def initStruct(self):
		self.struct = OrderedDict([
			('root', self.rootpath),
			('show'	, ''),
			('work'	, 'work'),
			# -------------------------------------------------
			# these levels could deleted depends on show struct
			('seq'	, ''),
			('scene', ''),
			('shot'	, ''),
			# -------------------------------------------------
			('run', 'scenes'),
			('task'	, ''),
			('rev'	, '')
			])
		self.head = 'root'
		self.showStruct = set(['seq', 'scene', 'shot'])
		self.bypassStruct = ['work','run']
		self.printStruct = ['show', 'seq', 'scene', 'shot', 'task', 'rev']

	# update
	def update(self):
		''' update working directory and item list. '''
		head = self.head
		#self.writeLog(head)
		if head == 'root':
			self.initStruct()
		if head == 'show':
			self.updateShow()
		self.updateDir()
		self.updateItems()

	def updateShow(self):
		''' reads '.showinfo' file in the show directory, checking it's structure, then delete unused level. '''
		structfile = ospath.join(self.rootpath, self.struct['show'], '.showinfo')
		self.writeLog("{} imported".format(structfile))

		with open(structfile) as f:
			read = f.readline()
			self.writeLog("reset struct to {}".format(read))
			readStruct = set(read.strip('\n').split('/'))

			delStruct = self.showStruct - readStruct
			if delStruct:
				self.writeLog("{} will be deleted".format(" ,".join(delStruct)))
			else:
				self.writeLog("Nothing will be deleted")

			for level in delStruct:
				del self.struct[level]

	def updateDir(self):
		''' Tasks and revs are not a dir, so we have to set our last dir '''
		struct = self.struct
		dirindex = min(self.currentHeadIndex(), struct.keys().index('run'))
		workingdir = ospath.join(*struct.values()[:dirindex+1])
		print(workingdir)
		if os.path.isdir(workingdir):
			self.workingdir = workingdir
		else:
			raise ValueError("Cannot find working directory : {0}".format(workingdir))

	def updateItems(self):
		''' update items (files and directories) in current directory'''
		items = os.listdir(self.workingdir)
		items = self.itemculling(items)
		if self.currentHeadIndex() <= self.headIndex('shot'):
			items = self.directories(items)
		elif self.head == 'run':
			items = self.tasks(items)
			self.struct['task']=items
		elif self.head == 'task':
			items = self.revs(items, self.struct['task'])
		else:
			raise KeyError('head is in a danger area! : {0}'.format(head))
		self.items = items


	# print
	def printMessage(self):
		filebox.clearScreen()
		print('='*75)
		print('Shot Manager V{version}'.format(version=self.version).center(75))
		print('user : {0}, part : {1}'.format(self.user, self.part).rjust(75))
		print('='*75)

		print('{0}'.format(self.workingdir).rjust(75))

		for s, v in self.struct.items()[self.headIndex('show'):self.currentHeadIndex()+1]:
			if s not in self.bypassStruct:
				print('{0: >8} : {1}'.format(s.upper(), v))

		print('<{0}>'.format(self.nextHead().upper()))
		items = [' : '.join(['{0: >4}'.format(idx+1),val]) for idx,val in enumerate(self.items)]
		print('\n'.join(items))
		print('-'*75)

		if self.showlog and self.log:
			print(self.log)
			print('-'*75)

		print('>>>'),

	def printHelp(self):
		filebox.clearScreen()
		print
		print('-'*75)
		print('HELP')
		print('-'*75)
		print('go inside : (num)')
		print('go up one level : (..)')
		print('go to the top : (/)')
		print
		print('new item : (new)')
		print('ex - (new sc01) or (new task1)')
		print
		print('open directory : (o) or (open)')
		print
		print('change software : (use)')
		print('if you want to change to maya    : (use maya)')
		print('if you want to change to max     : (use max)')
		print('if you want to change to houdini : (use houdini)')
		print('-'*75)
		print
		print('>>> Enter to close help.'),
		raw_input()

	# action
	def action(self, userInput):
		u = userInput.strip().lower() # strip and force change to lower string

		if (not u) or (u in ['help', '/?', '/help']):
			self.printHelp()
		elif u in ['q', 'quit', 'exit']:
			sys.exit('Bye!')
		elif u in ['o', 'open']:
			self.opendir()
		elif u.startswith('use '):
			change, sw = u.split(' ')
			self.changesoftware(sw)
		elif u.startswith('part '):
			self.part = u.split()[1]
		elif u.startswith('user '):
			self.user = u.split()[1]
		elif u.startswith('del '):
			item = u.split()[1]
			self.delete(item)
		elif u.startswith('omit '):
			item = u.split()[1]
			self.omit(item)
		elif u.startswith('new '):
			names = u.split()[1:]
			for n in names:
				print(n)
				self.new(n)
		elif u.startswith('log '):
			if u.split()[1] == 'on':
				self.logOn()
			elif u.split()[1] == 'off':
				self.logOff()
			else:
				self.writeLog("you can do 'log on' or 'log off'")
		elif u=='`':
			self.runLastTask()
		elif u=='~':
			self.runLastFile()
		elif u == '.':
			pass # Copy directory path to the clipboard

 		else: # Throw any other input to move(), so they can handle it
			self.move(u)

	# cull
	def itemculling(self, items):
		'''Any directory or file starts with . or _ will not display'''
		culls = [i for i in items if not (i.startswith('.') or i.startswith('_'))]
		return culls

	def directories(self, items):
		'''It takes current path's items, then only return directories'''
		dirs = sorted([i for i in items if ospath.isdir(ospath.join(self.workingdir,i))])
		return dirs

	def tasks(self, items):
		''' check the software we are using, then throw files for other software '''
		files = [i for i in items if ospath.isfile(ospath.join(self.workingdir,i))]
		validFiles = [] # matched file for software user currently use.

		exts = self.software[self.use]['read']
		for e in exts:
			validFiles += [f for f in files if e in f]

		rest = re.compile('[-_.]?v?\d*[.]\w+$')
		tasksAndOthers = [rest.sub('', i) for i in validFiles]
		tasksAndOthers = sorted(list(set(tasksAndOthers)))

		shotpath = self.fileprepath()
		tasks = [t[len(shotpath)+1:] for t in tasksAndOthers if t.startswith(shotpath)]

		return tasks

	def revs(self, items, task):
		revs = [i for i in items if i.startswith(task)]
		revs = sorted(list(set(revs)))
		revs.reverse()
		return revs


	# head - "head" means "Current Level"
	def headIndex(self, head):
		return self.struct.keys().index(head)

	def currentHeadIndex(self):
		return self.headIndex(self.head)

	def headShift(self, shift):
		self.head = self.struct.keys()[self.currentHeadIndex()+shift]

	def currentHead(self):
		return self.struct.keys()[self.currentHeadIndex()]

	def nextHead(self, head=None):
		try:
			return self.struct.keys()[self.currentHeadIndex()+1]
		except IndexError:
			return None

	def prevHead(self, head=None):
		try:
			return self.struct.keys()[self.currentHeadIndex()-1]
		except IndexError:
			return None

	def setHeadData(self, data):
		self.struct[self.head]=data

	def clearHeadData(self):
		self.struct[self.head]=''

	# move
	def move(self, inputstring):
		lowerinput = inputstring.lower()
		loweritems = [i.lower() for i in self.items]
		if inputstring == '..':
			self.up()
		elif inputstring == '/':
			self.top()
		elif inputstring.isdigit():
			select = int(inputstring)-1
			if 0 <= select < len(self.items):
				self.down(self.items[select])
			else:
				self.writeLog('invalid number : {0}'.format(inputstring))
		elif lowerinput in loweritems:
				i = loweritems.index(lowerinput)
				self.down(self.items[i])
		else:
			self.writeLog('invalid input : {0}'.format(inputstring))

	def top(self):
		self.head = 'root'
		#self.initStruct()

	def up(self):
		struct = self.struct
		if self.head in self.bypassStruct:
			while self.head in self.bypassStruct:
				self.headShift(-1)
		self.clearHeadData()
		if self.head != 'root':
			self.headShift(-1)

	def down(self, dest):
		struct = self.struct
		if self.nextHead() == 'task':
			self.runTask(self.workingdir, dest)
		elif self.nextHead() == 'rev':
			self.runRev(dest)
		else:
			self.headShift(1)
			self.setHeadData(dest)
			self.update() # there are chances to skip update, so force update
			while self.nextHead() in self.bypassStruct:
				self.headShift(1)
		print(self.head)


	# run
	def runTask(self, dir, task):
		flist = os.listdir(dir)
		shot = self.fileprepath()
		flist = sorted([f for f in flist if f.startswith(shot+'.'+task)])
		flist.reverse()
		lastf = flist[0]
		lastfpath = ospath.join(self.workingdir, lastf)
		self.lastrundir = dir
		self.lastruntask = task
		self.lastrunfile = lastfpath
		os.system('{0} {1}'.format(self.software[self.use]['execute'], lastfpath))

	def runFile(self, file):
		print(self.use, self.software[self.use])
		os.system('{0} {1}'.format(self.software[self.use]['execute'], file))

	def runLastTask(self):
		if self.lastrundir and self.lastruntask:
			self.runTask(self.lastrundir, self.lastruntask)
		else:
			self.writeLog('Could not find last task! Maybe its your first time to use this program... or not? :)')

	def runLastFile(self):
		if self.lastrunfile:
			self.runFile(self.lastrunfile)


	# new
	def new(self, name):
		nexthead = self.nextHead()
		if   nexthead in ['show']:
			self.newshow(name)
		elif nexthead in ['seq', 'scene']:
			self.newdir(name)
		elif nexthead in ['shot']:
			self.newshot(name)
		elif nexthead in ['task', 'rev']:
			self.newtask(name)

	def newdir(self, dirname):
		nd = ospath.join(self.workingdir, dirname)
		os.mkdir(nd)

	def newshow(self, showname):
		''' this will make show struct directories and info (.showinfo) file'''
		A, B, C = 'seq/scene/shot', 'scene/shot', 'shot'
		print('choose one of these types')
		print('1. show/' + A)
		print('2. show/' + B)
		print('3. show/' + C)
		userinput = raw_input()
		if userinput not in ['1', '2', '3']:
			self.log+='intput invalid, please type 1-3'
			return
		else:
			showtype = [A, B, C][int(userinput)-1]
		showpath = ospath.join(self.workingdir, showname)
		os.mkdir(showpath)
		maketree.make('show', showpath)
		self.log+=showtype
		self.log+=showpath
		self.makeShowInfoFile(showtype, showpath)

	def makeShowInfoFile(self, showtype, showpath):
		showfile = ospath.join(showpath, '.showinfo')
		with open(showfile, 'w') as f:
			f.write(showtype)

	def newshot(self, shot):
		path = ospath.join(self.workingdir, shot)
		os.mkdir(path)
		maketree.make('shot', path)

	def newtask(self, taskname):
		struct = self.struct
		structname = self.structname
		structpath = self.structpath
		filename = '.'.join([self.fileprepath(), taskname, 'v101', self.software[self.use]['write']])
		filepath = ospath.join(self.workingdir, filename)
		shotpath = self.shotpath()
		renderpath = self.renderpath()
		startf, endf, fps = 1, 240, 24.0

		initscript = self.software[self.use]['initscript'].format(
			show=structname('show'),
			seq=structname('seq'),
			scene=structname('scene'),
			shot=structname('shot'),
			task=taskname,
			showpath = structpath('show'),
			seqpath=structpath('seq'),
			scenepath=structpath('scene'),
			taskpath=structpath('run'),
			shotpath=shotpath,
			renderpath=renderpath,
			filepath=filepath,
			fps=24, start=(startf-1)/fps, end=endf/fps
		)
		scriptfile = ospath.join(self.workingdir, '.temp_init')
		with open(scriptfile, 'w') as f:
			f.write(initscript)

		command = self.software[self.use]['batch'] + ' ' + scriptfile
		# command = self.software[self.use]['batch'].format(filepath=filepath) + ' ' + scriptfile
		self.writeLog("running setup script.. : {}".format(command))
		os.system(command)
		os.remove(scriptfile)
		self.runFile(filepath)


	# other actions
	def opendir(self):
		dir = self.workingdir
		os.system('thunar {dir}'.format(dir=dir))

	def changesoftware(self, sw):
		if sw in self.software:
			self.use = sw
			# self.struct['software'] = self.software[self.use]['dir']
		else:
			print("there isn't such a software")

	def delete(self, item):
		''' Move items to '_deleted' directory '''
		itempath = ospath.join(self.workingdir, item)
		filebox.incBackup(itempath, backupdirname ='_deleted', move=True)

	def omit(self, item):
		''' Move items to '_omitted' directory '''
		itempath = ospath.join(self.workingdir, item)
		filebox.incBackup(itempath, backupdirname ='_omitted', move=True)

	def writeLog(self, comment):
		if self.log:
			self.log+='\n'
		self.log+="{}".format(comment)

	def clearLog(self):
		self.log=''

	def logOn(self):
		self.showlog=True

	def logOff(self):
		self.showlog=False

	# utility
	def structname(self, structname):
		try:
			return self.struct[structname]
		except KeyError:
			return ''

	def structpath(self, structname):
		struct = self.struct
		try:
			idx = struct.keys().index(structname)
		except ValueError:
			return ''

		paths = struct.values()[:idx+1]
		structpath = []
		for p in paths:
			structpath.append(p)
		# print(structpath)
		return('/'.join(structpath))

	def fileprepath(self):
		prepath = []
		struct = self.struct
		showidx, shotidx = struct.keys().index('show'), struct.keys().index('shot')
		paths = struct.values()[showidx : shotidx+1]
		for p in paths:
			if not p in self.bypassStruct:
				prepath.append(p)
		return('_'.join(prepath))

	def shotpath(self):
		return self.workingdir.replace(self.software[self.use]['dir'], '').rstrip('/')

	def renderpath(self):
		return ospath.join(self.shotpath(), self.renderdir)

	def printHierachy(self):
		hierachy = []
		for i in self.printStruct:
			if i in self.struct:
				hierachy.append((i, self.struct[i]))
		return hierachy




# Import and Export Settings
settingfile = ospath.expanduser('~/.hrc')

def ImportSetting():
	if ospath.getctime(settingfile) < ospath.getmtime(sys.argv[0]):
		raise IOError
	with open(settingfile, 'r') as f:
		shotdata = pickle.load(f)
		if not ospath.isdir(shotdata.workingdir):
			raise IOError
		return shotdata

def ExportToFile(shotclass):
	with open(settingfile, 'w') as f:
		pickle.dump(shotclass, f)

def getUser():
	for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
		user = os.environ.get(name)
		if user:
			return user

def newH():
	print("Hi, is it your first time to use H?")
	print("I will ask some informations")

	defaultuser = getUser()
	user = raw_input("What's your name? [{0}] : ".format(defaultuser))
	if user == '':
		user = defaultuser

	part = raw_input("Do you have a part? : ")

	while True:
		defaultdir = '~/PROJECTS'
		rootdir = raw_input("It will create root of projects directory. Where should it be? [{0}] : ".format(defaultdir))
		if rootdir == '':
			rootdir = defaultdir
		rootdir = ospath.expanduser(rootdir)

		try:
			os.mkdir(rootdir)
			print("Created : {0}".format(rootdir))
			break
		except:
			if ospath.isdir(rootdir):
				merge = raw_input("It already created, do you want merge with it? [yes/NO] : ")
				if merge == 'yes':
					# We are done. Break loop.
					break
				else:
					print('I will treat it as NO.')
					continue
			else:
				raise
	print("Where come to H!")
	time.sleep(1)
	shot = shotdata(user, part, rootdir)
	return shot


def main():
	try:
		shot = ImportSetting()
	except:
		shot = newH()

	while True:
		shot.update()
		ExportToFile(shot)
		shot.printMessage()
		shot.clearLog()
		userInput = raw_input()
		shot.action(userInput)
		# break

if __name__ == '__main__':
	main()
