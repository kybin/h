# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pm_v01.ui'
#
# Created: Thu Oct 18 16:11:50 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(370, 473)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(370, 473))
        MainWindow.setMaximumSize(QtCore.QSize(370, 473))
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Project Manager", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../Users/Jungmin/Program Files/Nuke6.3v2/plugins/icons/cj_sub1.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStatusTip(_fromUtf8(""))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setIconSize(QtCore.QSize(24, 24))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setTabShape(QtGui.QTabWidget.Rounded)
        MainWindow.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.project_list = QtGui.QComboBox(self.centralwidget)
        self.project_list.setGeometry(QtCore.QRect(10, 10, 221, 25))
        self.project_list.setObjectName(_fromUtf8("project_list"))
        self.cg_list = QtGui.QListWidget(self.centralwidget)
        self.cg_list.setGeometry(QtCore.QRect(10, 50, 221, 401))
        self.cg_list.setObjectName(_fromUtf8("cg_list"))
        self.new_prj = QtGui.QPushButton(self.centralwidget)
        self.new_prj.setGeometry(QtCore.QRect(240, 10, 121, 23))
        self.new_prj.setText(QtGui.QApplication.translate("MainWindow", "New Project", None, QtGui.QApplication.UnicodeUTF8))
        self.new_prj.setObjectName(_fromUtf8("new_prj"))
        self.new_shot = QtGui.QPushButton(self.centralwidget)
        self.new_shot.setGeometry(QtCore.QRect(240, 50, 121, 23))
        self.new_shot.setText(QtGui.QApplication.translate("MainWindow", "New Shot", None, QtGui.QApplication.UnicodeUTF8))
        self.new_shot.setObjectName(_fromUtf8("new_shot"))
        self.set_project = QtGui.QPushButton(self.centralwidget)
        self.set_project.setGeometry(QtCore.QRect(240, 380, 121, 71))
        self.set_project.setText(QtGui.QApplication.translate("MainWindow", "Set Project", None, QtGui.QApplication.UnicodeUTF8))
        self.set_project.setCheckable(False)
        self.set_project.setChecked(False)
        self.set_project.setObjectName(_fromUtf8("set_project"))
        self.refresh_btn = QtGui.QPushButton(self.centralwidget)
        self.refresh_btn.setGeometry(QtCore.QRect(240, 340, 121, 31))
        self.refresh_btn.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.refresh_btn.setCheckable(False)
        self.refresh_btn.setChecked(False)
        self.refresh_btn.setObjectName(_fromUtf8("refresh_btn"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.cg_list, QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem*)")), MainWindow.slot_cglist)
        QtCore.QObject.connect(self.new_shot, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.slot_newshot)
        QtCore.QObject.connect(self.new_prj, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.slot_newprj)
        QtCore.QObject.connect(self.project_list, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), MainWindow.slot_prj)
        QtCore.QObject.connect(self.set_project, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.slot_setprj)
        QtCore.QObject.connect(self.refresh_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.slot_refresh)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

