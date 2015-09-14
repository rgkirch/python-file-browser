# I dream of making my own os one day. I will call it Bent os.

#from Tkinter import *
import Tkinter as tk
import tkMessageBox
import os

# not used
class Vimregex( object ):
    """implement something like 'vimregex.com'"""
    vimregex_keywords = ["substitute"]

# main widget
class Explorer:
    """
    Allows the user to navigate the file tree.
    Uses two widgets to convey this: Explorer and List.
    """
    def __init__(self, parent):
        self.widget_list = List( parent )

        self.widget_commandBar = CommandBar( parent )

        self.widget_list.grid( row=55 )
        self.widget_commandBar.grid( row=99 )

    # TODO set size limit for command_history
    # TODO hiting up should show you the previous one, hiting down should show you the command you were just composing
    #       example, i enter the command 'renam' but don't hit enter, i hit <Up> <Down> and still see 'renam'
    

class CommandBar:
    """
    The commandbar will allow the user to enter longer command strnigs.
    If the user wants to enter a vim style substitution command, the user may do so here.
    The user may also use the <Up><Down> keys to view previous commands
    """
    # because there is a separate object for CommandBar each instance will have its own command history
    # dict = {rename:[0,3],ls:[1,5,6],cd:[2,4]}
    #   ls was the last one entered
    #   <UP>(ls)<Up>(ls)<Up>(cd)
    # commands entered: sub_brad, sub_bravo, stash
    # dict = {s:{u:{b:{_:{b:{r:{a:{d:{},v:{o:{}}}}}}}},t:{a:{s:{h:{}}}}}}
    # aa,ab,b
    # dict = {a:{a:{},b:{}},b:{}}
    def __init__( self, frame ):
        self.command_history = [""]
        self.command_history_index = 0
        self.command_history_length = 0
        self.tkEntry = tk.Entry( frame )

        self.tkEntry.delete( 0, tk.END )
        self.tkEntry.insert( 0, self.command_history[ self.command_history_index ] )

        self.tkEntry.bind( "<Return>", self.save_command)
        self.tkEntry.bind( "<Up>", self.display_previous_command )
        self.tkEntry.bind( "<Down>", self.display_next_command )


        #print( self.tkEntry.grid_info() )

    def grid( self, *args, **kwargs ):
        self.tkEntry.grid( row=kwargs[ "row" ] )

    def save_command( self, event ):
        """record entered command in history, reset history index"""
        text_command = self.tkEntry.get()
        if text_command:
            self.tkEntry.delete( 0, tk.END )
            # replace len(commandhis) with saved value for performance nicrease
            self.command_history[ -1 : len( self.command_history ) ] = [ text_command, "" ]
            self.command_history_index = len( self.command_history ) - 1

    def display_previous_command( self, event ):
        if self.command_history_index > 0:
            self.command_history_index -= 1
        self.insert_command_from_history()

    def display_next_command( self, event ):
        if self.command_history_index < len( self.command_history ) - 1:
            self.command_history_index += 1
        self.insert_command_from_history()

    def insert_command_from_history( self ):
        self.tkEntry.delete( 0, tk.END )
        self.tkEntry.insert( 0, self.command_history[ self.command_history_index ] )

class List:
    """
    A List object will display stuff. The user may use keyboard shortcuts to control aspects of how the stuff in the list is displayed.
    """
    def __init__( self, parent ):
        self.contents = []
        self.tkListbox = tk.Listbox( parent,
                selectmode=tk.EXTENDED )
        self.tkListbox.grid()

    def grid( self, *args, **kwargs ):
        self.tkListbox.grid( row=kwargs[ "row" ] )

    def display_list( self, list ):
        self.tkListbox.delete( 0, tk.END )
        self.tkListbox.insert( 0, list )

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
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            self.quit()

app = BentExplorerApp()
app.mainloop()
#app.destroy()
