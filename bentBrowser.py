# I dream of making my own os one day. I will call it Bent os.

from Tkinter import *
import os

# main widget
class File_Explorer():
    def __init__(self, parent):
        top = Frame( parent )
        top.grid( row=0, columnspan=2 )
        left_half = Frame( parent )
        left_half.grid( column=0, row=1, sticky=N )
        right_half = Frame( parent )
        right_half.grid( column=1, row=1 )

        self.title_text = Message( top,
                text="bent file explorer" )

        self.btn_quit = Button( left_half,
                text="QUIT",
                command=parent.quit )

        self.lbx_dirs = Listbox( right_half,
                selectmode=EXTENDED )

        self.title_text.grid()
        self.btn_quit.grid( column=0, row=1 )
        self.lbx_dirs.grid()
    def update(self):
        for item in sorted(os.listdir(".")):
            self.lbx_dirs.insert(END, item)

class App():
    def __init__(self, root):
        frame = Frame(root)
        frame.grid()
        fe = File_Explorer( frame )

root = Tk()
app = App(root)
root.mainloop()
root.destroy()
