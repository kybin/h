#!/usr/bin/python
# coding:utf-8

# standard module 
import os
import sys
import re
import os.path as ospath
import pickle
import shutil
import itertools
# external module
import env
import maketree
import filebox
from OrderedDict import OrderedDict

class shotdata:
	def __init__(self):
		self.version = '0.02'
		self.part = 'fx'
		self.user = getUser()
		self.rootpath = env.ProjectRoot
		self.workingdir = self.rootpath
		self.software = {
			'houdini':
			{'dir':'scenes', 'read':['hip'], 'write':'hip', 'batch':'hython', 'execute': 'houdini', 
			'initscript' : '''
hou.hipFile.clear()

hou.setFrame({fps})
hou.hscript('tset {start}, {end}')

ip = hou.node('out').createNode('ifd', 'ip')
ip.parm('vm_picture').set('ip')

seq = hou.node('out').createNode('ifd', '{shot}_{task}')
seq.parm('vm_picture').set('$OUT/v01/$OS.$F4.exr')
seq.parm('vm_image_comment').set('$HIP/$HIPNAME')
seq.setPosition(hou.Vector2(2,0))

hou.hscript('set -g SHOW = {show}')
hou.hscript('set -g SEQ = {seq}')
hou.hscript('set -g SCENE = {scene}')
hou.hscript('set -g SHOT = {shot}')
hou.hscript('set -g TASK = {task}')

hou.hscript('set -g SHOWPATH = {showpath}')
hou.hscript('set -g SEQPATH = {seq}')
hou.hscript('set -g SCENEPATH = {scenepath}')
hou.hscript('set -g SHOTPATH = {shotpath}')
hou.hscript('set -g TASKPATH = {taskpath}')
hou.hscript('set -g DATAPATH = {showpath}/assets')

hou.hscript('set -g JOB = {shotpath}')
hou.hscript('set -g OUT = {renderpath}')

hou.hipFile.save('{filepath}')'''
			}, 

			'maya':
			{'dir':'scenes', 'read':['ma', 'mb'], 'write':'mb', 'batch':'mayabatch.exe -script', 'execute': 'maya.exe', 
			'initscript':'''
file -rn "{file}";
file -s;'''
			},

			'max':
			{'dir':'scenes', 'read':['max'], 'write':'max', 'batch':'3dsmax.exe -mxs', 'execute': '3dsmax',
			'initscript':'''
'''			}
		}

		self.use = 'houdini'
		self.renderdir = 'images'
		self.structfile = '.showinfo'
		self.orderfile = '.order'
		self.lastrundir = ''
		self.lastruntask = ''
		self.lastrunfile = ''
		self.items=[]
		self.log = ''
		self.initStruct()


	# struct
	def initStruct(self):
		self.struct = OrderedDict([
			('root', self.rootpath),
			('show'	, ''),
			('work'	, 'work'),
			('shot'	, ''),
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
		''' update status : workingdir, dirlists ... '''
		head = self.head
		if head == 'root':
			self.initStruct()
		if head == 'show':
			self.updateShow() 
		self.updateDir()
		self.updateItems()

	def updateShow(self):
		''' reads .showinfo file in the show directory, then delete unused level from self.struct. '''
		structfile = ospath.join(self.rootpath, self.struct['show'], '.showinfo')
		with open(structfile) as f:
			readStruct = set(f.readline().strip('\n').split('/'))
			delStruct = self.showStruct - readStruct
			for level in delStruct:
				del self.struct[level]
				#print("{0} deleted".format(level))

	def updateDir(self):
		''' Tasks and revs are not a dir, so we have to set our last dir '''
		struct = self.struct
		dirindex = min(self.currentHeadIndex(), struct.keys().index('run'))
		workingdir = ospath.join(*struct.values()[:dirindex+1])
		print(workingdir)
		if os.path.isdir(workingdir):
			self.workingdir = workingdir
		else:
			raise ValueError("There isn't such a directory. {0}".format(workingdir))

	def updateItems(self):
		''' update items (files and directories) in current directory'''
		head = self.head
		items = os.listdir(self.workingdir)
		#print(items)
		#self.log+=items
		items = self.itemculling(items)
		if self.currentHeadIndex() <= self.headIndex('shot'):
			items = self.directories(items)
		elif head == 'run':
			items = self.tasks(items)
			self.struct['task']=items
		elif head == 'task':
			items = self.revs(items, self.struct['task'])
		else:
			raise KeyError('head is in a danger area! : {0}'.format(head))

		if ospath.isfile(ospath.join(self.workingdir, self.orderfile)):
			orderfile = ospath.join(self.workingdir, self.orderfile)
			with open(orderfile) as f:
				lines = f.read().splitlines()
				for l in lines:
					if l not in items:
						raise ValueError('item does not match with order file. fix or delete `{0}`'.format(orderfile))
			items = lines
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

		if self.log:
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
		u = userInput.strip()
		lu = u.lower()
		workingdir = self.workingdir

		if (not u) or (u in ['help', '/?', '/help']):
			self.printHelp()	
		elif lu in ['q', 'quit', 'exit']:
			sys.exit('Bye!')
		elif lu in ['o', 'open']:		
			self.opendir()
		elif lu.startswith('use '):
			change, sw = u.split(' ')
			self.changesoftware(sw)
		elif lu.startswith('part '):
			self.part = u.split()[1]
		elif lu.startswith('user '):
			self.user = u.split()[1]
		elif lu.startswith('del '):
			item = u.split()[1]
			self.delete(item)
		elif lu.startswith('omit '):
			item = u.split()[1]
			self.omit(item)
		elif lu.startswith('new '):
			names = u.split()[1:]
			for n in names:
				print(n)
				self.new(n)
		elif u == 'order':
			orderfile = ospath.join(self.workingdir, self.orderfile)
			if not ospath.isfile(orderfile):
				# self.updateItems()
				with open(orderfile, 'w') as f:
					for i in self.items:
						f.write('{0}\n'.format(i))
			os.system(orderfile)
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
		tasks = []
		exts = self.software[self.use]['read']
		for e in exts:
			tasks += [f for f in files if e in f]
		rest = re.compile('[-_.]?v?\d*[.]\w+$')
		tasks = [rest.sub('', i) for i in tasks]
		tasks = sorted(list(set(tasks)))
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

	# move or run
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
		self.headShift(-1)
		print(self.head)

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

	def runTask(self, dir, task):
		flist = os.listdir(dir)
		flist = sorted([f for f in flist if f.startswith(task)])
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
		self.writeLog(command)
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
		''' Move a dir or file to _deleted directory '''
		itempath = ospath.join(self.workingdir, item)
		print("jump to filebox")
		raw_input()
		filebox.incBackup(itempath, backupdirname ='_deleted', move=True)

	def omit(self, item):
		''' Move a dir or file to _omitted directory '''
		itempath = ospath.join(self.workingdir, item)
		filebox.incBackup(itempath, backupdirname ='_omitted', move=True)

	def writeLog(self, comment):
		if self.log:
			self.log+='\n'
		self.log+=comment

	def clearLog(self):
		self.log=''

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
		# try:
		# 	paths[1]='FX' # will removed
		# except IndexError:
		# 	pass
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
		return ospath.join(self.shotpath(), 'images')

	def printHierachy(self):
		hierachy = []
		for i in self.printStruct:
			if i in self.struct:
				hierachy.append((i, self.struct[i]))
		return hierachy



# Import and Export Settings
settingfile = ospath.expanduser('~/.piplrc')
	
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

# Start here
def main():
	try:
		shot = ImportSetting()
	except IOError:
		shot = shotdata()
	except OSError:
		shot = shotdata()
	while True:
	# for i in range(1):
		shot.update()
		ExportToFile(shot)
		shot.printMessage()
		shot.clearLog()
		userInput = raw_input()
		shot.action(userInput)

if __name__ == '__main__':
	main()
