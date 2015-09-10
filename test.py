from Tkinter import *
import os

class App(Frame):
    def __init__(self, master):
        frame = Frame(master)
        frame.grid()
        #self.grid()

        top = Frame(frame)
        top.grid( row=0, columnspan=2 )
        left_half = Frame(frame)
        left_half.grid( column=0, row=1, sticky=N )
        right_half = Frame(frame)
        right_half.grid( column=1, row=1 )

        self.title_text = Message( top,
                text="bent file explorer" )

        self.btn_quit = Button( left_half,
                text="QUIT",
                command=frame.quit )

        self.btn_hello = Button( left_half,
                text="hello",
                command=self.hello )

        self.lbx_dirs = Listbox( right_half,
                selectmode=EXTENDED )

        self.title_text.grid()
        self.btn_hello.grid( column=0, row=0 )
        self.btn_quit.grid( column=0, row=1 )
        self.lbx_dirs.grid()

        #for item in sorted(os.listdir(".")):
        #    self.listbox.insert(END, item)

    def hello( self ):
        print "hello"

root = Tk()
app = App(root)
root.mainloop()
root.destroy()
