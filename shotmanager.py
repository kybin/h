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
from OrderedDict import OrderedDict

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
		self.resetInfo()

	def resetInfo(self):
		self.info = OrderedDict([
			('show'	,	{'use':True,
						'name':''}),
			('work'	,	{'use':'Constant',
						'name':'work'}),
			('seq'	,	{'use':False,
						'name':''}),
			('scene',	{'use':False,
						'name':''}),
			('shot'	,	{'use':True,
						'name':''}),
			('software',{'use':'Constant',
						'name':self.software[self.mysoft]['dir']}),
			('task'	,	{'use':True,
						'name':''}),
			('rev'	,	{'use':True,
						'name':''}),
			('show'	,	{'use':True,
						'name':''}),
			])
		print('quit reset')

	def update(self):
		''' update status : workdir, dirlists ... '''
		info = self.info
		show, others = info['show']['name'], info['seq']['name'] and info['scene']['name'] and info['shot']['name']

		if not show:
			self.resetInfo()
		if show and not others:
			self.updateShow()
		self.updateDir()
		self.updateItems()
		print('quit update')

	def updateShow(self):
		'''update show struct'''

		self.resetInfo()

		show = self.info['show']['name']
		structfile = '/'.join([self.rootpath, show, self.structfile])

		with open(structfile) as f: # file data : (seq)/(scene)/shot, seq or scene may not exist.
			uses = f.readline().strip('\n').split('/')
			for s in uses:
				self.info[s]['use']=True
		print('quit updateStruct')

	def updateDir(self):
		pos = self.infoToPos()

		dirpath = '/'.join(pos)
		print(dirpath)
		self.workdir = self.rootpath + '/' + dirpath
		print('quit updateDir')

	def infoToPos(self):
		pos = []
		for k, v in self.info.iteritems():
			if v['use']:
				if v['name']:
					pos.append(v['name'])		
				else:
					break
			else:
				pass
		return pos

	# def posToInfo(self, pos):
	# 	info = self.info
	# 	for i, v in enumerate(pos):
	# 		info[i]

	# 		elif v['use'] == 'Constant':
	# 			append()
	# 		else:


	def updateItems(self):
		d = self.workdir
		it = sorted(os.listdir(d))
		it = [i for i in it if not (i.startswith('_') or i.startswith('.'))]

		task = self.info['task']['name']
		shot = self.info['shot']['name']

		if task:
			it = [i for i in it if i.startswith(task)]
			it = [i for i in it if os.path.isfile(d + '/' + i)]
			it.reverse()
		elif shot:
			it = [i for i in it if os.path.isfile(d + '/' + i)]
			it = list(set([filebox.versioncut(i) for i in it]))
			it = sorted(it)	
		else:
			it = [i for i in it if os.path.isdir(d + '/' + i)]

		self.items = it
		print('quit updateItems')


	def showMessage(self):
		info = self.info
		pos = self.infoToPos()

		# pstruct = ['show', 'seq', 'scene', 'shot', 'task']
		# pstruct = [i for i in pstruct if info[i]['use']]

		os.system('cls')
		print(self.workdir)
		print('-'*75)
		print('Shot Manager V{version}').format(version=self.version)
		print('-'*75)

		items = [' : '.join(['{0: >5}'.format(index+1),val]) for index,val in enumerate(self.items)]
		last = len(pos)
		for i, s in enumerate(info):
			# print(last, idx), 
			if s['use']:
				if s['name']:
					print('{name} : {val}'.format(name=name, val=s['name']))
				else:
					print('< {name} >'.format(name=name))
					if i is last:
						print('\n'.join(items))
			else:
				pass

		print('-'*75)
		# print(status['guides'])
		# print('-'*75)
		if self.log:
			print(self.log)
			print('-'*75)
		print('>>>'),
		print('quit showMessage')

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

	def up(self):
		info = self.info
		head = self.curHead()
		if head:
			info[head]['name']=''
		# self.position = pos
		print('quit up')

	def top(self):
		self.resetInfo()
		print('quit top')		

	def down(self, dest):
		info = self.info
		next = self.nextHead()
		info[next]=dest

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
	def curHead(self):
		last = ''
		for k, v in self.info:
			if v['use']:
				if v['name']:
					last=k
				else:
					break
			else:
				pass
		return last
	def nextHead(self):
		last = ''
		for k, v in self.info:
			if v['use']:
				if not v['name']:
					last=k
					break
			else:
				pass
		if not last:
			print('stack is full!')
			raise
		return last

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