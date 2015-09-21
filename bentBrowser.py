# I dream of making my own os one day. I will call it Bent os.

# general TODO
# figure out how to allow width of widget to expand as window expands, set weight to 1 not 0
# everything with pickle is in progress

# TODO check python version and use relevant tkinter virsion
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
#import tkMessageBox
# consider using trustedPickle instead
import pickle
import os

# TODO a better way to do this, maybe make a package and then say from package import *
from Explorer import Explorer
from Listing import Listing
from CommandBar import CommandBar

DEBUG = 1

class BentExplorerApp( tk.Tk ):
    """
    """
    def __init__( self, *args, **kwargs ):
        tk.Tk.__init__( self, *args, **kwargs )
        self.protocol( "WM_DELETE_WINDOW", self.destroy )

        self.wm_title("bent file explorer")
        self.text_last_command = tk.StringVar()
        #print( self.winfo_screenwidth() )

        widget_file_explorer = Explorer( self )
        frame_bottom = tk.Frame( self )

        btn_quit = tk.Button( frame_bottom,
            text="QUIT",
            command=self.Quit )

        lbl_last_command = tk.Label( frame_bottom,
                textvariable = self.text_last_command )

        widget_file_explorer.grid( row=0, sticky='nesw' )
        #post grid row column configure - must be called after grid but should be specified by the widget itself, not here
        widget_file_explorer.pgrc_configure()
        frame_bottom.grid( row=1, sticky='nesw' )
        btn_quit.grid( column=2, sticky='e' )
        lbl_last_command.grid( column=0, sticky='w' )

        self.rowconfigure('0', weight=1)
        self.columnconfigure('all', weight=1)
        frame_bottom.columnconfigure('all', weight=1)


    def __getstate__( self ):
        return None

    def __setstate__( self ):
        return None

    def save_app_state( self ):
        with open( "BentExplorerApp.pickle", "wb" ) as f:
            pickle.dump( self, f )

    def Quit( self ):
        #if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
        self.save_app_state()
        self.quit()

    def status_last_command( self, text ):
        self.text_last_command.set( text )

if __name__ == "__main__":
    app = BentExplorerApp()
    app.mainloop()
    #app.destroy()
