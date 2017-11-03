from Tkinter import *

class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"
    def say_goodbye(self):
        print "Good bye"
    def confirmMessage(self):
        print "Confirmed"

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "HELLO"
        self.hi_there['fg'] = "blue"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack({"side": "left"})

        self.confirm = Button(self)
        self.confirm["text"] = "CONFIRM"
        self.confirm["fg"] = "yellow"
        self.confirm["command"] = self.confirmMessage
        self.confirm.pack({"side": "left"})

        fred = Button(self, text="Test fred", fg="red", bg="blue")
        fred.pack(side= "left")

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
