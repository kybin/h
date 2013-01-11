# coding:utf-8

# 이 프로그램은 계속 열어놓고 프로그램을 실행시키거나 폴더를 열때 사용한다.
# 프로젝트의 구조는 다음중 하나가 된다.

# 1.쇼/시퀀스/씬/샷/리비전
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

def globalStatus(status):
	# shottree = checkTree()
	status['rootdir'] = env.path().ProjectRoot
	# status['guides'] = "상위로:'..', 맨위로:'/', 폴더열기:'open', 주 프로그램 변경:'default', 이름변경:'A > B'"
	status['guides'] = "opendir:'(o)open', default program:'(d)default', rename:'(r)rename'"
	status['guides'] += "\nselect:'(NUM)name', up:'..', top:'/' directory address:'.'"
	status['position'] = []

	return status

def localStatus(status):
	root = status['rootdir']
	pos = status['position']
	show, seq, scene, shot, shotname, rev = pos + (6-len(pos))*[None]

	if show:
		worklist = [show, 'work', seq, scene, shot]
		work = '/'.join([i for i in worklist if i])
		# print(work)
	else:
		work = ''

	workdir = root + '/' + work
	# print(workdir)
	items = sorted(os.listdir(workdir))
	items = [i for i in items if os.path.isdir(workdir + '/' + i) and not i.startswith('_')]

	# outdir = [show, 'out', seq, scene , shot]
	# out = [i for i in outdir if i]
	# outitems = os.listdir()

	status['show'] = show
	status['seq'] = seq
	status['scene'] = scene
	status['shot'] = shot
	status['position'] = pos
	status['work'] = work
	status['workdir'] = workdir
	status['items'] = items
	# status[''] = 
	return status

def up(l):
	return l[:-1]
def top(l):
	return []
def down(l, sel):
	l.append(sel)
	return l
def openDir(d):
	d = d.replace('/', '\\')
	os.system('explorer {dir}'.format(dir=d))
def excute():
	pass

def doSomething(status, userInput):
	u = userInput.lower()
	pos = status['position']
	items = [i.lower() for i in status['items']]
	workdir = status['workdir']
	print(items, userInput)
	if u in ['q', 'quit']:
		return False
	elif u in ['o', 'open']:		
		openDir(workdir)
	elif u == '..':
		pos = up(pos)
	elif u == '/':
		pos = top(pos)
	else:
		if u.isdigit():
			u = int(u)
			if 0 < u < len(items):
				pos = down(pos, items[u-1])
			else:
				print('input out of bound')
		else:
			if u in items:
				pos = down(pos, u)
			else:
				print('invalid input')
	status['position'] = pos
	return status

def showMessage(status):
	os.system('cls')
	show = status['show']
	seq = status['seq']
	scene = status['scene']
	shot = status['shot']
	items = [' : '.join(['{0: >5}'.format(i+1),j]) for i,j in enumerate(status['items'])]

	message = ''	
	if show:
		print('SHOW  : {0}'.format(show)); print
		if seq:
			print('SEQ   : {0}'.format(seq)); print
			if scene:
				print('SCENE : {0}'.format(scene));	print
				if shot:
					print('SHOT  : {0}'.format(shot)); print

				else: print('-'*75); print('SHOT')
			else: print('-'*75); print('SCENE')
		else: print('-'*75); print('SEQ')
	else: print('-'*75); print('SHOW')

	print('-'*75)
	print('\n'.join(items))
	print('-'*75)
	print(status['guides'])
	print('-'*75)
	try:
		print(status['results'])
		print('-'*75)
	except:
		pass
	print('>>>'),



def main():
	status = {}
	status = globalStatus(status)

	while status:
		status = localStatus(status)
		showMessage(status)
		userInput = raw_input()
		status = doSomething(status, userInput)
		# status['result']='냠'
		# break

if __name__=='__main__':
	main()