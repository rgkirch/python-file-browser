try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

class Listing( tk.Listbox):
    """
    A Listing object will display stuff. The user may use keyboard shortcuts to control aspects of how the stuff in the list is displayed.
    """
    # The Listing can return a filename or dirname to the parent Explorer so that the Explorer can navigate to a new directory.
    # The Listing does not change folder itself. Just display whats given to it and it has options for changing the aesthetics.
    def __init__( self, parent ):
        """Listing inheretis from listbox, call listbox init function to avoid error of not finding attribute tk."""
        #tk.Listbox.__init__( self, parent, selectmode=tk.EXTENDED )
        super().__init__( parent, selectmode=tk.EXTENDED )
        self.config( font="monospace 14" )

        self.parent = parent
        self.bind( "<Double-Button-1>", self.primary )
        self.bind( "<Return>", self.primary )
        self.bind( "<Alt-Up>", self.parent.alt_up )
        self.bind( "<Escape>", self.key_escape )
        self.bind( "<Key>", self.key_pressed )
        self.rowconfigure('all', weight=1)
        self.columnconfigure('all', weight=1)
        self.keys = []

    def __getstate__( self ):
        return None

    def __setstate__( self ):
        return None

    def key_escape(self, event):
        try:
            if self.keys[0] == "/":
                self.keys = []
                self.parent.refresh_list()
                print("escaping search")
        except IndexError:
            print("escape")

    def key_pressed(self, event):
        char = repr(event.char).replace("'", "")
        if len(char) > 1:
            print("listing key_pressed: oh, no,", char, "length > 1")
        if char:
            self.keys.append(char)
            if len(self.keys) > 1 and self.keys[0] == "/":
                self.parent.filter_list("".join(self.keys[1:]))
            else:
                self.keys = [char]
        print("".join(self.keys))

    def primary( self, event ):
        #self.parent.listing_items_selected( self.curselection )
        selection = self.curselection()
        contents = self.get( 0, tk.END )
        self.parent.primary( [ contents[int(x)] for x in selection ] )
        return None

    def secondary( self, event ):
        pass

    def pickle( self ):
        with open( "listing.pickle", "wb" ) as f:
            pickle.dump( self, f )

    def replace_contents( self, contents ):
        self.delete( 0, tk.END )
        for item in contents:
            self.insert( 0, item )

    def append_contents( self, contents ):
        for item in contents:
            self.insert( tk.END, item )
