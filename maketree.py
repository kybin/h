#-*-coding:utf-8-*-
import os
import re
import sys
import posixpath as path

def __checkConflict(treename, treedict, recursionlist=[]):
	print(treename, recursionlist)
	if treename in recursionlist:
		recursionlist.append(treename)
		print('error : recursion conflict!')
		print(' -> '.join(recursionlist))
		sys.exit(1)

	recursionlist.append(treename)
	branches = [i.rstrip() for i in treedict[treename].splitlines() if i.strip()]
	print(branches)
	for b in branches:
		print(b)
		b = b.strip()
		if b.startswith('@'):
			treename = b.replace('@', '', 1)
			if  treename in treedict:
				__checkConflict(treename, treedict, recursionlist)
	return


def __parseTree(treestr):
	branches = [i.rstrip() for i in treestr.splitlines() if i.strip()]
	defaultdepth = branches[0].count('\t') # expand to spaces

	dirs= []
	tree = []
	for b in branches:
		dirname = b.strip()
		depth = b.count('\t')-defaultdepth

		if depth < 0: # if depth is below zero, raise error
			print('please check your tree : {0}'.format(path.join(*dirs)))
			sys.exit(1)

		dirs = dirs[:depth]
		dirs.append(dirname)

		try:	
			dirs[depth] 
		except: 
			# depth != len(dirs[:depth]) + 1
			# means depth jump forward more than 1 step
			print('please check your tree : {0}'.format(path.join(*dirs)))
			raise IndexError

		tree.append(path.join(*dirs))
	return tree


def __parseFile(text):
	splits = re.findall(r'@\w+\s*\{.+?\}', text, re.S)
	treedict = {}

	for i in splits:
		obj = re.compile(r'''
			@
			(?P<name>\w+)
			\s*
			\{
			(?P<value>.+?)
			\}'''
			, re.S | re.X)

		s = obj.search(i)
		treedict[s.group('name')]=s.group('value')

	return treedict


def make(treename, dir):
	thisfilepath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
	treefile = path.join(thisfilepath, 'folder_tree.txt')
	with open(treefile) as f:
		text = f.read()

	treedict = __parseFile(text)
	
	# __checkConflict(treename, treedict)	
	
	treestr = treedict[treename]
	if treestr:
		branches = __parseTree(treestr)

		if branches:
			for b in branches:
				print(path.join(dir, b))
				os.makedirs(path.join(dir, b))
	

if __name__=="__main__":
	tree, dir = sys.argv[1:3]
	make(tree, dir)
