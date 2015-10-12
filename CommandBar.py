try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

class CommandBar( tk.Entry ):
    """
    The commandbar will allow the user to enter longer command strnigs.
    If the user wants to enter a vim style substitution command, the user may do so here.
    The user may also use the <Up><Down> keys to view previous commands
    """
    # TODO set size limit for command_history - maybe
    # because there is a separate object for CommandBar each instance will have its own command history

    # if enter ren and hit up, complete to rename(if entered previously)
    # dict = {rename:[0,3],ls:[1,5,6],cd:[2,4]}
    #   ls was the last one entered
    #   <UP>(ls)<Up>(ls)<Up>(cd)
    # commands entered: sub_brad, sub_bravo, stash
    # dict = {s:{u:{b:{_:{b:{r:{a:{d:{},v:{o:{}}}}}}}},t:{a:{s:{h:{}}}}}}
    # aa,ab,b
    # dict = {a:{a:{},b:{}},b:{}}
    def __init__( self, parent ):
        #tk.Entry.__init__( self, parent, insertofftime=0 )
        super().__init__( parent, insertofftime=0 )
        # TODO figure out how to set columnconfigure to 1
        #self.configure(  )

        self.parent = parent

        self.command_history = [""]
        self.command_history_index = 0
        self.command_history_length = 0

        # delete nothing then insert the empty string...
        self.delete( 0, tk.END )
        self.insert( 0, self.command_history[ self.command_history_index ] )

        self.bind( "<Return>", self.save_command)
        self.bind( "<Up>", self.display_previous_command )
        self.bind( "<Down>", self.display_next_command )
        self.bind( "<Left>", lambda y: None )
        self.bind( "<Right>", lambda y: None )
    
    def __getstate__( self ):
        # TODO maybe, have it save the 100 most popular commands in command history for autocomplete when reopen
        return pickle.dumps( (self.command_history, self.command_history_index, self.command_history_length) )

    def __setstate__( self, item ):
        print( item )


    def save_command( self, event ):
        """record entered command in history, reset history index"""
        text_command = self.get()
        if text_command:
            self.delete( 0, tk.END )
            # replace len(commandhis) with saved value for performance nicrease
            self.command_history[ -1 : len( self.command_history ) ] = [ text_command, "" ]
            self.command_history_index = len( self.command_history ) - 1

    def display_previous_command( self, event ):
        """Show the previous(by index) command in the command bar. If there was any text in the command bar, it will become the last entry of the command history. Different than hiting <Return>"""
        if self.command_history_index > 0:
            if self.command_history_index == len( self.command_history ) - 1:
                self.command_history[ -1 ] = self.get()
            self.command_history_index -= 1
            self.delete( 0, tk.END )
            self.insert( 0, self.command_history[ self.command_history_index ] )

    def display_next_command( self, event ):
        """Show the next(by index) command in the command bar."""
        if self.command_history_index < len( self.command_history ) - 1:
            self.command_history_index += 1
            self.delete( 0, tk.END )
            self.insert( 0, self.command_history[ self.command_history_index ] )
