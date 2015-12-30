from PyQt4 import QtGui
from BentExplorer import MainWindow
import sys

app = QtGui.QApplication(sys.argv[1:])
window = MainWindow()
#window.show()
app.setFont(QtGui.QFont("monospace", 14))
app.exec_()
