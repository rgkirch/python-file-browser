from PyQt4 import QtGui
from PyQt4.QtCore import QThread
import sys, os, stat, itertools
from enum import Enum, unique
from pathlib import Path

# notes, should handle files as 'file objects' not just strings
# should be able to query file.isdir or file.size
# could then pass to style() so that listWidgetItems can be made with dirs blue and stuff


class Thread(QThread):
    def __init__(self):
        QThread.__init__(self)
    def __del__(self):
        self.wait()
    def run(self):
        print("hello")
        window = QtGui.QMainWindow()
        window.show()

@unique
class Type(Enum):
    """Just for types, not to be instantiated."""
    DIR, FILE, UNSET = list(range(3))
    def __lt__(self, other):
        return self.value < other.value

class ListWidget(QtGui.QListWidget):
    parent = None
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

    def populate_widget(self, path):
        self.clear()
        for item in map(FileItem, path.iterdir()):
            self.addItem(item)
        self.sortItems()

    def event(self, event):
        handled = super().event(event)
        if isinstance(event, QtGui.QKeyEvent):
            #print(event.key())
            pass
        elif isinstance(event, QtGui.QContextMenuEvent):
            self.contextMenu(event)
        return handled

    def contextMenu(self, event):
        contextMenu = QtGui.QMenu()
        contextMenuEntries = []
        contextMenu.addAction("test one")
        contextMenu.addAction("test two")
        contextMenu.exec_(QtGui.QCursor.pos())

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
    path = None
    item_type = None
    def __init__(self, path):
        super().__init__()
        # future: pass in options for things you want like 'hash=true'
        self.path = path
        # set listWidgetItem display text
        self.setText(path.name)
        # temporary implementation of property setting
        if path.is_file():
            self.item_type = Type.FILE
        elif path.is_dir:
            self.item_type = Type.DIR
            self.setTextColor(QtGui.QColor("blue"))

    def __lt__(self, other):
        if self.item_type == other.item_type:
            return str(self.path) < str(other.path)
        else:
            return self.item_type < other.item_type

    def __str__(self):
        return str(self.path)

class BentExplorerApp(QtGui.QMainWindow):
    def __init__(self, parent=None):
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

        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        self.menuBar()

        self.show()
        self.centralWidget().currentWidget().populate_widget(self.current_directory)

def main():
    app = QtGui.QApplication(sys.argv[1:])
    window = BentExplorerApp()
    #window.show()
    app.exec_()

if __name__ == '__main__':
    main()
