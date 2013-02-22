# coding:utf-8

# general script
import os
import sys
import env
import re
import posixpath
from OrderedDict import OrderedDict
# my script
import maketree



class shotdata:
	def __init__(self):
		self.version = '0.01'
		self.part = 'fx'
		self.user = 'yongbin'

		self.rootpath = env.path().ProjectRoot
		self.head = 'root'
		self.workdir = self.rootpath
		self.software = {
			'houdini':
			{'dir':'houdini', 'read':'hip', 'write':'hip', 'batch':'hython', 'exe': 'houdini', 'initscript': 
			'''
hou.hscript('set -g SHOW = {show}')
hou.hscript('set -g SEQ = {seq}')
hou.hscript('set -g SCENE = {scene}')
hou.hscript('set -g SHOT = {shot}')
hou.hscript('set -g TASK = {task}')
hou.hscript('set -g JOB = {shotpath}')
hou.hscript('set -g OUT = {outpath}')
hou.hipFile.save('{file}')
			'''
			}, 

			'maya':
			{'dir':'maya/scenes', 'read':['ma', 'mb'], 'write':'mb', 'batch':'mayabatch.exe -script', 'exe': 'maya', 'initscript':
			'''
file -rn "{file}";
file -s;
			'''
			},

			'max':
			{'dir':'max', 'read':'max', 'write':'max'}
		}
		# self.struct = None
		self.use = 'houdini'
		self.structfile = '.showStruct'
		self.variableStruct = ['seq', 'scene']
		self.bypassStruct = ['work','software']
		self.runfile = ''
		self.log = ''
		self.resetStruct()

	def resetStruct(self):
		self.struct = OrderedDict([
			('root', self.rootpath),
			('show'	, ''),
			('work'	, 'work'),
			('seq'	, ''),
			('scene', ''),
			('shot'	, ''),
			('software', self.software[self.use]['dir']),
			('task'	, ''),
			('rev'	, '')
			])
		self.printStruct = ['show', 'seq', 'scene', 'shot', 'task', 'rev']

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
		for s in vs:
			if s not in rs:
				try: 
					del struct[s] # 가변적인 틀중 샷과 맞지 않는 틀은 지움
				except KeyError:
					pass
				try:
					self.printStruct.pop(self.printStruct.index(s))
				except:
					pass

	def readStruct(self):
		structfile = '/'.join([self.rootpath, self.struct['show'], self.structfile])
		with open(structfile) as f:
			struct = f.readline().strip('\n').split('/')
		return struct

	def updateDir(self):
		# tasks and revs is not a dir, so we set our last dir is software level
		idx = min(self.headIndex(), self.struct.keys().index('software'))
		wd = '/'.join(self.struct.values()[:idx+1])
		print(wd)
		if os.path.isdir(wd):
			self.workdir = wd
		else:
			print("There isn't such a directory.")
			raise ValueError


	## "Items" mean "Files and Directories" in current directory
	def updateItems(self):
		head = self.head
		i = os.listdir(self.workdir)
		i = self.itemcull(i)
		if head in ['root', 'show', 'work', 'seq', 'scene', 'shot']:
			i = self.directories(i)
		elif head == 'software':
			i = self.tasks(i)
			self.struct['task']=i
		elif head == 'task':
			i = self.revs(i, self.struct['task'])
		else:
			print('head is in a danger area! : {head}'.format(head=head))
			raise ValueError
		self.items = i

	def itemcull(self, items):
		'''item startswith . or _ will cull'''
		culls = [i for i in items if not (i.startswith('.') or i.startswith('_'))]
		return culls

	def directories(self, items):
		'''it takes items and return directories'''
		wd = self.workdir
		dirs = [i for i in items if os.path.isdir(wd + '/' + i)]
		return dirs

	def tasks(self, items):
		tasks = [i for i in items if os.path.isfile(self.workdir + '/' + i)]
		tasks = [i for i in tasks if self.software[self.use]['read'] in i]
		tasks = [i.replace(self.fileprepath()+'.', '') for i in tasks if i.startswith(self.fileprepath())]
		rest = re.compile('[_.]?v?\d*[.]\w+$')
		tasks = [rest.sub('', i) for i in tasks]
		tasks = sorted(list(set(tasks)))
		return tasks

	def revs(self, items, task):
		revs = [i for i in items if self.fileprepath()+'.'+task in i]
		revs.reverse()
		return revs

	def showMessage(self):
		os.system('cls')
		items = [' : '.join(['{0: >4}'.format(index+1),val]) for index,val in enumerate(self.items)]
		print
		print('-'*75)
		print('Shot Manager V{version}').format(version=self.version)
		print('-'*75)
		if self.head != 'root':
			for s, n in self.printHierachy():
				if self.nexthead() != s:
					print('{struct: >8} : {name}'.format(struct=s.upper(), name=n))
				else:
					print('-'*75)
					print('< {struct} >'.format(struct=s.upper()))
					print('\n'.join(items))	
					break		
		else:
			print('\n'.join(items))			
		print('-'*75)
		print('>>>'),

	def printHierachy(self):
		hierachy = []
		for i in self.printStruct:
			if i in self.struct:
				hierachy.append((i, self.struct[i]))
		return hierachy

	def action(self, userInput):
		u = userInput.strip().lower()

		items = self.items
		workdir = self.workdir
		log = self.log

		loweritems = [i.lower() for i in items]

		if u in ['q', 'quit']:
			sys.exit('Bye!')
		elif u in ['o', 'open']:		
			self.opendir()
		elif u.startswith('use '):
			change, sw = u.split(' ')
			self.changesoftware(sw)
		elif u.startswith('new '):
			new, name = u.split()
			self.new(name)
		elif u == '..':
			self.up()
		elif u == '/':
			self.top()
		elif u == '.':
			log=workdir # will replace function -> copy directory path
		elif u == '':
			pass
		else:
			if u.isdigit():
				u = int(u)
				if 0 < u <= len(items):
					self.down(items[u-1])
				else:
					log += 'input out of bound : {input}'.format(input=u)
			else:
				if u in loweritems:
					i = loweritems.index(u)
					u = items[i]
					self.down(u)
				else:
					log += 'invalid input : {input}'.format(input=u)
		
		self.log = log


	# "head" means "Current Level"
	def headshift(self, shift):
		self.head = self.struct.keys()[self.headindex()+shift]

	# head and position

	def headShift(self, shift):
		keys = self.struct.keys()
		cur = self.headIndex()
		new = max(cur+shift, 0)
		self.head = keys[new]

	def headIndex(self):
		return self.struct.keys().index(self.head)

	def nextIndex(self):
		if self.headIndex() == 'rev':
			return None
		else:
			return self.struct.keys()[self.headIndex()+1]

	def prevIndex(self):
		if self.headIndex() == 'root':
			return None
		else:
			return self.struct.keys()[self.headIndex()-1]

	def top(self):
		self.head = 'root'
		self.resetStruct()

	def up(self):
		struct = self.struct
		if self.head in self.bypassStruct:
			while self.head in self.bypassStruct:
				self.headshift(-1)
		struct[self.head]=''
		self.headshift(-1)
		print(self.head)

	def down(self, dest):
		struct = self.struct
		if self.head != 'task':
			self.headShift(1)
			struct[self.head]=dest
			while self.nextIndex() in self.bypassStruct:
				self.headShift(1)
		else:
			self.run(self.workdir + '/' + dest)


	# user actions

	def run(self, file):
		os.system('start "" {0} {1}'.format(self.software[self.use]['exe'], file))

	def opendir(self):
		d = self.workdir
		d = d.replace('/', '\\') # explorer only care about windows style paths
		os.system('explorer {dir}'.format(dir=d))

	def changesoftware(self, sw):
		if sw in self.software:
			self.use = sw
			self.struct['software'] = self.software[self.use]['dir']
		else:
			print("there isn't such a software")

	# additional functionallity...
	def delete(self):
		pass
	def omit(self):
		pass



	# new item functionallity
	def new(self, name):
		dest = self.nextIndex()

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
			except:
				print('your intput is invalid')
				return
			self.newshow(name, showtype)

		elif dest in ['seq', 'scene']:
			self.newdir(name)
		elif dest == 'shot':
			self.newshot(name)
		elif dest in ['task', 'rev']:
			self.newtask(name)

	def newdir(self, dirname):
		nd = posixpath.join(self.workdir, dirname)
		os.mkdir(nd)

	def newshow(self, show, showtype):
		path = posixpath.join(self.workdir, show)
		os.mkdir(path)
		maketree.make('show', path)
		
		showfile = posixpath.join(path, self.structfile)

		with open(showfile, 'w') as f:
			f.write(showtype)

	def newshot(self, shot):
		path = posixpath.join(self.workdir, shot)
		os.mkdir(path)
		os.makedirs(path.replace('work', 'output'))
		maketree.make('shot', path)

	def newtask(self, taskname):
		struct = self.struct
		file = self.workdir + '/' + self.fileprepath() + '.' + taskname + '.v101.' + self.software[self.use]['write']
		shotpath = self.workdir
		outpath = self.outdir()
		
		initscript = self.software[self.use]['initscript'].format(show=struct['show'], seq=struct['seq'], scene=struct['scene'], shot=struct['shot'], task=taskname, shotpath=shotpath, outpath=outpath, file=file)
		scriptfile = posixpath.join(self.workdir, '.temp_init')
		with open(scriptfile, 'w') as f:
			f.write(initscript)
		
		command = self.software[self.use]['batch'].format(file=file) + ' ' + scriptfile
		print(command)
		os.system(command)
		os.remove(scriptfile)
		self.run(file)

	def fileprepath(self):
		prepath = []
		struct = self.struct
		show, shot = struct.keys().index('show'), struct.keys().index('shot')
		paths = struct.values()[show : shot+1]
		for p in paths:
			if not p in self.bypassStruct:
				prepath.append(p)
		return('_'.join(prepath))

	def outdir(self):
		return self.workdir.replace('work', 'output').replace(self.software[self.use]['dir'], '').rstrip('/')


def main():
	print('program in')
	shot = shotdata()
	while True:
	# for i in range(1):
		shot.update()
		# raw_input()
		shot.showMessage()
		userInput = raw_input()
		shot.action(userInput)

if __name__ == '__main__':
	main()