# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'listbox.ui'
#
# Created: Tue Oct 13 16:22:25 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_rootWindow(object):
    def setupUi(self, rootWindow):
        rootWindow.setObjectName(_fromUtf8("rootWindow"))
        rootWindow.resize(438, 589)
        self.rootWidget = QtGui.QWidget(rootWindow)
        self.rootWidget.setObjectName(_fromUtf8("rootWidget"))
        self.gridLayout = QtGui.QGridLayout(self.rootWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.listWidget = QtGui.QListWidget(self.rootWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        font.setPointSize(10)
        self.listWidget.setFont(font)
        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnBrowse = QtGui.QPushButton(self.rootWidget)
        self.btnBrowse.setObjectName(_fromUtf8("btnBrowse"))
        self.horizontalLayout.addWidget(self.btnBrowse)
        self.btnQuit = QtGui.QPushButton(self.rootWidget)
        self.btnQuit.setObjectName(_fromUtf8("btnQuit"))
        self.horizontalLayout.addWidget(self.btnQuit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        rootWindow.setCentralWidget(self.rootWidget)
        self.menuBar = QtGui.QMenuBar(rootWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 438, 20))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        rootWindow.setMenuBar(self.menuBar)
        self.actionOh_thas_what = QtGui.QAction(rootWindow)
        self.actionOh_thas_what.setObjectName(_fromUtf8("actionOh_thas_what"))
        self.actionOh_snap = QtGui.QAction(rootWindow)
        self.actionOh_snap.setObjectName(_fromUtf8("actionOh_snap"))
        self.actionQuit = QtGui.QAction(rootWindow)
        self.actionQuit.setCheckable(False)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.menuFile.addAction(self.actionQuit)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(rootWindow)
        QtCore.QMetaObject.connectSlotsByName(rootWindow)

    def retranslateUi(self, rootWindow):
        rootWindow.setWindowTitle(_translate("rootWindow", "MainWindow", None))
        self.listWidget.setToolTip(_translate("rootWindow", "<html><head/><body><p>tooltip</p></body></html>", None))
        self.btnBrowse.setText(_translate("rootWindow", "list", None))
        self.btnQuit.setText(_translate("rootWindow", "quit", None))
        self.menuFile.setTitle(_translate("rootWindow", "File", None))
        self.actionOh_thas_what.setText(_translate("rootWindow", "oh, thas what", None))
        self.actionOh_snap.setText(_translate("rootWindow", "oh, snap", None))
        self.actionQuit.setText(_translate("rootWindow", "Quit", None))

