from PyQt4 import QtGui

app = QtGui.QApplication([])

w = QtGui.QMainWindow()
menu = QtGui.QMenu("menu", w)

menu.addAction(QtGui.QAction('50%', menu, checkable=True))
menu.addAction(QtGui.QAction('100%', menu, checkable=True))
menu.addAction(QtGui.QAction('200%', menu, checkable=True))
menu.addAction(QtGui.QAction('300%', menu, checkable=True))
menu.addAction(QtGui.QAction('400%', menu, checkable=True))

w.menuBar().addMenu(menu)
w.show()
app.exec_()
