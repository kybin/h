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
# from collections import defaultdict
from OrderedDict import OrderedDict

class shotdata:
	def __init__(self):
		self.version = '0.01'
		self.part = 'fx'
		self.user = 'yongbin'

		self.rootpath = env.path().ProjectRoot
		self.head = ''
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
		self.variableStruct = ['seq', 'scene']
		self.log = ''
		# self.resetStruct()

	def update(self):
		''' update status : workdir, dirlists ... '''
		struct = self.struct

		if head == '':
			self.resetStruct()
		if head == 'show':
			self.updateShow() 
		self.updateDir()
		self.updateItems()
		print('quit update')

	def resetStruct(self):
		self.struct = OrderedDict([
			('root', self.rootpath)
			('show'	, ''
			('work'	, 'work'),
			('seq'	, ''),
			('scene', ''),
			('shot'	, ''),
			('software', self.software[self.mysoft]['dir']),
			('task'	, ''
			('rev'	, ''
			('show'	, '')
			])

	def updateShow(self):
		'''update show struct'''
		struct = self.struct

		rs = self.readStruct()
		vs = self.variableStruct
		for s in vs:
			if s not in rs:
				del struct[s]
		# if error we have to return 'self.struct'

	def readStruct(self):
		structfile = '/'.join([self.rootpath, struct['show'], self.structfile])
		with open(structfile) as f:
			struct = f.readline().strip('\n').split('/')
		return struct

	def updateDir(self):
		self.workdir = '/'.join(self.struct.values()[:headIndex+1])

	def updateItems(self):
		'''it takes workdir and return directory items'''
		i = os.listdir(os.workdir)
		i = cullItems(i)
		if head in ['root', 'show', 'seq', 'scene']:
			i = returnDirs(i)
		elif head == 'show':
			i = returnTasks(i)
		elif head == 'task':
			i = returnRevs(i)
		else:
			print('head is in danger area! : {head}'.format(head=head))
			raise
		self.items = i

	def cullItems(self, items):
		'''item startswith . or _ will pass'''
		culls = [i for i in items if not (i.startswith('.') or i.startswith('_'))]
		return culls

	def returnDirs(self, items):
		'''it takes items and return directories'''
		wd = self.workdir
		dirs = [i for i in items if os.path.isdir(wd + '/' + i)]
		return dirs

	def returnTasks(self):
		# it takes file list and return tasks
		pass

	def returnRevs(self):
		# it takes files and return revs
		pass

	def showMessage(self):
		# return message
		pass

	def doSomething(self, userInput):

		u = userInput.lower()

		# pos = self.position
		items = self.items
		workdir = self.workdir
		log = self.log

		loweritems = [i.lower() for i in items]

		if u in ['q', 'quit']:
			raise
		elif u in ['o', 'open']:		
			self.opendir()
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



	# head and position

	def headIndex(self):
		return self.struct.keys().index(head)

	def headShift(self, shift):
		keys = self.struct.keys()
		cur = headIndex()
		self.head = keys[cur+shift]

	def top(self):
		self.head = 'root'
		self.resetStruct()
		print('quit top')		

	def up(self):
		struct = self.struct
		head = self.curHead()

		struct[head]=''
		self.headShift(-1)
		while struct[head]:
			headShift(-1)

	def down(self, dest):
		struct = self.struct
		head = self.head
		self.headShift(1)
		struct[head]=dest
		while struct[head]:
			headShift(1)



	def excute(file):
		os.system('start {0}'.format(file))
	def opendir(self):
		d = self.workdir
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


if __name__ == '__main__':
	main()