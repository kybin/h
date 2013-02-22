class path:
	def __init__(self):
		self.ProjectRoot = "T:/03_RnD_server/10.FX"
		self.ProjectTree = "D:/pipl/folder_tree.txt"

def projectpath(prj):
	return '/'.join([path().ProjectRoot, prj])
