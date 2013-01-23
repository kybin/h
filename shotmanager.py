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
						'maya':{'dir':'maya/scenes', 'exe':['ma', 'mb']}
						'max':{'dir':'max', 'exe':'max'}
						}
		# self.struct = None
		self.mysoft = 'houdini'
		self.structfile = '.showStruct'

	def resetenv(self):
		# self.show = None
		# self.seq = None
		# self.scene = None
		# self.shot = None
		# self.software = self.software[self.mysoft]['dir']
		# self.task = ''
		self.names = {'show':None, 'seq':None, 'scene':None, 'shot':None, 'software':mysoftdir, 'task':''}

	def update(self):
		''' update status : workdir, dirlists ... '''
		p = self.position
		if len(p) == 0:
			reset()
		if len(p) == 1:
			updateShow()
			updateStruct()
		updateDir()
		updateItems()

	def updateShow(self):
		self.show = self.position[0]

	def updateStruct(self):
		filepath = '/'.join([self.rootpath, self.show, self.structfile])
		# 4 main struct is 'show', 'seq', 'scene', 'shot'. but some of this can be missing.
		with open(filepath) as f:
			mainStruct = f.readline().strip('\n').split('/')
			for k in mainStruct:
				self.names[k]=''
		mainStruct = mainStruct.insert(mainStruct.index('show')+1, 'work')
		subStruct = ['task', 'rev']
		self.struct = mainStruct.extend(subStruct)

	def updateDir(self):
		dirlist = []
		for val in self.position:
			dirlist.append(val)
			try:
				dirlist.append(child[val])
			except IndexError:
				pass
		self.workdir = self.rootpath + self.

	def updateItems(self):
		files = sorted(os.listdir(self.workdir))
		files = [f for f in files if not (f.startswith('_') or f.startswith('.'))]

		task = status['task']
		shot = status['shot']

		if :
			files = [f for f in files if f.startswith(task)]
			files = [f for f in files if os.path.isfile(workdir + '/' + f)]
			files.reverse()
		elif shot:
			files = [f for f in files if os.path.isfile(workdir + '/' + f)]
			files = list(set([filebox.versioncut(f) for f in files]))
			files = sorted(files)	
		else:
			files = [f for f in files if os.path.isdir(workdir + '/' + f)]

		return files


	def move(self):
		pass


	



class viewer:

def main():
	status = {}
	status = globalStatus(status)

	while status:
		status = resetStatus(status)
		showMessage(status)
		clearlog(status)
		userInput = raw_input()
		status = doSomething(status, userInput)


def globalStatus(status):
	status['version'] = '0.01'
	status['rootdir'] = env.path().ProjectRoot
	status['guides'] = ''
	# status['guides'] = "select:'(NUM)name', up:'..', top:'/' directory address:'.'"
	# status['guides'] += "\nopendir:'(o)open', default program:'(d)default', rename:'(r)rename'"
	status['position'] = []
	status['log'] = ''
	return status

def resetStatus(status):
	pos = status['position']
	for i, s in enumerate(['show','seq','scene','shot','task','rev']):
		try:
			status[s] = pos[i]
		except:
			status[s] = None

	work = workdir(status)
	items = workitem(status, work)

	status['workdir'] = work
	status['items'] = items
	status['log'] = items
	# status[''] = 
	return status

def workdir(status):
	stat = copy.deepcopy(status)
	root = stat['rootdir']
	pos = stat['position']
	if pos:
		pos.insert(1, 'work')
		work = '/'.join(pos[:4])
		workdir = root + '/' + work
	else:
		workdir = root
	return workdir

def workitem(status, workdir):
	files = sorted(os.listdir(workdir))
	files = [f for f in files if not (f.startswith('_') or f.startswith('.'))]

	task = status['task']
	shot = status['shot']

	if task:
		files = [f for f in files if f.startswith(task)]
		files = [f for f in files if os.path.isfile(workdir + '/' + f)]
		files.reverse()
	elif shot:
		files = [f for f in files if os.path.isfile(workdir + '/' + f)]
		files = list(set([filebox.versioncut(f) for f in files]))
		files = sorted(files)	
	else:
		files = [f for f in files if os.path.isdir(workdir + '/' + f)]

	return files




def showMessage(status):
	items = [' : '.join(['{0: >5}'.format(index+1),val]) for index,val in enumerate(status['items'])]
	# show = status['show']
	# seq = status['seq']
	# scene = status['scene']
	# shot = status['shot']
	# task = status['task']
	# rev = status['rev']
	struct = ['show', 'seq', 'scene', 'shot', 'task', 'rev']

	os.system('cls')

	print('-'*75)
	print('Shot Manager V{version}').format(version=status['version'])
	print('-'*75)

	last = 0
	for i,val in enumerate(struct):
		if status[val]:
			last = i+1
		else:
			break

	for idx, name in enumerate(struct):
		# print(last, idx), 
		if status[name]:
			print('{name} : {val}'.format(name=name, val=status[name]))

		else:
			print('< {name} >'.format(name=name))
			if idx == last:
				print('\n'.join(items))

	print('-'*75)
	print(status['guides'])
	print('-'*75)
	if status['log']:
		print(status['log'])
		print('-'*75)
	print('>>>'),

def clearlog(status):
	status['log'] = ''

def doSomething(status, userInput):
	#####################
	u = userInput.lower()
	#####################
	pos = status['position']
	items = status['items']
	loweritems = [i.lower() for i in status['items']]

	workdir = status['workdir']
	if u in ['q', 'quit']:
		return False
	elif u in ['o', 'open']:		
		opendir(workdir)
	elif u == '..':
		status['log'] += 'here'
		pos = up(pos)
		status['log'] += '/'.join(pos)
	elif u == '/':
		pos = top(pos)
	elif u == '.':
		status['log']=status['workdir'] # will replace function -> copy directory path
	elif u == '':
		pass
	# elif u.startswith('new '):
	# 	newname = u.lstrip('new')
	# 	newname = newname.strip()
	else:
		if u.isdigit():
			u = int(u)
			if 0 < u <= len(items):
				down(status, pos, items[u-1])
			else:
				status['log'] += 'input out of bound : {input}'.format(input=u)
		else:
			if u in loweritems:
				i = loweritems.index(u)
				u = items[i]
				down(pos, u)
			else:
				status['log'] += 'invalid input : {input}'.format(input=u)
	status['position'] = pos
	return status

def up(l):
	try:
		l.pop()
	except IndexError:
		pass
	return l
def top(l):
	l = []
	return l
def down(status, l, sel):	
	if not status['task']:
		l.append(sel)
	else:	
		file = status['workdir'] + '/' + sel
		excute(file)
	return l
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

if __name__=='__main__':
	main()