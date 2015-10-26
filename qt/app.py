from PyQt4 import QtGui
from PyQt4.QtCore import QThread
import sys, os, dis
import hellothere, checkbox

class Thread(QThread):
    def __init__(self):
        QThread.__init__(self)
    def __del__(self):
        self.wait()
    def run(self):
        pass

class Hellothere( QtGui.QWidget, hellothere.Ui_Form ):
    def __init__(self, parent):
        super().__init__()
        super().setupUi(parent)

class Checkbox( QtGui.QWidget, checkbox.Ui_Form ):
    def __init__(self, parent):
        super().__init__()
        super().setupUi(parent)

class BentExplorerApp(QtGui.QMainWindow):
    def __init__(self, parent=None):
        """
        >>> self.ui = listbox.Ui_rootWindow()
        >>> print( "self", type( self ) )
        ('self', <class '__main__.App'>)
        """
        super().__init__(parent)
        self.stacked_layout = QtGui.QStackedLayout()
        #self.stacked_layout.addWidget(Hellothere(hello))
        #self.stacked_layout.addWidget(Checkbox(check))
        self.stacked_layout.addWidget(hellothere.Ui_Form())
        self.stacked_layout.addWidget(checkbox.Ui_Form())
        self.central_widget = QtGui.QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)
        self.stacked_layout.setCurrentIndex(0)
        #centralWidget.setCurrentWidget(self.centralWidget().widget(0))
        #self.centralWidget().widget(0).hide()

        #self.rootWindow = rootWindow.Ui_rootWindow()
        #self.widgets.append( self.rootWidget )
        #self.fileList = fileList.Ui_filelist()
        #self.widgets.append( self.fileList )

        #self.setupUi(self, self.widgets)

        #self.rootWidget.gridLayout.addItem( self.fileList )

        #self.ui.btnBrowse.clicked.connect(self.browse_folder)
        #self.ui.actionAppQuit.triggered.connect(QtGui.qApp.quit)
        #self.ui.actionAppQuit.setShortcut("q")
        self.setWindowTitle("Bent File Explorer")
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
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
