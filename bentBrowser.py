# I dream of making my own os one day. I will call it Bent os.

#from Tkinter import *
import Tkinter as tk
import tkMessageBox
import os

# main widget
class Listing( object ):
    command_history = []
    command_history_index = 0
    def __init__(self, parent):
        self.lbx_dirs = tk.Listbox( parent,
                selectmode=tk.EXTENDED )
        self.lbx_dirs.grid( row=0 )

        self.command_bar = tk.Entry( parent )
        self.command_bar.bind( "<Return>", self.run_command )
        self.command_bar.bind( "<Up>", self.display_previous_command )
        self.command_bar.grid( row=10 )

        self.update()
    def run_command( self, event ):
        "record entered command in history, reset history index, and run command"
        print( self.command_bar.get() )
        self.command_history.append( self.command_bar.get() )
        self.command_history_index = len( self.command_history )
        self.command_bar.delete( 0, tk.END )
    def display_previous_command( self, event ):
        pass
    def update(self):
        self.lbx_dirs.delete( 0, tk.END )
        for item in sorted(os.listdir( os.path.expanduser("~") + "/" )):
            self.lbx_dirs.insert(tk.END, item)
    def debug_print_selected( self ):
        print( self.lbx_dirs.curselection() )

class BentExplorerApp( tk.Tk ):
    def __init__( self, *args, **kwargs ):
        tk.Tk.__init__( self, *args, **kwargs )
        self.protocol( "WM_DELETE_WINDOW", self.destroy )

        self.wm_title("bent file explorer")
        #print( self.winfo_screenwidth() )
        # if you leave out the master widget as seen here, tkinter uses the most recently created root window as master
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

