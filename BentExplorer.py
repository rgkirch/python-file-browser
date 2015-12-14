from PyQt4 import QtGui
from collections import OrderedDict
from ListWidget import ListWidget

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.widgets = []
        self.setCentralWidget(QtGui.QStackedWidget(self))
        self.listwidget = ListWidget(self)
        self.centralWidget().addWidget(self.listwidget)
        self.centralWidget().setCurrentIndex(0)
        self.setWindowTitle("Bent File Explorer")
        self.setupMenuBar()
        self.show()
        self.listwidget.populate_widget()

    def setCurrentIndex(self, index):
        self.centralWidget().setCurrentIndex(index)

    def makeMenuBarEntry(self, parent_menu, parent_dict):
        for key in parent_dict.keys():
            menu = QtGui.QMenu(key, self)
            sub = dict[key]
            if isinstance(sub, dict):
                parent_menu.addMenu(makeMenuBarEntry(new_menu, sub))
            elif isinstance(sub, str):
                parent_menu.addActions()
            else:
                print("error, something unique lctauet")
                sys.exit("unknown type")
        
    def setupMenuBar(self):
        menu_layout = {
            "menu":{
                "quit":{}
            }
        }
        menu = makeMenuBarEntry(self.menuBar(), menu_layout)
        menu = QtGui.QMenu("menu", self)
        search = QtGui.QMenu("search", self)
        view = QtGui.QMenu("view", self)
        actions = []
        actions.append(QtGui.QAction("quit", menu))
        actions[-1].triggered.connect(QtGui.qApp.quit)
        menu.addActions(actions)
        actions = []
        search.addActions(actions)
        actions = []
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
                    # test for existance of file (for collision)
                    if os.path.isfile(result[key]) or os.path.isdir(result[key]):
                        overwrite_confirm = QtGui.QMessageBox(self)
                        overwrite_confirm.setText("the file "+thing+" already exists in the directory")
                        overwrite_confirm.setInformativeText("Do you want to overwrite the file?")
                        overwrite_confirm.setStandardButtons(QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
                        overwrite = overwrite_confirm.exec_()
                        if overwrite == QtGui.QMessageBox.Ok:
                            #searchInterface.renameFiles(result)
                            os.rename(key, result[key])
