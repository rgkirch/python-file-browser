# I dream of making my own os one day. I will call it Bent os.

#from Tkinter import *
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
#import tkMessageBox
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
    def __init__(self, parent_frame ):
        self.widget_list = List( master=parent_frame )
        self.widget_commandBar = CommandBar( master=parent_frame )

        self.widget_list.grid( row=55 )
        self.widget_commandBar.grid( row=99 )

    def update( self, *args, **kw ):
        print( "hello" )
        self.widget_list.update( args )

    # TODO set size limit for command_history
    # TODO hiting up should show you the previous one, hiting down should show you the command you were just composing
    #       example, i enter the command 'renam' but don't hit enter, i hit <Up> <Down> and still see 'renam'
    

class CommandBar( tk.Entry ):
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
    def __init__( self, master=None, cnf={}, **kw ):
        tk.Widget.__init__(self, master, 'entry', cnf, kw)
        
        #self.parent_object = 
        self.command_history = [""]
        self.command_history_index = 0
        self.command_history_length = 0
        #self.tkEntry = tk.Entry( master )

        self.delete( 0, tk.END )
        self.insert( 0, self.command_history[ self.command_history_index ] )

        self.bind( "<Return>", self.save_command)
        self.bind( "<Up>", self.display_previous_command )
        self.bind( "<Down>", self.display_next_command )

    def save_command( self, event ):
        """record entered command in history, reset history index"""
        text_command = self.get()
        if text_command:
            self.delete( 0, tk.END )
            # replace len(commandhis) with saved value for performance nicrease
            self.command_history[ -1 : len( self.command_history ) ] = [ text_command, "" ]
            self.command_history_index = len( self.command_history ) - 1
            self.parent_object.update( text_command )

    def display_previous_command( self, event ):
        if self.command_history_index > 0:
            self.command_history_index -= 1
        self.insert_command_from_history()

    def display_next_command( self, event ):
        if self.command_history_index < len( self.command_history ) - 1:
            self.command_history_index += 1
        self.insert_command_from_history()

    def insert_command_from_history( self ):
        self.delete( 0, tk.END )
        self.insert( 0, self.command_history[ self.command_history_index ] )

class List( tk.Listbox):
    """
    A List object will display stuff. The user may use keyboard shortcuts to control aspects of how the stuff in the list is displayed.
    """
    def __init__( self, master=None, cnf={}, **kw ):
        tk.Widget.__init__(self, master, 'listbox', cnf, kw)

        self.contents = []
        #self.tkListbox = tk.Listbox( master,
                #selectmode=tk.EXTENDED )
        self.grid()

    def update( self, args, sec ):
        self.contents.append( args )
        self.insert( tk.END, args )

    def display_list( self, list ):
        self.delete( 0, tk.END )
        self.insert( 0, list )

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
