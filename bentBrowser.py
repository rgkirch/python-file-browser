# I dream of making my own os one day. I will call it Bent os.

#from Tkinter import *
import Tkinter as tk
import os

# main widget
class File_Explorer(  ):
    def __init__(self, parent):
        top = tk.Frame( parent )
        top.grid( row=0, columnspan=2 )
        left_half = tk.Frame( parent )
        left_half.grid( column=0, row=1, sticky=tk.N )
        right_half = tk.Frame( parent )
        right_half.grid( column=1, row=1 )

        self.title_text = tk.Message( top,
                text="bent file explorer" )

        self.btn_quit = tk.Button( left_half,
                text="QUIT",
                command=parent.quit )

        self.lbx_dirs = tk.Listbox( right_half,
                selectmode=tk.EXTENDED )

        self.title_text.grid()
        self.btn_quit.grid( column=0, row=1 )
        self.lbx_dirs.grid()
    def update(self):
        print( "update" )
        for item in sorted(os.listdir(".")):
            self.lbx_dirs.insert(END, item)

class BentExplorerApp( tk.Tk ):
    def __init__( self, *args, **kwargs ):
        tk.Tk.__init__( self, *args, **kwargs )
        frame = tk.Frame( self )
        frame.grid()
        fe = File_Explorer( frame )

app = BentExplorerApp()
app.mainloop()
app.destroy()
