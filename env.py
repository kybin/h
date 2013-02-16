class path:
	def __init__(self):
		self.ProjectRoot = "c:/users/yongbin/dev/SHOW"
		self.ProjectTree = "folder_tree.txt"

def projectpath(prj):
	return '/'.join([path().ProjectRoot, prj])
