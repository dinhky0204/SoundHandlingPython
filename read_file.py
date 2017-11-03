from scipy.io import wavfile
from matplotlib import pyplot as plt
from pylab import*
import numpy as np
import math
import wave
import sys
#Tkinter TkFileDialog TkCommonDialog
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
root = Tk()
root.filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("wav files","*.wav"),("all files","*.*")))
print (root.filename)
FRAME_DURATION = 0.02
# samplerate, data = wavfile.read(root.filename)
status = 0
# timeArray = arange(0, len(data), 1)
# timeArray = timeArray / float(samplerate)
# FRAME_LENGTH = FRAME_DURATION * samplerate
# NUMBER_FRAME = int(len(data)/FRAME_LENGTH)
# TIME = (float)(len(data)/samplerate);

def sound_analy(file_name, w):
    samplerate, data = wavfile.read(root.filename)
    data = data / (2. ** 15)
    timeArray = arange(0, len(data), 1)
    timeArray = timeArray / float(samplerate)
    FRAME_LENGTH = FRAME_DURATION * samplerate
    NUMBER_FRAME = int(len(data) / FRAME_LENGTH)
    TIME = (float)(len(data) / samplerate);
    print "Frame length: ", FRAME_LENGTH
    print "Number frame: ", NUMBER_FRAME
    print "Length: ", len(data)
    print "Time: ", TIME
    ax = plt.plot(timeArray, data)
    plt.xlabel('time(s)')
    plt.ylabel('amplitude')
    return [FRAME_LENGTH, NUMBER_FRAME, data, samplerate]

def sum_of_squares(xs):
    sum_of_squares=0
    for i in xs:
        squared = i * i
        sum_of_squares += squared
    return sum_of_squares

def min_of_square(arr):
    min = 1
    for i in arr:
        i = abs(i)
        if i == 0:
            min = 0
            break
    return min

return_value = sound_analy(root.filename, 0)
FRAME_LENGTH =return_value[0]
NUMBER_FRAME = return_value[1]
data = return_value[2]
samplerate = return_value[3]

for i in xrange(0, (2*NUMBER_FRAME-1)):
    start_at = int(i*FRAME_LENGTH/2)
    stop_at = int((i+2)*FRAME_LENGTH/2)
    tmp = sum_of_squares(data[start_at:stop_at])
    tmp = math.sqrt(abs(tmp))
    test = min_of_square(data[start_at:stop_at])
    # print tmp
    if tmp < 0.046:
        if status == 0:
            plt.plot([(i)*FRAME_LENGTH/(2*samplerate), (i)*FRAME_LENGTH/(2*samplerate)], [-1, 1], color="blue")
            status = 1
        elif min(data[start_at:stop_at]) == 0:
            plt.plot([(i) * FRAME_LENGTH / (2*samplerate), (i) * FRAME_LENGTH / (2*samplerate)], [-1, 1], color="yellow")
            status = 0
    elif tmp > 0.046:
        if status == 1:
            plt.plot([(i)*FRAME_LENGTH/(2*samplerate), (i)*FRAME_LENGTH/(2*samplerate)], [-1, 1], color="red")
            status = 0
        elif min(data[start_at:stop_at]) == 0:
            plt.plot([(i) * FRAME_LENGTH / (2*samplerate), (i) * FRAME_LENGTH / (2*samplerate)], [-1, 1], color="yellow")
            status = 0
    else:
        status = 0
plt.show()
