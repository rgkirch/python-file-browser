from PyQt4 import QtGui # Import the PyQt4 module we'll need
import sys # We need sys so that we can pass argv to QApplication

import listbox # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer

class App(QtGui.QMainWindow):
    def __init__(self):
        """
        >>> self.ui = listbox.Ui_rootWindow()
        >>> print( "ui", type( self.ui ) )
        ('ui', <class 'listbox.Ui_rootWindow'>)
        >>> print( "self", type( self ) )
        ('self', <class '__main__.App'>)
        """
        self.ui = listbox.Ui_rootWindow()
        super(self.__class__, self).__init__()
        self.ui.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined


def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = App()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
