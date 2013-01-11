import os
class path:
	def __init__(self, inputpath):
		self.inputpath = inputpath
		self.path = inputpath.replace("\\", "/")
		lastpath = self.path.split("/")[-1]

		if '.' in lastpath:
			self.name = lastpath
			self.nameWithoutExtension = ".".join(lastpath.split(".")[:-1])
			self.extension = lastpath.split(".")[-1]
			self.directory = "/".join(self.path.split("/")[:-1])
			self.parentdir = "/".join(self.path.split("/")[:-2])
		else: # if itself a directory
			self.name = ''
			self.extension = ''
			self.nameWithoutExtension = ''
			self.directory = self.path
			self.parentdir = "/".join(self.path.split("/")[:-1])
	def exist(self):
		return os.path.isfile(self.path)

	def existDir(self):
		return os.path.isdir(self.directory)

	def existParentDir(self):
		return os.path.isdir(self.parentdir)
		

