class path:
	def __init__(self):
		self.ProjectRoot = "D:/SHOW"
		self.ProjectTree = "D:/pipl/folder_tree.txt"

def projectpath(prj):
	return '/'.join([path().ProjectRoot, prj])