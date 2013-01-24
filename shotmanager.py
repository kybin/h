# coding:utf-8

# 이 프로그램은 계속 열어놓고 프로그램을 실행시키거나 폴더를 열때 사용한다.
# 프로젝트의 구조는 다음중 하나가 된다.

# 1.쇼/시퀀스/씬/샷/잡/리비전
# 2.쇼/씬/샷/리비전
# 3.쇼/샷/리비전

# 구조를 리스트로 표현해보면 [$SHOW/$SEQ/$SCENE/$SHOT/$REV]
# 실제폴더구조는	[$SHOW/work/$SEQ/$SCENE/$SHOT/$REV]
# 					[$SHOW/out/ $SEQ/$SCENE/$SHOT/$REV]

# 여기서 샷부터는 각각의 프로그램마다 따로 출력된다. (work,out으로 나눌수도 있음)
# 각 위치에서는 아이템 선택또는 폴더열기가 가능하다.
# 기능 : 위치이동, 파일열기, 폴더열기
import os
import env
import filebox
import copy
import time
from collections import defaultdict

class shotdata:
	def __init__(self):
		self.version = '0.01'
		self.part = 'fx'
		self.user = 'yongbin'

		self.rootpath = env.path().ProjectRoot
		self.position = []
		self.workdir = self.rootpath
		self.software = {
						'houdini':{'dir':'houdini', 'exe':'hip'}, 
						'maya':{'dir':'maya/scenes', 'exe':['ma', 'mb']},
						'max':{'dir':'max', 'exe':'max'}
						}
		# self.struct = None
		self.mysoft = 'houdini'
		self.structfile = '.showStruct'
		self.log = ''
		self.reset()

	def reset(self):
		# 'None' in this dict means 'Not Use'
		mysoftdir = self.software[self.mysoft]['dir']
		self.replacements = {'show':None, 'seq':None, 'scene':None, 'shot':None, 'software':mysoftdir, 'task':''}
		self.struct = ['show', 'work', 'seq', 'scene', 'shot', 'software', 'task']
		print('quit reset')

	def update(self):
		''' update status : workdir, dirlists ... '''
		p = self.position
		if len(p) == 0:
			self.reset()
		if len(p) == 1:
			self.updateShow()
			self.updateStruct()
		# updatePosition()
		self.updateDir()
		self.updateItems()
		print('quit update')

	def updateShow(self):
		self.show = self.position[0]
		self.replacements['show'] = self.position[0]
		print('quit updateShow')

	def updateStruct(self):
		'''when our position arrives at 'show' this method reads show struct from file'''

		filepath = '/'.join([self.rootpath, self.show, self.structfile])
		with open(filepath) as f:
			# file data may look like this : show/seq/scene/shot
			mainstruct = f.readline().strip('\n').split('/')
			for k in mainstruct:
				self.replacements[k]='' # this will be using
		struct = ['show', 'work', 'seq', 'scene', 'shot', 'software', 'task']
		for k in struct:
			if k in self.replacements and self.replacements[k] is None:
				struct.remove(k)
		self.struct = struct
		print('quit updateStruct')

	def updateDir(self):
		dirpath = '/'.join(self.position)
		print(dirpath)
		self.workdir = self.rootpath + '/' + dirpath
		print('quit updateDir')

	def updateItems(self):
		workdir = self.workdir
		files = sorted(os.listdir(workdir))
		files = [f for f in files if not (f.startswith('_') or f.startswith('.'))]

		task = self.replacements['task']
		shot = self.replacements['shot']

		if task is not None and task is not '':
			files = [f for f in files if f.startswith(task)]
			files = [f for f in files if os.path.isfile(workdir + '/' + f)]
			files.reverse()
		elif shot is not None and shot is not '':
			files = [f for f in files if os.path.isfile(workdir + '/' + f)]
			files = list(set([filebox.versioncut(f) for f in files]))
			files = sorted(files)	
		else:
			files = [f for f in files if os.path.isdir(workdir + '/' + f)]

		self.items = files
		print('quit updateItems')


	def showMessage(self):
		version = self.version
		rpl = self.replacements
		items = [' : '.join(['{0: >5}'.format(index+1),val]) for index,val in enumerate(self.items)]
		printstruct = ['show', 'seq', 'scene', 'shot', 'task']
		printstruct = [i for i in printstruct if rpl[i] is not None]


		os.system('cls')

		print('-'*75)
		print('Shot Manager V{version}').format(version=version)
		print('-'*75)

		last = 0
		for i,val in enumerate(printstruct):
			if rpl[val]:
				last = i+1
			else:
				break

		for idx, name in enumerate(printstruct):
			# print(last, idx), 
			if rpl[name]:
				print('{name} : {val}'.format(name=name, val=rpl[name]))

			else:
				print('< {name} >'.format(name=name))
				if idx == last:
					print('\n'.join(items))

		print('-'*75)
		# print(status['guides'])
		# print('-'*75)
		if self.log:
			print(self.log)
			print('-'*75)
		print('>>>'),
		print('quit showMessage')

	def doSomething(self, userInput):
		#####################
		u = userInput.lower()
		#####################
		pos = self.position
		items = self.items
		workdir = self.workdir
		log = self.log

		loweritems = [i.lower() for i in items]

		if u in ['q', 'quit']:
			raise
		elif u in ['o', 'open']:		
			opendir(workdir)
		elif u == '..':
			self.up()
		elif u == '/':
			self.top()
		elif u == '.':
			log=workdir # will replace function -> copy directory path
		elif u == '':
			pass
		# elif u.startswith('new '):
		# 	newname = u.lstrip('new')
		# 	newname = newname.strip()
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
		# self.position = pos
		print('quit doSomething')

	# def updatePosition(self):
	# 	# replace with keys
	# 	pos = []
	# 	for k in self.struct:
	# 		if k in self.replacements:
	# 			pos.append(self.replacements[k])
	# 		else:
	# 			pos.append(k)

	# 	# cut
	# 	idx = 0
	# 	for i, val in enumerate(pos):
	# 		if not val:
	# 			idx = i
	# 	self.position = pos[:idx]
	# 	print('quit updatePosition')


	def up(self):
		pos = self.position
		rpl = self.replacements
		try:
			k = pos.pop()
			while rpl[k]:
				k = pos.pop()
		except IndexError:
			pass
		except KeyError:
			pass
		self.position = pos
		print('quit up')		
	def top(self):
		self.position = []
		print('quit top')		

	def down(self, dest):	
		pos = self.position
		rpl = self.replacements
		struct = self.struct

		name = struct[len(pos)]
		pos.append(dest)
		rpl[name]= pos[-1]
		print(name, pos[-1])
		print(struct)
		print(pos)
		print(rpl)
		print('start loop')
		try:
			k = struct[len(pos)]
			print(k)
			while k not in rpl: # mean it's constant path
				pos.append(k)
				k += 1
				print(pos)
		except:
			pass
		print('quit loop')
		print(struct)
		print(pos)
		print(rpl)
		# self.position = pos

		print('quit down')

	def excute(file):
		os.system('start {0}'.format(file))
	def opendir(d):
		d = d.replace('/', '\\') # explorer only care about windows style path
		os.system('explorer {dir}'.format(dir=d))
	def delete():
		pass
	def omit():
		pass
	def newshow():
		pass
	def newjob():
	# def new(status, name):
	# 	if status['position']
		pass

def main():
	shot = shotdata()
	while True:
		shot.update()
		raw_input()
		shot.showMessage()
		pos = shot.position
		items = shot.items
		userInput = raw_input()
		shot.doSomething(userInput)


if __name__=='__main__':
	main()