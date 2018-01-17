import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Tkinter import *
from scipy.io import wavfile
import Tkinter, Tkconstants, tkFileDialog
from matplotlib import pyplot as plt
import math
from scipy.io.wavfile import write
from pygame import mixer
import wave

class mclass:
    def __init__(self,  window):
        self.window = window
        self.filename = tkFileDialog.askopenfilename(initialdir="/home/dinhky/PycharmProjects/", title="Select sound file",
                                                filetypes=(("wav files", "*.wav"), ("all files", "*.*")))
        self.new_sig = []
        self.hamming_sig = []
        self.samplerate = 0
        self.frame_len = 0
        if not self.filename:
            print "Exit!"
            self.window.destroy()
        else:
            self.box = Entry(window)
            self.quit_btn = Button(window, text="QUIT", bg= "red", fg="black", command=self.window.quit)
            self.quit_btn.pack(side="bottom")
            samplerate, data = wavfile.read(self.filename)
            data = data / (2. ** 15)
            plt.plot(data)
            plt.show()
window= Tk()
start= mclass (window)
window.mainloop()
