from PyQt4 import QtGui
from PyQt4.QtCore import QThread
import sys
import os
import listbox

class Thread(QThread):
    def __init__(self):
        QThread.__init__(self)
    def __del__(self):
        self.wait()
    def run(self):
        pass

class BentExplorerApp(QtGui.QMainWindow):
    def __init__(self):
        """
        >>> self.ui = listbox.Ui_rootWindow()
        >>> print( "ui", type( self.ui ) )
        ('ui', <class 'listbox.Ui_rootWindow'>)
        >>> print( "self", type( self ) )
        ('self', <class '__main__.App'>)
        """
        super().__init__()
        self.ui = listbox.Ui_rootWindow()
        self.ui.setupUi(self)
        self.ui.btnBrowse.clicked.connect(self.browse_folder)
        self.ui.actionAppQuit.triggered.connect(self.close)
        self.setWindowTitle("My Window")
        self.show()
    def browse_folder(self):
        self.ui.listWidget.clear()
        directory = QtGui.QFileDialog.getExistingDirectory(self,"Pick a folder")
        if directory:
            for file_name in os.listdir(directory): 
                self.ui.listWidget.addItem(file_name)

def main():
    app = QtGui.QApplication(sys.argv[1:])
    window = BentExplorerApp()
    app.exec_()

if __name__ == '__main__':
    main()
