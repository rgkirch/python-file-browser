from PyQt4 import QtGui
from PyQt4.QtCore import QThread
import sys, os, dis

class Thread(QThread):
    def __init__(self):
        QThread.__init__(self)
    def __del__(self):
        self.wait()
    def run(self):
        pass
class ListWidget(QtGui.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        print( "list widget init" )
    def replaceItems(self, items):
        self.clear()
        self.addItems(items)


class BentExplorerApp(QtGui.QMainWindow):
    def __init__(self, parent=None):
        """
        >>> self.ui = listbox.Ui_rootWindow()
        >>> print( "self", type( self ) )
        ('self', <class '__main__.App'>)
        """
        super().__init__(parent)
        self.widgets = []
        # explorerapp central widget is stacked widget with explorerapp as parent
        self.setCentralWidget(QtGui.QStackedWidget(self))
        # add widget to widgets list, widget has stacked widget as parent
        self.widgets.append(ListWidget(self.centralWidget()))
        # add widgets to stacked widget
        for widget in self.widgets:
            self.centralWidget().addWidget(widget)
        self.centralWidget().setCurrentIndex(0)
        self.centralWidget().currentWidget().replaceItems(["one","two","three"])

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
