# I dream of making my own os one day. I will call it Bent os.

#from Tkinter import *
import Tkinter as tk
import tkMessageBox
import os

# main widget
class Listing( object ):
    def __init__(self, parent):
        self.lbx_dirs = tk.Listbox( parent,
                selectmode=tk.EXTENDED )
        self.lbx_dirs.grid()
        self.update()
    def update(self):
        for item in sorted(os.listdir( os.path.expanduser("~") + "/" )):
            self.lbx_dirs.insert(tk.END, item)

class BentExplorerApp( tk.Tk ):
    def __init__( self, *args, **kwargs ):
        tk.Tk.__init__( self, *args, **kwargs )
        self.protocol( "WM_DELETE_WINDOW", self.destroy )

        self.wm_title("bent file explorer")
        #print( self.winfo_screenwidth() )
        frame = tk.Frame()
        frame.grid( row=5 )
        bottom = tk.Frame()
        bottom.grid( row=10 )

        btn_quit = tk.Button( bottom,
                text="QUIT",
                command=self.Quit )
        btn_quit.grid()

        widget_file_explorer = Listing( frame )
    def Quit( self ):
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            self.quit()

app = BentExplorerApp()
app.mainloop()
#app.destroy()

