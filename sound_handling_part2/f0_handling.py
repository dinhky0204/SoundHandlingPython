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

def f0_handling:
    
FRAME_DURATION = 0.04
list_f0 = []
new_sig = []
fix_data = []
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
if type(data[0]) is np.ndarray:
    for i in xrange(0, (len(data)-1)):
        fix_data.append(data[i][0])
    data = fix_data
print "len of new_data: ", len(fix_data)
    


def r_item(k, arr):
    total = 0
    for n in xrange(0, (FRAME_LENGTH-k-1)):
        total = total + arr[n]*arr[n+k]
    # print total
    return total

def r_total(new_data):
    new_r = []
    for k in xrange(0, K):
        new_r.append(r_item(k, new_data))
    return new_r
def max_of_arr(arr):
    result = 0
    flag = [-2,-2]
    for i in arr:
        if i > flag:
            result = i
            flag = i
    return result

def f0(r):
    star_point = int(samplerate/450)
    end_point = int(samplerate/80)
    print "start point: ", star_point
    print "end point: ", end_point
    point = np.argmax(r[star_point:end_point])+star_point
    print "point: ", point
    # point_max = max_of_arr(r[200:600])
    # point = FRAME_LENGTH/point
    # print "end point: ", end_point
    # print "min:", point_min   
    # print "point max:", point_max
    # print "test: ", np.amax(r[200:600])
    print "f0: ", samplerate/point
    return samplerate/point

def sum_of_squares(xs):
    total = 0
    # total = np.array([1])
    for i in xs:
        squared = i * i
        total += squared
    return total
count = 0

for i in xrange(0,2*NUMBER_FRAME-1):
    tmp = 0
    R = []
    min = 0
    start_at = int(i * FRAME_LENGTH/2)
    stop_at = int((i + 2) * FRAME_LENGTH/2)
    tmp = sum_of_squares(data[start_at:stop_at])
    # tmp = np.sum(data[start_at:stop_at]**2)
    tmp = np.sqrt(abs(tmp))
    if tmp >= 1:
        tmp = (i+1)*FRAME_LENGTH/(2*samplerate)
        array_time.append(tmp)
        count += 1
        new_data = data[start_at: stop_at]
        new_sig.extend(new_data)
        R = r_total(new_data)
        list_f0.append(f0(R))
        if count == 12:
            plt.plot(R)
            break
        # print start_at
        # print stop_at
        if status == 0:
            # plt.plot([start_at/samplerate, start_at/samplerate], [-1, 1], color="red")
            print "RED"
            status = 1
    else:
        if status == 1:
            # plt.plot([stop_at/samplerate, stop_at/samplerate], [-1, 1], color="blue")
            status = 0
            print "BLUE"
            status = 0