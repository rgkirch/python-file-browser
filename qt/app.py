from PyQt4 import QtGui
from PyQt4.QtCore import QThread
import sys, os, stat, itertools
from enum import Enum, unique
from pathlib import Path

# notes, should handle files as 'file objects' not just strings
# should be able to query file.isdir or file.size
# could then pass to style() so that listWidgetItems can be made with dirs blue and stuff


class Thread(QThread):
    """later"""
    def __init__(self):
        QThread.__init__(self)
    def __del__(self):
        self.wait()
    def run(self):
        pass

@unique
class Type(Enum):
    """Just for types, not to be instantiated."""
    UNSET, DIR, FILE = range(3)

class ListWidget(QtGui.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

    def populate_widget(self, path):
        self.clear()
        for item in map(FileItem, path.iterdir()):
            self.addItem(item)
        self.sortItems()

class Default():
    default_directory = Path(os.path.expanduser("~"))
    #default_directory = Path("~").expanduser()
    error = "Error: "
    class style():
        class directory():
            color = QtGui.QColor.blue
        class folder():
            color = QtGui.QColor.black

class FileItem(QtGui.QListWidgetItem):
    item_type = Type.UNSET
    item_md5 = Type.UNSET
    def __init__(self, path):
        super().__init__()
        # future: pass in options for things you want like 'hash=true'
        self.setText(path.name)
        if path.is_file():
            self.item_type=Type.FILE
        elif path.is_dir():
            self.item_type=Type.DIR
            self.setTextColor(QtGui.QColor("blue"))
        else:
            print("FileItem constructor, not file or dir")

    def __lt__(self, other):
        if self.item_type == Type.DIR and other.item_type == Type.FILE:
            return True
        elif self.item_type == Type.FILE and other.item_type == Type.DIR:
            return False
        elif self.item_type == other.item_type:
            return self.text() < other.text()
        else:
            print("error, file item lt")

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
        >>> self.populate_widget("hello", "hi")
        """
        super().__init__(parent)
        self.widgets = []
        self.current_directory = Default.default_directory
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
        self.centralWidget().currentWidget().populate_widget(self.current_directory)




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
