import hou
import os
import shutil
import time
import filebox

def setVariable(name, value):
    hou.hscript("set -g {name} = {value}".format(name=name, value=value))
    print("set {name} = {value}".format(name=name, value=value))

def SaveBackupRender(node):
	renderpath = node.parm('sopoutput').eval()

	if hou.hipFile.hasUnsavedChanges():
		hou.hipFile.saveAsBackup()

	src = hou.hipFile.path()
	dstd = os.path.dirname(renderpath)
	dstf = filebox.prefix(renderpath)+'.'+time.strftime('%Y_%m%d_%Hh%Mm%Ss', time.localtime())+'.hip'

	if os.path.isdir(dstd):
		shutil.copyfile(src, dstf)
		node.parm('execute').pressButton()
	else:
		print("there isn't such a directory")