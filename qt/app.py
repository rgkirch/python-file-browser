from PyQt4 import QtGui
from PyQt4.QtCore import QThread
import sys, os, dis, stat, itertools
from enum import Enum, unique

# notes, should handle files as 'file objects' not just strings
# should be able to query file.isdir or file.size
# could then pass to style() so that listWidgetItems can be made with dirs blue and stuff

class Thread(QThread):
    def __init__(self):
        QThread.__init__(self)
    def __del__(self):
        self.wait()
    def run(self):
        pass
@unique
class Type(Enum):
    UNSET, FILE, DIR = range(3)

class Style():
    pass

class ListWidget(QtGui.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    def replaceItems(self, items):
        self.clear()
        # additem is overloaded for strings and listWidgetItems
        # additems only works for strings
        for item in items:
            self.addItem(item)

class Default():
    default_directory = os.path.expanduser("~/")
    error = "Error: "
    class style():
        class directory():
            color = QtGui.QColor.blue
        class folder():
            color = QtGui.QColor.black

class FileItem(QtGui.QListWidgetItem):
    item_type = Type.UNSET
    item_md5 = Type.UNSET
    def __init__(self, path_to_file):
        super().__init__()
        # future: pass in options for things you want like 'hash=true'
        self.setText(path_to_file)
        if os.path.exists(path_to_file):
            if os.path.isfile(path_to_file):
                self.item_type=Type.FILE
            elif os.path.isdir(path_to_file):
                self.item_type=Type.DIR
                self.setTextColor("blue")
            else:
                print("FileItem constructor, not file or dir")
        else:
            print("FileItem constructor, path {0} not exist".format(path_to_file))
    @property
    def item_md5(self):
        if self.item_md5 == Type.UNSET:
            #self.item_md5 = hashlib.md5()
            return item_md5
        else:
            return item_md5
class BentExplorerApp(QtGui.QMainWindow):
    def __init__(self, parent=None):
        """
        >>> self.populateWidget("hello", "hi")
        """
        super().__init__(parent)
        self.default = Default()
        self.widgets = []
        self.current_directory = self.default.default_directory
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

    def populateWidget(self, list_widget, directory):
        try:
            file_list = os.listdir( directory )
            if file_list:
                #file_list = list( map( FileItem, map(lambda y: , file_list) ) )
            list_widget.replaceItems( file_list )
        except FileNotFoundError:
            self.directory = self.default.default_directory
            print("FileNotFoundError:", self.default.error, "BentExplorerApp, populate(), listdir(not a valid dir)", file=sys.stderr)
        except:
            if isinstance( list_widget, QtGui.QListWidget ) and isinstance( directory, str ):
                print("something went wrong, BentExplorerApp, populateWidget()", file=sys.stderr)
            else:
                print("default exception:", "BentExplorerApp, populate expected params of type\n{0} and {1} but got params of type\n{2} and {3}".format( QtGui.QListWidget, str, type(list_widget), type(directory)), file=sys.stderr)



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
