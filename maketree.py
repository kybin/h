#-*-coding:utf-8-*-
import os
import re
import sys
import posixpath as path

def __parseTree(treestr):
	branches = [i.rstrip() for i in treestr.splitlines() if i.strip()]
	defaultdepth = branches[0].count('\t') # expand to spaces

	dirs= []
	tree = []
	for b in branches:
		dir = b.strip()
		depth = b.count('\t')-defaultdepth

		if depth < 0 or depth - len(dirs)  > 0: 
			# if depth is below zero
			# or "jumps forward" more than one step, then raise error
			print('please check your tree : {0}'.format(path.join(*dirs)))
			raise IndexError

		dirs = dirs[:depth]
		dirs.append(dir)

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
	treestr = treedict[treename]
	if treestr:
		branches = __parseTree(treestr)

	if branches:
		for b in branches:
				print(path.join(dir, b))
				os.makedirs(path.join(dir, b))
	# elif branches is False:
	# 	print('Check tree "{name}"'.format(name=name))
	# elif branches is None:
	# 	print('No branches at "{name}"'.format(name=name))
	

if __name__=="__main__":
	tree = sys.argv[1]
	curdir = os.getcwd().replace('\\', '/')
	make(tree, curdir)
