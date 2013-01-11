class path:
	def __init__(self):
		self.ProjectRoot = "T:/03_RnD_server/Project"
		self.ProjectTree = "T:/03_RnD_server/Project/__setting__/folder_tree.txt"

def projectpath(prj):
	return '/'.join([path().ProjectRoot, prj])