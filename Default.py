from PyQt4 import QtGui
from pathlib import Path
import os

class Default:
    #default_directory = Path(os.path.expanduser("~"))
    default_directory = Path(os.path.expanduser(os.getcwd()))
    error = "Error: "
    class style:
        class directory:
            color = QtGui.QColor.blue
        class folder:
            color = QtGui.QColor.black
