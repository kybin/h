class path:
	def __init__(self):
		self.ProjectRoot = "/home/yongbin/dev/SHOW"
		self.ProjectTree = "/home/yongbin/dev/pipl/folder_tree.txt"

def projectpath(prj):
	return '/'.join([path().ProjectRoot, prj])
