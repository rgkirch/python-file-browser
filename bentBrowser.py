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

DEBUG = 1

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

		self.widget_list.grid( row=55 )
		self.widget_commandBar.grid( row=99 )

		self.default_directory = os.path.expanduser("~/")
		self.current_working_directory = self.default_directory
		self.contents = os.listdir( self.current_working_directory )
		self.contents = filter( lambda y: not y.startswith("."), self.contents )
		self.widget_list.replace_contents( self.contents )

	def __getstate__( self ):
		return pickle.dumps( self.contents ) + pickle.dumps( self.widget_list ) + pickle.dumps( self.widget_commandBar )

	def __setstate__( self, item ):
		print( item )
	
	def navigate_to_subdirectory( self, subdirectory ):
		"""Expects the name of a directory in the scope of the current directory."""
		if subdirectory in os.listdir( self.current_working_directory ):
			self.current_working_directory = os.path.join( self.current_working_directory, subdirectory )
			if DEBUG:
				print( "cd", subdirectory )
	def navigate_to_absolute_directory( self, absolute_path ):
		"""Expects absolute path."""
		# may be redundant with navigate_to_subdirectory
		pass
	
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
	#	ls was the last one entered
	#	<UP>(ls)<Up>(ls)<Up>(cd)
	# commands entered: sub_brad, sub_bravo, stash
	# dict = {s:{u:{b:{_:{b:{r:{a:{d:{},v:{o:{}}}}}}}},t:{a:{s:{h:{}}}}}}
	# aa,ab,b
	# dict = {a:{a:{},b:{}},b:{}}
	def __init__( self, parent_frame, parent_object ):
		tk.Entry.__init__( self, parent_frame, insertofftime=0 )
		# TODO figure out how to set columnconfigure to 1
		#self.configure(  )

		self.parent_object = parent_object

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

class Listing( tk.Listbox):
	"""
	A Listing object will display stuff. The user may use keyboard shortcuts to control aspects of how the stuff in the list is displayed.
	"""
	# The Listing can return a filename or dirname to the parent Explorer so that the Explorer can navigate to a new directory.
	# The Listing does not change folder itself. Just display whats given to it and it has options for changing the aesthetics.
	def __init__( self, parent_frame, parent_object ):
		"""Listing inheretis from listbox, call listbox init function to avoid error of not finding attribute tk."""
		tk.Listbox.__init__( self, parent_frame, selectmode=tk.EXTENDED )

	def __getstate__( self ):
		return None

	def __setstate__( self ):
		return None

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

class BentExplorerApp( tk.Tk ):
	def __init__( self, *args, **kwargs ):
		tk.Tk.__init__( self, *args, **kwargs )
		self.protocol( "WM_DELETE_WINDOW", self.destroy )

		self.wm_title("bent file explorer")
		#print( self.winfo_screenwidth() )
		frame_main = tk.Frame( self )
		frame_main.grid( row=55 )
		widget_file_explorer = Explorer( frame_main )

		btn_quit = tk.Button( self,
				text="QUIT",
				command=self.Quit )
		btn_quit.grid( row=99 )

	def __getstate__(self):
		return None

	def __setstate__(self):
		return None

	def save_app_state( self ):
		with open( "BentExplorerApp.pickle", "wb" ) as f:
			pickle.dump( self, f )

	def Quit( self ):
		#if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
		save_app_state()
		self.quit()

if __name__ == "__main__":
	app = BentExplorerApp()
	app.mainloop()
	#app.destroy()
