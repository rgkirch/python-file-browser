from PyQt4 import QtGui
from PyQt4 import QtCore
#from PyQt4.QtCore import QThread
#from PyQt4.QtCore import SIGNAL
import sys, os, stat
from enum import Enum, unique
from pathlib import Path
# notes, should handle files as 'file objects' not just strings
# should be able to query file.isdir or file.size
# could then pass to style() so that listWidgetItems can be made with dirs blue and stuff


#class Thread(QThread):
#    def __init__(self):
#        QThread.__init__(self)
#    def __del__(self):
#        self.wait()
#    def run(self):
#        print("hello")
#        window = QtGui.QMainWindow()
#        window.show()

@unique
class Type(Enum):
    """Just for types, not to be instantiated."""
    DIR, FILE, UNSET = list(range(3))
    def __lt__(self, other):
        return self.value < other.value

#class contextMenu(QtGui.QMenu):
#    contextMenuActions = []
#    def __init__(self, *argv):
#        super.__init__(*argv)
#        self.contextMenuActions.append(QtGui.QAction("test one", self))
#        self.contextMenuActions[0].trigger = lambda y: print("hello")
#        self.contextMenuActions.append(QtGui.QAction("test two", self))

class SearchesWidget(QtGui.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.doubleClicked.connect(lambda: self.select())

    def select(self):
        item = self.selectedItems()[0]
        self.parent.listwidget.replaceItems(item.searchObject.matchedFiles)
        self.parent.setIndex(0, refresh=False)

    def replaceItems(self, items):
        self.clear()
        for item in items:
            temp = QtGui.QListWidgetItem()
            temp.searchObject = item
            temp.setText(str(temp.searchObject.searchString))
            self.addItem(temp)

    def rerun(self, items):
        item = items[0]
        so = item.searchObject
        result = searchInterface.getSearchResults(so.userIdNum, so.directory, so.searchString, so.includeSubDirectories)
        self.parent.listwidget.replaceItems(result)
        self.parent.setIndex(0, refresh=False)

    def contextMenuEvent(self, event):
        contextMenuActions = []
        contextMenu = QtGui.QMenu()
        contextMenuActions.append(QtGui.QAction("re-run search", self))
        contextMenuActions[-1].triggered.connect(lambda: self.rerun(self.selectedItems()))
        contextMenu.addActions(contextMenuActions)
        action = contextMenu.exec_(QtGui.QCursor.pos())
