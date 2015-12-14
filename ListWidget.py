from PyQt4 import QtGui
from Default import Default

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
        for item in map(ListWidgetItem, items):
            self.addItem(item)
        self.sortItems()

    def populate_widget(self, path=None):
        if path:
            self.path = path
        self.clear()
        dotdot = ListWidgetItem(self.path.parent)
        dotdot.setText("..")
        self.addItem(dotdot)
        for item in map(ListWidgetItem, self.path.iterdir()):
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
        name = str(items[0].path.absolute())
        if name.endswith(".zip"):
            name = name[:-4]
        num = 0
        newname = name
        while os.path.isfile(newname) or os.path.isdir(newname):
            newname = name + str(num)
            num += 1
        os.mkdir(newname)
        searchInterface.extractZip(str(items[0]), newname)

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
