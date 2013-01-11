from PyQt4 import QtGui
from PyQt4 import QtCore
from pm_interface import Ui_MainWindow
import time, os, sys, prjutil, threading
import hou

global win_state
win_state = 0

class main_ui(QtGui.QMainWindow):
	def __init__(self,parent=None):
		global win_state

		try:
			QtGui.QWidget.__init__(self,parent)
			self.ui=Ui_MainWindow()
			self.ui.setupUi(self)
			
			self.prjFolder = "T:/03_RnD_server/Project"
			self.prjList = os.listdir(self.prjFolder)
			self.prjList = [prj for prj in self.prjList if not prj.startswith('_')]
			
			for i in self.prjList:
					self.ui.project_list.addItem(QtCore.QString(i))
					
			self.shotList = os.listdir("/".join([self.prjFolder, self.prjList[0], "work"]))
			self.shotList.sort()
		except:
			pass
		
		##for shot in self.shotList:
		##	item = QtGui.QListWidgetItem(QtCore.QString(shot))
		##	self.ui.cg_list.addItem(item)
		
		
		
	def slot_cglist(self):
		pass
		##print type(self.ui.cg_list)
		##print dir(self.ui.cg_list)
	
	def slot_exit(self):
		global win_state
		
	def slot_newshot(self):
		print 'New Shot'
		getshot = str(QtGui.QInputDialog.getText(self,"New Shot","type new shot name",0,'')[0])
		print getshot
		if getshot == '':
			pass
		else:
			currentPrj = self.prjList[self.ui.project_list.currentIndex()]
			shotFolder = "/".join([self.prjFolder, currentPrj, "work", getshot])
			outFolder = "/".join([self.prjFolder, currentPrj, "output", getshot])
			prjutil.makeDirTree(shotFolder, 'shot')
			os.makedirs(outFolder)
			print shotFolder
			print outFolder
			
			self.yb_refresh()
					
		
	def yb_refresh(self):
		self.ui.cg_list.clear()
		currentPrj = self.ui.project_list.currentIndex()
		workDir = "/".join([self.prjFolder, self.prjList[currentPrj], "work"])
		self.shotList = [item for item in self.shotList if os.path.isdir("/".join([workDir,item])) == True]
		self.shotList = [item for item in self.shotList if not item.startswith('_')]

		##self.shotList = [item for item in self.shotList if os.path.isdir(item) == True]
		self.shotList.sort()
		for shot in self.shotList:
			item = QtGui.QListWidgetItem(QtCore.QString(shot))
			self.ui.cg_list.addItem(item)
		
	def jm_refresh(self):
		self.ui.project_list.clear()
		self.prjList = os.listdir(self.prjFolder)
		self.prjList = [prj for prj in self.prjList if not prj.startswith('_')]
		
		for i in self.prjList:
				self.ui.project_list.addItem(QtCore.QString(i))
		
	def slot_newprj(self):
		getprj = str(QtGui.QInputDialog.getText(self,"New Project","type new project name",0,'')[0])
		if getprj == '':
			pass
		else:
			prjPath = "/".join([self.prjFolder, getprj])
			prjutil.makeDirTree(prjPath, 'project')
		
		self.jm_refresh()
		curprj = self.prjList.index(getprj)
		self.ui.project_list.setCurrentIndex(curprj)
		self.yb_refresh()

		
	def slot_refresh(self):
		self.jm_refresh()
		self.yb_refresh()
		
		
	def slot_prj(self):
		try:
			self.ui.cg_list.clear()
			
			currentPrj = self.ui.project_list.currentIndex()
			workDir = "/".join([self.prjFolder, self.prjList[currentPrj], "work"])
			self.shotList = os.listdir(workDir)

			self.shotList = [item for item in self.shotList if os.path.isdir("/".join([workDir,item])) == True]
			self.shotList = [item for item in self.shotList if not item.startswith('_')]
			self.shotList.sort()
			
			for shot in self.shotList:
				item = QtGui.QListWidgetItem(QtCore.QString(shot))
				self.ui.cg_list.addItem(item)
		except:
			pass
			
			
	def setVariable(self, name, value):
		global hou
		if value != None:
			hou.hscript("".join(["set -g ",name,"=",value]))
			print(" ".join(["set",str(name),"=",str(value)]))


	def slot_setprj(self):
		try:
			global hou
			print("")
			
			prjName = str(self.prjList[self.ui.project_list.currentIndex()])
			shotName = str(self.ui.cg_list.currentItem().text())
			
			self.setVariable("PRJNAME", prjName)
			self.setVariable("SHOTNAME", shotName)
			
			prj = self.prjFolder + "/" + prjName
			print("")
			
			self.setVariable("PRJ", prj)
			self.setVariable("JOB", "/".join([prj, "work", shotName, "houdini"]))
			self.setVariable("OUT", "/".join([prj, "output", shotName]))
			self.setVariable("COMMON", "/".join([prj, "common"]))

			self.close()
		except:
			pass
		

	
def get_window():
	try:
		app = QtGui.QApplication(sys.argv)
		myapp = main_ui()
		myapp.show()
		sys.exit(app.exec_())
	except:
		pass