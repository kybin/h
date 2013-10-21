# coding:utf-8

# general script
import os
import sys
import env
import re
import os.path as ospath
import pickle
import shutil
import itertools

# external module
import maketree
import filebox
from OrderedDict import OrderedDict




class shotdata:
	def __init__(self):
		self.version = '0.02'
		self.part = 'fx'
		self.user = getUser()
		self.rootpath = env.ProjectRoot
		self.workdir = self.rootpath
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
		self.structfile = '.showStruct'
		self.orderfile = '.order'
		self.runfile = ''
		self.lastrundir = ''
		self.lastruntask = ''
		self.lastrunfile = ''
		self.log = ''
		self.resetStruct()


	# struct
	def resetStruct(self):
		self.struct = OrderedDict([
			('root', self.rootpath),
			('show'	, ''),
			('work'	, 'work'),
			('seq'	, ''),
			('scene', ''),
			('shot'	, ''),
			('run', 'scenes'),
			('task'	, ''),
			('rev'	, '')
			])
		self.head = 'root'
		self.variableStruct = ['seq', 'scene']
		self.deletedStruct = []
		self.bypassStruct = ['work','run']
		self.printStruct = ['show', 'seq', 'scene', 'shot', 'task', 'rev']

	def readStruct(self):
		structfile = '/'.join([self.rootpath, self.struct['show'], self.structfile])
		with open(structfile) as f:
			struct = f.readline().strip('\n').split('/')
		return struct


	# update
	def update(self):
		''' update status : workdir, dirlists ... '''
		head = self.head
		if head == 'root':
			self.resetStruct()
		if head == 'work': # 원래 쇼였을때 실행되어야하나 down() 실행시 바로 넘어가 버리기 때문에 work로 지정
			self.updateShow() 
		self.updateDir()
		self.updateItems()

	def updateShow(self):
		'''update show struct'''
		struct = self.struct

		rs = self.readStruct()
		vs = self.variableStruct
		ds = self.deletedStruct
		for s in vs:
			if s not in rs:
				try: 
					del struct[s] # 가변적인 틀중 샷과 맞지 않는 틀은 지움
					ds.append(s)
				except KeyError:
					print('{0} already deleted'.format(s))
					pass
				try:
					self.printStruct.pop(self.printStruct.index(s))
				except:
					pass

	def updateDir(self):
		# tasks and revs are not a dir, so we have to set our last dir
		idx = min(self.headIndex(), self.struct.keys().index('task')-1)
		limitedstruct = self.struct.values()[:idx+1]
		wd = '/'.join(limitedstruct)
		print(wd)
		if os.path.isdir(wd):
			self.workdir = wd
		else:
			raise ValueError("There isn't such a directory. {0}".format(wd))


	def updateItems(self): # "Items" means "Files and Directories" in current directory
		head = self.head
		items = os.listdir(self.workdir)
		items = self.itemculling(items)
		if self.headIndex() <= self.headIndex('shot'):
			items = self.directories(items)
		elif head == 'run':
			items = self.tasks(items)
			self.struct['task']=items
		elif head == 'task':
			items = self.revs(items, self.struct['task'])
		else:
			print('head is in a danger area! : {head}'.format(head=head))
			raise ValueError

		if ospath.isfile(ospath.join(self.workdir, self.orderfile)):
			orderfile = ospath.join(self.workdir, self.orderfile)
			with open(orderfile) as f:
				lines = f.read().splitlines()
				for l in lines:
					if l not in items:
						print('item does not match with order file. fix or delete `{0}`'.format(orderfile))
						sys.exit(1)
			items = lines


		self.items = items


	# print
	def printMessage(self):
		# os.system('cls')
		items = [' : '.join(['{0: >4}'.format(idx+1),val]) for idx,val in enumerate(self.items)]
		print('='*75)
		# print('-'*75)
		print('Shot Manager V{version}'.format(version=self.version).center(75))
		# print('-'*75)
		print('user : {0}, part : {1}'.format(self.user, self.part).rjust(75))
		print('='*75)
		if self.head != 'root':
			for s, v in self.struct.items()[1:]: # we don't wanna see root
				# print(s, self.head)
				if s != self.head:
					if s not in self.bypassStruct:
						print('{0: >8} : {1}'.format(s.upper(), v))
				else:
					print('-'*75)
					print('< {0} : {1} >'.format(s.upper(), v)),
					if self.nextHead() == 'task':
						print('- {0}'.format(self.use)),
					print('\n')
					print('\n'.join(items))	
					# if self.lastrunfile:
					# 	print('-'*75)
					# 	print('{0: >4} : {1} {2}'.format('`', self.lastruntask, '(### Last Task ###)'))
					break		
		else:
			print('\n'.join(items))			
		print('-'*75)
		print('>>>'),

	def printHelp(self):
		os.system('cls')
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
		print('>>> Enter to quit....'),
		raw_input()

	# action
	def action(self, userInput):
		u = userInput.strip()
		lu = u.lower()

		items = self.items
		workdir = self.workdir
		loweritems = [i.lower() for i in items]

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
			delitem = u.split()[1]
			self.delete(delitem)
		elif lu.startswith('new '):
			names = u.split()[1:]
			for n in names:
				print(n)
				self.new(n)
		elif u == 'order':
			orderfile = ospath.join(self.workdir, self.orderfile)
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

		elif u == '..':
			self.up()
		elif u == '/':
			self.top()
		elif u == '.':
			self.log=workdir # will replace function -> copy directory path
		else:
			if u.isdigit():
				u = int(u)
				if 0 < u <= len(items):
					self.down(items[u-1])
				else:
					self.log += 'input out of bound : {input}'.format(input=u)
			else:
				if lu in loweritems:
					i = loweritems.index(lu)
					u = items[i]
					self.down(u)
				else:
					self.log += 'invalid input : {input}'.format(input=u)
		


	# cull
	def itemculling(self, items):
		'''item startswith . or _ will cull'''
		culls = [i for i in items if not (i.startswith('.') or i.startswith('_'))]
		return culls

	def directories(self, items):
		'''it takes items and return directories'''
		dirs = sorted([i for i in items if os.path.isdir(self.workdir + '/' + i)])
		return dirs

	def tasks(self, items):
		files = [i for i in items if os.path.isfile(self.workdir + '/' + i)]
		tasks = []
		readExtensions = self.software[self.use]['read']
		for e in readExtensions:
			tasks += [f for f in files if e in f]
		# tasks = [i.replace(self.fileprepath()+'.', '') for i in tasks] #  if i.startswith(self.fileprepath())
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
	def headShift(self, shift):
		self.head = self.struct.keys()[self.headIndex()+shift]

	def headIndex(self, head=None):
		if not head:
			head = self.head
		return self.struct.keys().index(head)

	def nextHead(self, head=None):
		if not head:
			head = self.head
		if self.head == 'rev':
			return None
		else:
			return self.struct.keys()[self.headIndex(head)+1]

	def prevHead(self, head=None):
		if not head:
			head = self.head
		if self.head == 'root':
			return None
		else:
			return self.struct.keys()[self.headIndex(head)-1]


	# move or run
	def top(self):
		self.head = 'root'
		self.resetStruct()

	def up(self):
		struct = self.struct
		if self.head in self.bypassStruct:
			while self.head in self.bypassStruct:
				self.headShift(-1)
		struct[self.head]=''
		self.headShift(-1)
		print(self.head)

	def down(self, dest):
		struct = self.struct
		if self.nextHead() == 'task':
			self.runTask(self.workdir, dest)
		elif self.nextHead() == 'rev':
			self.runRev(dest)
		else:
			self.headShift(1)
			struct[self.head]=dest
			while self.nextHead() in self.bypassStruct:
				self.headShift(1)
		print(self.head)

	def runTask(self, dir, task):
		flist = os.listdir(dir)
		flist = sorted([f for f in flist if f.startswith(task)])
		flist.reverse()
		lastf = flist[0]
		lastfpath = ospath.join(self.workdir, lastf)
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
			self.log = 'cannot find last task'

	def runLastFile(self):
		if self.lastrunfile:
			self.runFile(self.lastrunfile)


	# new
	def new(self, name):
		dest = self.nextHead()
		if dest == 'show':
			A, B, C = 'seq/scene/shot', 'scene/shot', 'shot'
			print('choose one of these types')
			print('1. show/' + A)
			print('2. show/' + B)
			print('3. show/' + C)

			ui = raw_input()
			try:
				ui = int(ui)
				showtype = [A, B, C][ui-1]
			except :
				print('your intput is invalid')
				raise # we should return in a stable ver, but now for debugging, raise it
			self.newshow(name, showtype)

		elif dest in ['seq', 'scene']:
			self.newdir(name)
		elif dest == 'shot':
			self.newshot(name)
		elif dest in ['task', 'rev']:
			self.newtask(name)

		# orderfile = ospath.join(self.workdir, self.orderfile)
		# with open(orderfile, 'a') as f:
		# 	f.write(name)
		# 	f.write('\n')
 


	def newdir(self, dirname):
		nd = ospath.join(self.workdir, dirname)
		os.mkdir(nd)

	def newshow(self, show, showtype):
		path = ospath.join(self.workdir, show)
		os.mkdir(path)
		print('maketree!!!!!!!!!!!!!!!!!!!!!!!!')
		maketree.make('show', path)
		
		showfile = ospath.join(path, self.structfile)

		with open(showfile, 'w') as f:
			f.write(showtype)

	def newshot(self, shot):
		path = ospath.join(self.workdir, shot)
		os.mkdir(path)
		# os.makedirs(path.replace(self.struct['work'], 'output', 1))
		maketree.make('shot', path)

	def newtask(self, taskname):
		struct = self.struct
		structname = self.structname
		structpath = self.structpath
		filename = '.'.join([self.fileprepath(), taskname, 'v101', self.software[self.use]['write']])
		filepath = ospath.join(self.workdir, filename)
		shotpath = self.shotpath()
		renderpath = self.renderpath()

		# # before make script, we have to append deletedStruct to currentStruct so let the follow string formatting won't make error
		# for s in self.deletedStruct:
		# 	struct[s]=''
		startf, endf, fps = 1, 240, 24.0

		initscript = self.software[self.use]['initscript'].format(
			show=structname('show'), seq=structname('seq'), scene=structname('scene'), shot=structname('shot'), task=taskname,
			showpath = structpath('show'), seqpath=structpath('seq'), scenepath=structpath('scene'), taskpath=structpath('run'),
			shotpath=shotpath, renderpath=renderpath, filepath=filepath,
			fps=24, start=(startf-1)/fps, end=endf/fps)
		scriptfile = ospath.join(self.workdir, '.temp_init')
		with open(scriptfile, 'w') as f:
			f.write(initscript)
		
		command = self.software[self.use]['batch'] + ' ' + scriptfile
		# command = self.software[self.use]['batch'].format(filepath=filepath) + ' ' + scriptfile
		print(command)
		os.system(command)
		os.remove(scriptfile)
		self.runFile(filepath)


	# other actions
	def opendir(self):
		dir = self.workdir
		os.system('thunar {dir}'.format(dir=dir))

	def changesoftware(self, sw):
		if sw in self.software:
			self.use = sw
			# self.struct['software'] = self.software[self.use]['dir']
		else:
			print("there isn't such a software")

	def delete(self, item):
		''' Move a dir or file to _deleted directory '''
		itempath = ospath.join(self.workdir, item)
		filebox.incBackup(itempath, backupdirname ='_deleted', move=True)

	def omit(self, item):
		''' Move a dir or file to _omitted directory '''
		itempath = ospath.join(self.workdir, item)
		filebox.incBackup(itempath, backupdirname ='_omitted', move=True)


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
		return self.workdir.replace(self.software[self.use]['dir'], '').rstrip('/')

	def renderpath(self):
		return ospath.join(self.shotpath(), 'images')

	def printHierachy(self):
		hierachy = []
		for i in self.printStruct:
			if i in self.struct:
				hierachy.append((i, self.struct[i]))
		return hierachy



# Import and Export Settings
settingfile = ospath.expanduser('~/.shotmanager')
	
def ImportSetting():
	if ospath.getctime(settingfile) < ospath.getmtime(sys.argv[0]):
		raise IOError
	with open(settingfile, 'r') as f:
		shotdata = pickle.load(f)
		if not ospath.isdir(shotdata.workdir):
			raise IOError
		return shotdata

def ExportSetting(shotclass):
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
		shot = shotdata() # new shot
	except OSError:
		shot = shotdata() # new shot
	# except Error as e:
	# 	raise(e)
	# shot = shotdata()
	while True:
		shot.update()
		ExportSetting(shot)
		shot.printMessage()
		userInput = raw_input()
		#if userInput in ['help', '/?', '/help']:
		#	shot.printHelp()
		#else:
		shot.action(userInput)

if __name__ == '__main__':
	main()
