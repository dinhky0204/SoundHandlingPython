from Tkinter import *
import ttk

class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(side = "bottom")
        self.initUI()
    def initUI(self):
        self.entrythingy = Entry()
        self.entrythingy.pack()

        # Label(self.master, text="First").grid(row=0)
        # Label(self.master, text="Second").grid(row=1)

        label1 = ttk.Label(text="W", style="BW.TLabel")
        label1.pack(side = "left")

        frame3 = Frame(self)
        frame3.pack(fill=BOTH, expand=True)
        lbl3 = Label(frame3, text="Review", width=6)
        lbl3.pack(side=LEFT, anchor=N, padx=5, pady=5)
        self.entry1 = Entry(frame3)
        self.entry1.pack(fill=X, padx=5, expand=True)

        self.contents = StringVar()

        self.contents.set("frame number")
        # self.contents.grid(row=0, column = 2)
        self.entrythingy["textvariable"] = self.contents

        # and here we get a callback when the user hits return.
        # we will have the program print out the value of the
        # application variable when the user hits return
        self.entrythingy.bind('<Key-Return>',
                              self.print_contents)
        fred = Button(self, text="Test fred", fg="red", bg="blue", command = self.printcontent)
        fred.pack(side="right")
        quit_btn = Button(self, text="QUIT", fg="red", command = self.quit)
        quit_btn.pack(side = "right")

    def print_contents(self, event):
        print "hi. contents of entry is now ---->", \
              self.contents.get()
    def printcontent(self):
        print "This is content: "
        print self.entry1.get()
root = Tk()
app = App(master=root)
app.mainloop()
root.destroy()