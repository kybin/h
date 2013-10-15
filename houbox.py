import hou
import os
import shutil
import time
# dependency
import filebox

def setVariable(name, value):
    hou.hscript("set -g {name} = {value}".format(name=name, value=value))
    print("set {name} = {value}".format(name=name, value=value))

def SaveBackupRender(node):
	'''	this may useful for rop operators
		rop_geometry, mantra, mdd, etc...
	'''
	# Save
	if hou.hipFile.hasUnsavedChanges():
		hou.hipFile.saveAsBackup()

	# Backup - copy current working hip file to render directory
	workingfile = hou.hipFile.path()
	renderpath = node.parm('sopoutput').eval()
	renderdir = os.path.dirname(renderpath)
	backupfile = filebox.prefix(renderpath)+'.'+time.strftime('%Y_%m%d_%Hh%Mm%Ss', time.localtime())+'.hip'
	
	if os.path.isdir(renderdir):
		shutil.copyfile(workingfile, backupfile)
	else:
		print("there isn't such a directory")
		return False
		
	# Render
	node.render()
