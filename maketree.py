#-*-coding:utf-8-*-
import os
import re
import sys
import posixpath

def __parseTree(treestr):
	branches = [i.rstrip() for i in treestr.split('\n') if i.strip()]
	# print(branches)
	curtree= []
	accumtree = []

	if branches: # this is not perfect
		defaultdepth = branches[0].count('\t')
		# print(defaultdepth)
		branches = [i.replace('\t', '', defaultdepth) for i in branches]
		# print(branches)
	else:
		return None

	for b in branches:
		depth, name = b.count('\t'), b.strip()
		# print(depth, name)
		curtree = curtree[:depth]
		curtree.append(name)
		#print(curtree)

		try:
			curtree[depth]
		except IndexError:
			print('please check your tree : {0}'.format("/".join(curtree)))
			return False

		accumtree.append('/'.join(curtree))
	return accumtree


def __importTrees(text):
	splits = re.findall(r'@\w+\s*\{.+?\}', text, re.S)
	trees = {}

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
		trees[s.group('name')]=s.group('value')

	return trees

def make(tree, dir):
	thisfilepath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
	treefile = posixpath.join(thisfilepath, 'folder_tree.txt')
	with open(treefile) as f:
		text = f.read()

	imports = __importTrees(text)
	branches = __parseTree(imports[tree])

	if branches:
		for b in branches:
				print(posixpath.join(dir, b))
				os.makedirs(posixpath.join(dir, b))
	elif branches is False:
		print('Check tree "{name}"'.format(name=name))
	elif branches is None:
		print('No branches at "{name}"'.format(name=name))
	

if __name__=="__main__":
	tree = sys.argv[1]
	curdir = os.getcwd().replace('\\', '/')
	make(tree, curdir)
