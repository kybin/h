class path:
	def __init__(self):
<<<<<<< HEAD
		self.ProjectRoot = "T:/03_RnD_server/10.FX"
		self.ProjectTree = "D:/pipl/folder_tree.txt"
=======
		self.ProjectRoot = "c:/users/yongbin/dev/SHOW"
		self.ProjectTree = "folder_tree.txt"
>>>>>>> 6d398c603063859ed360d6f007806018e7e83763

def projectpath(prj):
	return '/'.join([path().ProjectRoot, prj])
