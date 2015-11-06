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
    def replaceItems(self, items):
        self.clear()
        self.addItems(items)

class Defaults():
    default_directory = os.path.expanduser("~/")
    error = "Error: "

class BentExplorerApp(QtGui.QMainWindow):
    def __init__(self, parent=None):
        """
        >>> self.populateWidget("hello", "hi")
        """
        super().__init__(parent)
        self.defaults = Defaults()
        self.widgets = []
        self.current_directory = self.defaults.default_directory
        # explorerapp central widget is stacked widget with explorerapp as parent
        self.setCentralWidget(QtGui.QStackedWidget(self))
        # add widget to widgets list, widget has stacked widget as parent
        self.widgets.append(ListWidget(self.centralWidget()))
        # add widgets to stacked widget
        for widget in self.widgets:
            self.centralWidget().addWidget(widget)
        self.centralWidget().setCurrentIndex(0)
        #self.centralWidget().currentWidget().replaceItems(["one","two","three"])
        self.setWindowTitle("Bent File Explorer")
        self.show()
        self.populateWidget( self.centralWidget().currentWidget(), self.current_directory )

    def populateWidget(self, list_widget, current_directory):
        try:
            file_list = os.listdir( current_directory )
            list_widget.replaceItems( file_list )
        except FileNotFoundError:
            self.current_directory = self.defaults.default_directory
            print("FileNotFoundError:", self.defaults.error, "BentExplorerApp, populate(), listdir(not a valid dir)", file=sys.stderr)
        except:
            print("default exception:", "BentExplorerApp, populate expected (qListWidget, str) got ({0}, {1})".format(type(list_widget), type(current_directory)), file=sys.stderr)



    def browse_folder(self):
        self.centralWidget().currentWidget().clear()
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
