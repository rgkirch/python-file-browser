# I dream of making my own os one day. I will call it Bent os.

#from Tkinter import *
import Tkinter as tk
import os

# main widget
class Listing( object ):
    def __init__(self, parent):
        self.title_text = tk.Message( parent,
                text="bent file explorer" )


        self.lbx_dirs = tk.Listbox( parent,
                selectmode=tk.EXTENDED )

        self.title_text.grid()
        self.lbx_dirs.grid()
    def update(self):
        print( "update" )
        for item in sorted(os.listdir(".")):
            self.lbx_dirs.insert(END, item)

class BentExplorerApp( tk.Tk ):
    def __init__( self, *args, **kwargs ):
        tk.Tk.__init__( self, *args, **kwargs )
        frame = tk.Frame()
        frame.grid( row=0 )
        bottom = tk.Frame()
        bottom.grid( row=10 )

        btn_quit = tk.Button( bottom,
                text="QUIT",
                command=self.quit )
        btn_quit.grid()

        widget_file_explorer = Listing( frame )

app = BentExplorerApp()
app.mainloop()
app.destroy()
