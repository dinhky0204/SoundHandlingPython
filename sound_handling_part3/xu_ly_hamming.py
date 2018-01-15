import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Tkinter import *
from scipy.io import wavfile
import Tkinter, Tkconstants, tkFileDialog
import math

class handling:
    def sound_analy(self, filename, FRAME_DURATION):
        samplerate, data = wavfile.read(filename)
        data = data / (2. ** 15)
        timeArray = np.arange(0, len(data), 1)
        timeArray = timeArray / float(samplerate)
        FRAME_LENGTH = FRAME_DURATION * samplerate
        NUMBER_FRAME = int(len(data) / FRAME_LENGTH)
        TIME = (float)(len(data) / samplerate);
        print "Frame length: ", FRAME_LENGTH
        print "Number frame: ", NUMBER_FRAME
        print "Length: ", len(data)
        print "Time: ", TIME
        return [FRAME_LENGTH, NUMBER_FRAME, data, samplerate]

    def sum_of_squares(self, xs):
        sum_of_squares = 0
        for i in xs:
            squared = i * i
            sum_of_squares += squared
        return sum_of_squares

    def min_of_square(self, arr):
        min = 1
        for i in arr:
            i = abs(i)
            if i == 0:
                min = 0
                break
        return min

class mclass:
    def __init__(self,  window):
        self.window = window
        self.filename = tkFileDialog.askopenfilename(initialdir="/home/dinhky/PycharmProjects/", title="Select sound file",
                                                filetypes=(("wav files", "*.wav"), ("all files", "*.*")))

        if not self.filename:
            print "Exit!"
            self.window.destroy()
        else:
            self.box = Entry(window)
            lbl3 = Label(window, text="Energy", width=6, font=("Helvetica", 14))
            lbl3.pack(side=TOP, anchor=N, pady=5)
            self.fig = Figure(figsize=(6, 6))
            self.button = Button(window, text="CHECK", bg = "#497e1e", fg="white", command=self.plot)
            # self.play = Button(window, text="PLAY", bg = "#497e1e", fg="white", command=self.hamming_handling)
            self.quit_btn = Button(window, text="QUIT", bg= "red", fg="black", command=self.window.quit)
            self.box.pack()
            self.quit_btn.pack(side="bottom")
            self.button.pack()

    def hamming_handling(SEL_FIRST):
        print "test function"

    def plot (self):
        print "Nang luong ====>", self.box.get()
        hd = handling()
        FRAME_DURATION = 0.04
        status = 0
        return_value_of_handling = hd.sound_analy(self.filename, FRAME_DURATION)

        FRAME_LENGTH = return_value_of_handling[0]
        NUMBER_FRAME = return_value_of_handling[1]
        NUMBER_FRAME_NEW = 0
        data = return_value_of_handling[2]
        samplerate = return_value_of_handling[3]

        a = self.fig.add_subplot(111)
        a.clear()
        samplerate, data = wavfile.read(self.filename)
        data = data / (2. ** 15)
        timeArray = np.arange(0, len(data), 1)
        timeArray = timeArray / float(samplerate)
        a.plot(timeArray, data, color="blue")


        for i in xrange(0, (2 * NUMBER_FRAME - 1)):
            start_at = int(i * FRAME_LENGTH / 2)
            stop_at = int((i + 2) * FRAME_LENGTH / 2)
            tmp = hd.sum_of_squares(data[start_at:stop_at])
            print "tmp:", tmp
            tmp = math.sqrt(abs(tmp))
            test = hd.min_of_square(data[start_at:stop_at])
            # tmp = 0.046
            if tmp < float(self.box.get()):
                if status == 0:
                    a.plot([(i) * FRAME_LENGTH / (2 * samplerate), (i) * FRAME_LENGTH / (2 * samplerate)], [-1, 1],
                             color="blue")
                    status = 1
                elif min(data[start_at:stop_at]) == 0:
                    a.plot([(i) * FRAME_LENGTH / (2 * samplerate), (i) * FRAME_LENGTH / (2 * samplerate)], [-1, 1],
                             color="yellow")
                    status = 0
            elif tmp > float(self.box.get()):
                if status == 1:
                    a.plot([(i) * FRAME_LENGTH / (2 * samplerate), (i) * FRAME_LENGTH / (2 * samplerate)], [-1, 1],
                             color="red")
                    status = 0
                elif min(data[start_at:stop_at]) == 0:
                    a.plot([(i) * FRAME_LENGTH / (2 * samplerate), (i) * FRAME_LENGTH / (2 * samplerate)], [-1, 1],
                             color="yellow")
                    status = 0
            else:
                status = 0

        a.set_title ("Plotting sound", fontsize=16)
        a.set_ylabel("amplitude", fontsize=14)
        a.set_xlabel("time(s)", fontsize=14)
        if hasattr(self, 'canvas'):
            # self.canvas.get_tk_widget().pack_forget()
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

window= Tk()
start= mclass (window)
window.mainloop()
