# main widget
class Explorer:
	"""
	Allows the user to navigate the file tree.
	Uses two widgets to convey this: Explorer and Listing.
	Explorer controls the file navigation.
	"""
	def __init__(self, parent_frame ):
		self.widget_list = Listing( parent_frame, self )
		self.widget_commandBar = CommandBar( parent_frame, self )

		self.widget_list.grid( row=55, sticky='nesw' )
		parent_frame.rowconfigure(0, weight=1)
		parent_frame.columnconfigure('all', weight=1)

		self.default_directory = os.path.expanduser("~/")
		self.current_working_directory = self.default_directory
		self.contents = os.listdir( self.current_working_directory )
		self.contents = filter( lambda y: not y.startswith("."), self.contents )
		self.widget_list.replace_contents( self.contents )

	def __getstate__( self ):
		return pickle.dumps( self.contents ) + pickle.dumps( self.widget_list ) + pickle.dumps( self.widget_commandBar )

	def __setstate__( self, item ):
		print( item )
	
	def navigate_to_subdirectory( self, index ):
		"""Expects the name of a directory in the scope of the current directory."""
		# TODO check that directory exists, os.path.exists may return false if we're lacking permisions even if it does exist
		# checks the current dir for subdir, change current dir to join(current dir, subdir)
		subdirectory = os.listdir( self.current_working_directory )[index]
		newpath = os.path.join( self.current_working_directory, subdirectory )
		if newpath.isdir() and subdirectory in os.listdir( self.current_working_directory ):
			self.current_working_directory = newpath
			if DEBUG:
				print( "cd", subdirectory )

	def navigate_to_absolute_directory( self, absolute_path ):
		"""Expects absolute path."""
		# may be redundant with navigate_to_subdirectory
		#self.

	def listing_item_selected( self, item ):
		self.navigate_to_subdirectory( item )
