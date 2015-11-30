from PyQt4 import QtGui
from PyQt4 import QtCore
import sys
import app

lication = QtGui.QApplication(sys.argv[1:])
window = app.InputDialog()
lication.exec_()
