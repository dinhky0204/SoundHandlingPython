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
        # ax = plt.plot(timeArray, data)
        # plt.xlabel('time(s)')
        # plt.ylabel('amplitude')
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
        self.filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                                filetypes=(("wav files", "*.wav"), ("all files", "*.*")))

        if not self.filename:
            print "Exit!"
            self.window.destroy()
        else:
            self.box = Entry(window)
            self.fig = Figure(figsize=(6, 6))
            self.button = Button(window, text="check", command=self.plot)
            self.box.pack()
            self.button.pack()

    def plot (self):
        print "====>", self.box.get()
        hd = handling()
        FRAME_DURATION = 0.02
        status = 0
        return_value_of_handling = hd.sound_analy(self.filename, FRAME_DURATION)

        FRAME_LENGTH = return_value_of_handling[0]
        NUMBER_FRAME = return_value_of_handling[1]
        data = return_value_of_handling[2]
        samplerate = return_value_of_handling[3]

        a = self.fig.add_subplot(111)
        # a.scatter(v,x,color='red')
        # a.plot(p, range(2 +max(x)),color='blue')
        samplerate, data = wavfile.read(self.filename)
        data = data / (2. ** 15)
        timeArray = np.arange(0, len(data), 1)
        timeArray = timeArray / float(samplerate)
        a.plot(timeArray, data, color="blue")


        for i in xrange(0, (2 * NUMBER_FRAME - 1)):
            start_at = int(i * FRAME_LENGTH / 2)
            stop_at = int((i + 2) * FRAME_LENGTH / 2)
            tmp = hd.sum_of_squares(data[start_at:stop_at])
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

        a.set_title ("Estimation Grid", fontsize=16)
        a.set_ylabel("Y", fontsize=14)
        a.set_xlabel("X", fontsize=14)
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().pack_forget()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

window= Tk()
start= mclass (window)
window.mainloop()