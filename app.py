from PyQt4 import QtGui
from PyQt4 import QtCore
#from PyQt4.QtCore import QThread
#from PyQt4.QtCore import SIGNAL
import sys, os, stat
from enum import Enum, unique
from pathlib import Path

import searchInterface
import searchObjects

# show history from database
# when select prev search of do new search
# show stuff in current view

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

class Default:
    #default_directory = Path(os.path.expanduser("~"))
    default_directory = Path(os.path.expanduser(os.getcwd()))
    error = "Error: "
    class style:
        class directory:
            color = QtGui.QColor.blue
        class folder:
            color = QtGui.QColor.black

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

class ListWidget(QtGui.QListWidget):
    parent = None
    path = Default.default_directory 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.doubleClicked.connect(lambda: self.primary())

    def primary(self, items=None):
        if not items:
            items = self.selectedItems()
        if len(items) == 1:
            if items[0].item_type == Type.DIR:
                self.folder_primary(items[0])
        if items[0].item_type == Type.FILE:
            self.file_primary(items[0])

    def folder_primary(self, item):
        self.populate_widget(item.path)

    def file_primary(self, item):
        if sys.platform == "linux" or sys.platform == "linux2":
            os.popen( "xdg-open " + str(item.path.absolute()).replace(" ","\ ") )
        elif sys.platform == "win32":
            os.popen( "start " + str(item.path.absolute()).replace(" ","\ ") )
        elif sys.platform == "darwin":
            #print("NotImplemented", file=sys.stderr)
            os.popen("" + item.text().replace(" ","\ "))

    def replaceItems(self, items):
        self.clear()
        for item in map(FileItem, items):
            self.addItem(item)
        self.sortItems()

    def populate_widget(self, path=None):
        if path:
            self.path = path
        self.clear()
        dotdot = FileItem(self.path.parent)
        dotdot.setText("..")
        self.addItem(dotdot)
        for item in map(FileItem, self.path.iterdir()):
            self.addItem(item)
        self.sortItems()

    def createNewFile(self):
        name,ok = QtGui.QInputDialog.getText(self, "create empty file", "enter name of new file")
        if ok and name:
            os.chdir(str(self.path.absolute()))
            os.mknod(name)

    def renameFilename(self, items):
        item = items[0]
        name,ok = QtGui.QInputDialog.getText(self, "rename file", "enter name of file")
        if ok and name:
            os.chdir(str(self.path.absolute()))
            os.rename(str(item.path.absolute()), name)

    def deleteFiles(self, items):
        os.chdir(str(self.path.absolute()))
        for item in items:
            os.remove(str(item.path.absolute()))

    def contextMenuEvent(self, event):
        contextMenuActions = []
        contextMenu = QtGui.QMenu()
        contextMenuActions.append(QtGui.QAction("create new file", self))
        contextMenuActions[-1].triggered.connect(lambda: self.createNewFile())
        contextMenuActions.append(QtGui.QAction("rename", self))
        contextMenuActions[-1].triggered.connect(lambda: self.renameFilename(self.selectedItems()))
        contextMenuActions.append(QtGui.QAction("delete file(s)", self))
        contextMenuActions[-1].triggered.connect(lambda: self.deleteFiles(self.selectedItems()))
        contextMenuActions.append(QtGui.QAction("create new zip from files", self))
        contextMenuActions[-1].triggered.connect(lambda: self.actionZip(self.selectedItems()))
        contextMenuActions.append(QtGui.QAction("unzip files", self))
        contextMenuActions[-1].triggered.connect(lambda: self.actionUnZip(self.selectedItems()))
        contextMenuActions.append(QtGui.QAction("remove spaces from filename", self))
        contextMenuActions[-1].triggered.connect(lambda: self.renameWithoutSpaces(self.selectedItems()))
        contextMenu.addActions(contextMenuActions)
        action = contextMenu.exec_(QtGui.QCursor.pos())
        #print(contextMenuActions.index(action))
        self.populate_widget()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.primary(self.selectedItems())
        elif event.key() == QtCore.Qt.Key_Backspace:
            self.populate_widget(self.path.parent)
        else:
            super().keyPressEvent(event)

    def actionUnZip(self, items):
        searchInterface.extractZip(str(items[0]), str(self.path.absolute()))

    def actionZip(self, items):
        """Creates new zip file."""
        name,ok = QtGui.QInputDialog.getText(self, "zip files", "enter name of new zip file")
        # user clicked ok and entered a string
        if ok and name:
            if not name.endswith(".zip"):
                name += ".zip"
            # already file of same name
            if name in os.listdir(str(self.path.absolute())):
                overwrite_confirm = QtGui.QMessageBox(self)
                overwrite_confirm.setText("the file "+name+" already exists in the current directory")
                overwrite_confirm.setInformativeText("Do you want to overwrite the file?")
                overwrite_confirm.setStandardButtons(QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
                overwrite = overwrite_confirm.exec_()
                if overwrite == QtGui.QMessageBox.Ok:
                    # backup name so can delete it later
                    old_name = name
                    while name in os.listdir(str(self.path.absolute())): 
                        name += ".tmp"
                    name = os.path.join(str(self.path.absolute()), name)
                    searchInterface.createNewZip(name, list(map(str, items)), str(self.path.absolute()))
                    # rename to remove .tmp
                    os.remove(old_name)
                    os.rename(name, old_name)
            else:
                name = os.path.join(str(self.path.absolute()), name)
                searchInterface.createNewZip(name, list(map(str, items)), str(self.path.absolute()))

    def renameWithoutSpaces(self, items):
        for item in items:
            os.chdir(str(item.path.parent.absolute()))
            oldname = item.path.name
            newname = oldname.replace(" ", "")
            if newname not in os.listdir():
                os.rename(oldname, newname)

class FileItem(QtGui.QListWidgetItem):
    path = None
    item_type = None
    def __init__(self, path):
        super().__init__()
        # future: pass in options for things you want like 'hash=true'
        if(isinstance(path, str)):
            self.path = Path(path)
        else:
            self.path = path
        # set listWidgetItem display text
        self.setText(self.path.name)
        # temporary implementation of property setting
        if self.path.is_file():
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
        # explorerapp central widget is stacked widget with explorerapp as parent
        self.setCentralWidget(QtGui.QStackedWidget(self))
        # add widget to widgets list, widget has stacked widget as parent
        self.listwidget = ListWidget(self)
        self.searchwidget = SearchesWidget(self)
        # add widgets to stacked widget
        self.centralWidget().addWidget(self.listwidget)
        self.centralWidget().addWidget(self.searchwidget)
        self.centralWidget().setCurrentIndex(0)
        #self.centralWidget().currentWidget().replaceItems(["one","two","three"])
        self.setWindowTitle("Bent File Explorer")

        self.setupMenuBar()
        #text = QtGui.QInputDialog.getText(self, "title", "lable")

        self.show()
        self.listwidget.populate_widget()

    def setIndex(self, index, refresh=True):
        if(index == 1):
            items = searchObjects.SearchObject.getSearchesByUser(0)
            self.searchwidget.replaceItems(items)
            self.centralWidget().setCurrentIndex(index)
        else:
            self.centralWidget().setCurrentIndex(index)
            if refresh:
                self.listwidget.populate_widget()

    def setupMenuBar(self):
        menu = QtGui.QMenu("menu", self)
        search = QtGui.QMenu("search", self)
        view = QtGui.QMenu("view", self)
        actions = []
        actions.append(QtGui.QAction("quit", menu))
        actions[-1].triggered.connect(QtGui.qApp.quit)
        menu.addActions(actions)
        actions = []
        actions.append(QtGui.QAction("recursive regex search", menu))
        actions[-1].triggered.connect(lambda: self.searchPrompt(True))
        actions.append(QtGui.QAction("regex search in current directory", menu))
        actions[-1].triggered.connect(lambda: self.searchPrompt(False))
        actions.append(QtGui.QAction("regex recursive search and replace", menu))
        actions[-1].triggered.connect(lambda: self.searchReplacePrompt(True))
        search.addActions(actions)
        actions = []
        actions.append(QtGui.QAction("browser", menu))
        actions[-1].triggered.connect(lambda: self.setIndex(0))
        actions.append(QtGui.QAction("past searches", menu))
        actions[-1].triggered.connect(lambda: self.setIndex(1))
        view.addActions(actions)
        self.menuBar().addMenu(menu)
        self.menuBar().addMenu(search)
        self.menuBar().addMenu(view)

    def searchPrompt(self, recursive):
        string, bool = QtGui.QInputDialog.getText(self, "enter search string", "searches are fun")
        if bool and string:
            if isinstance(self.centralWidget().currentWidget(), ListWidget):
                #print(self.centralWidget().currentWidget(), " is an instance of ", ListWidget)
                directory = str(self.centralWidget().currentWidget().path)
            else:
                #print(self.centralWidget().currentWidget(), " is not an instance of ", ListWidget)
                directory = QtGui.QFileDialog.getExistingDirectory()
            result = searchInterface.getSearchResults(0, directory, str(string), recursive)
            self.listwidget.replaceItems(result)

    def searchReplacePrompt(self, recursive):
        search, boolone = QtGui.QInputDialog.getText(self, "search and replace", "enter string for search")
        replace, booltwo = QtGui.QInputDialog.getText(self, "search and replace", "enter string for replace")
        if boolone and booltwo and search:
            if isinstance(self.centralWidget().currentWidget(), ListWidget):
                #print(self.centralWidget().currentWidget(), " is an instance of ", ListWidget)
                directory = str(self.centralWidget().currentWidget().path)
            else:
                #print(self.centralWidget().currentWidget(), " is not an instance of ", ListWidget)
                directory = QtGui.QFileDialog.getExistingDirectory()
            result = searchInterface.getPotentialRenames(0, directory, str(search), str(replace), recursive)
            for key in result.keys():
                rename_confirm = QtGui.QMessageBox(self)
                rename_confirm.setText("going to rename\n{} to\n{}".format(key, result[key]))
                rename_confirm.setInformativeText("Is this OK?")
                rename_confirm.setStandardButtons(QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
                rename = rename_confirm.exec_()
                if rename == QtGui.QMessageBox.Ok:
                    # filter out empty string just in case path ended with '/'
                    thing = list(filter(lambda y: y, result[key].split("/")))[-1]
                    print("thing", thing)
                    print("in dir", os.listdir(directory))
                    if thing in os.listdir(directory):
                        print("thing in directory")
                        overwrite_confirm = QtGui.QMessageBox(self)
                        overwrite_confirm.setText("the file "+thing+" already exists in the current directory")
                        overwrite_confirm.setInformativeText("Do you want to overwrite the file?")
                        overwrite_confirm.setStandardButtons(QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
                        overwrite = overwrite_confirm.exec_()
                        if overwrite == QtGui.QMessageBox.Ok:
                            os.rename(key, result[key])
            #searchInterface.renameFiles(result)
            #self.listwidget.replaceItems(result) #delete


def main():
    app = QtGui.QApplication(sys.argv[1:])
    window = BentExplorerApp()
    #window.show()
    app.setFont(QtGui.QFont("monospace", 14))
    app.exec_()

if __name__ == '__main__':
    main()
