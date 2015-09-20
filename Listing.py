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
        tk.Listbox.__init__( self, parent, selectmode=tk.EXTENDED )
        self.parent = parent
        self.bind( "<Return>", self.item_selected )
        self.rowconfigure('all', weight=1)
        self.columnconfigure('all', weight=1)

    def __getstate__( self ):
        return None

    def __setstate__( self ):
        return None

    def item_selected( self, event ):
        self.parent.listing_item_selected( self.curselection )

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
