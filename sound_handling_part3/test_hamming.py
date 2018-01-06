from __future__ import division
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Tkinter import *
from matplotlib import pyplot as plt
from scipy.io import wavfile
import Tkinter, Tkconstants, tkFileDialog
import math
from numpy.fft import fft, fftshift

chunk = 1024
FRAME_DURATION = 0.04
list_f0 = []
filename = tkFileDialog.askopenfilename(initialdir="/home/dinhky/PycharmProjects/", title="Select sound file",
                                                filetypes=(("wav files", "*.wav"), ("all files", "*.*")))
samplerate, data = wavfile.read(filename)
data = data / (2. ** 15)
timeArray = np.arange(0, len(data), 1)
timeArray = timeArray / float(samplerate)
status = 0

FRAME_LENGTH = int(FRAME_DURATION * samplerate)
NUMBER_FRAME = int(len(data) / FRAME_LENGTH)
K = int(FRAME_LENGTH*4/5)
print "Number frame: ", NUMBER_FRAME
print "Frame length:", FRAME_LENGTH
print "Sample: ", samplerate

# data = np.random.uniform(-1,1,44100)
print data
# window = np.hamming(51)
plt.plot(window)
# plt.plot(timeArray, data)

plt.show()