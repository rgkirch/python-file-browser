from PyQt4 import QtGui
from PyQt4.QtCore import QThread
import sys, os, dis

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

class FileObject():
    pass
class Default():
    default_directory = os.path.expanduser("~/")
    error = "Error: "
    class style():
        class directory():
            color = QtGui.QColor.blue
        class folder():
            color = QtGui.QColor.black

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

    def populateWidget(self, list_widget, current_directory):
        def nameToObj(name):
            temp = QtGui.QListWidgetItem()
            temp.setTextColor(QtGui.QColor("blue"))
            temp.setText(name)
            return temp
        try:
            file_list = os.listdir( current_directory )
            if file_list:
                file_list = list( map( nameToObj, file_list ) )
            list_widget.replaceItems( file_list )
        except FileNotFoundError:
            self.current_directory = self.default.default_directory
            print("FileNotFoundError:", self.default.error, "BentExplorerApp, populate(), listdir(not a valid dir)", file=sys.stderr)
        except:
            if isinstance( list_widget, QtGui.QListWidget ) and isinstance( current_directory, str ):
                print("something went wrong, BentExplorerApp, populateWidget()", file=sys.stderr)
            else:
                print("default exception:", "BentExplorerApp, populate expected params of type\n{0} and {1} but got params of type\n{2} and {3}".format( QtGui.QListWidget, str, type(list_widget), type(current_directory)), file=sys.stderr)



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
