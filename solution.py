# I dream of making my own os one day. I will call it Bent os.

#from Tkinter import *
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
#import tkMessageBox
import os

# main widget
class Explorer:
    def __init__(self, parent_frame ):
        self.widget_list = List( master=parent_frame )
        self.widget_list.grid()
class List( tk.Listbox):
    def __init__( self, master=None, cnf={}, **kw ):
        tk.Widget.__init__(self, master, 'listbox', cnf, kw)


class BentExplorerApp( tk.Tk ):
    def __init__( self, *args, **kwargs ):
        tk.Tk.__init__( self, *args, **kwargs )
        self.protocol( "WM_DELETE_WINDOW", self.destroy )

        self.wm_title("bent file explorer")
        #print( self.winfo_screenwidth() )
        # if you leave out the master widget as seen here, tkinter uses the most recently created root window as master
        frame_main = tk.Frame()
        frame_main.grid( row=5 )
        frame_bottom = tk.Frame()
        frame_bottom.grid( row=10 )

        btn_quit = tk.Button( frame_bottom,
                text="QUIT",
                command=self.Quit )
        btn_quit.grid()

        widget_file_explorer = Explorer( frame_main )
    def Quit( self ):
        #if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
        self.quit()

app = BentExplorerApp()
app.mainloop()
#app.destroy()
