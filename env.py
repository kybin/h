import os.path as ospath

#class env:
#	def __init__(self):
#		self.ProjectRoot = ospath.expandUser('~/prj')
#		self.ProjectTree = ospath.expandUser('~/dev/pipl/tree.txt')
#
#	def projectpath(self, prjname):
#		return '/'.join([self.ProjectRoot, prjname])

ProjectRoot = ospath.expanduser('~/prj')
ProjectTree = ospath.expanduser('~/dev/pipl/tree.txt')

def projectpath(prjname):
	return '/'.join([ProjectRoot, prjname])
