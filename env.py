class path:
	def __init__(self):
		self.ProjectRoot = "/home/yongbin/dev/Show"
		self.ProjectTree = "/homeyongbin/dev/pipl/folder_tree.txt"

def projectpath(prj):
	return '/'.join([path().ProjectRoot, prj])
