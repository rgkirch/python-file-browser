# TODO - directoies should be a differnt color - pass indicies to a funciton in listing that says to color certain ones

from Listing import Listing
from CommandBar import CommandBar
import os
import sys

# TODO maybe have the top level set config options for each including the debug flag
DEBUG = True

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

# main widget
class Explorer( tk.Frame ):
    """
    Allows the user to navigate the file tree.
    Uses two widgets to convey this: Explorer and Listing.
    Explorer controls the file navigation.
    """
    def __init__(self, parent ):
        #tk.Frame.__init__( self, parent )
        super().__init__( parent )
        self.parent = parent

        self.hide_dot_files_folders = True
        self.separate_dirs_n_files = True

        self.widget_list = Listing( self )
        self.widget_commandBar = CommandBar( self )

        self.widget_list.grid( row=0, sticky='nesw' )
        self.widget_commandBar.grid( row=1, sticky='nesw' )

        self.default_directory = os.path.expanduser("~/")
        self.current_working_directory = self.default_directory
        self.navigate_to_absolute_path( self.current_working_directory )


    def __getstate__( self ):
        # have a way to save the default directory
        #return pickle.dumps( self.contents ) + pickle.dumps( self.widget_list ) + pickle.dumps( self.widget_commandBar )
        return None

    def __setstate__( self, item ):
        return None

    # post grid row column
    def pgrc_configure(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure('all', weight=1)

    def navigate_to_absolute_path( self, absolute_path ):
        """Expects absolute path.
        Fills in the listing widget with the contents of the directory and colors some of the entries light gray."""
        if os.path.isdir( absolute_path ):
            os.chdir( absolute_path )
            self.current_working_directory = absolute_path
            self.contents = os.listdir( self.current_working_directory )
            if self.hide_dot_files_folders:
                self.contents = list( filter( lambda y: not y.startswith("."), self.contents ) )
            self.widget_list.replace_contents( self.contents )
            for index, entry in enumerate( self.widget_list.get( 0, tk.END ) ):
                if os.path.isdir( os.path.join( self.current_working_directory, entry ) ):
                    self.widget_list.itemconfig( index, fg='dark blue' )

    def primary( self, items ):
        if len( items ) == 1:
            newpath = os.path.join( self.current_working_directory, items[0] )
            if os.path.isdir( newpath ):
                self.folder_primary( newpath )
            else:
                self.file_primary( newpath )
        return None

    def folder_primary( self, abs_path ):
        self.parent.status_last_command( "cd " + str(abs_path) )
        #print( "cd", path)
        self.navigate_to_absolute_path( abs_path )
        return None

    def file_primary( self, path ):
        if sys.platform == "linux" or sys.platform == "linux2":
            #os.system( "xdg-open " + path )
            os.popen( "xdg-open " + path )
        elif sys.platform == "win32":
            os.popen( "start " + path )
        elif sys.platform == "darwin":
            os.popen( "" + path )
        return None

    def secondary( self, items ):
        print( items )

    def alt_up( self, event ):
        head = os.path.dirname( self.current_working_directory )
        self.navigate_to_absolute_path( head )
        return None

