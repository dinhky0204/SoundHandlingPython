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
from scipy.io.wavfile import write

FRAME_DURATION = 0.04
list_f0 = []
new_sig = []
list_point = []
filename = tkFileDialog.askopenfilename(initialdir="/home/dinhky/PycharmProjects/", title="Select sound file",
                                                filetypes=(("wav files", "*.wav"), ("all files", "*.*")))
samplerate, data = wavfile.read(filename)
data = data / (2. ** 15)
timeArray = np.arange(0, len(data), 1)
timeArray = timeArray / float(samplerate)
status = 0

FRAME_LENGTH = int(FRAME_DURATION * samplerate)
NUMBER_FRAME = int(len(data) / FRAME_LENGTH)
NUMBER_FRAME_NEW = 0
K = int(FRAME_LENGTH*4/5)
print "Number frame: ", NUMBER_FRAME
print "Frame length:", FRAME_LENGTH
print "Sample: ", samplerate

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
    point_min = np.argmin(r[0:200])
    end_point = point_min + 600
    point_max = np.argmax(r[point_min:end_point])
    # point_max = max_of_arr(r[200:600])
    # point = FRAME_LENGTH/point
    print "end point: ", end_point
    print "min:", point_min   
    print "point max:", point_max
    # print "test: ", np.amax(r[200:600])
    print "f0: ", samplerate/(point_max/2+point_min)
    return samplerate/(point_max/2+point_min)

def sum_of_squares(xs):
    total = 0
    # total = np.array([1])
    for i in xs:
        squared = i * i
        total += squared
    return total
def fix_hamming(hamming, data):  #data_frame
    base_point = hamming[0]
    index = float(np.amax(hamming)/np.amax(data));
    for i in xrange(0, len(hamming)):
        hamming[i] = (hamming[i]-base_point)/index
    return hamming
def fix_new_sig_frame(hamming, data):
    # print "length hamming: ", len(hamming)
    # print "length data: ", len(data)
    for i in xrange(0, len(hamming)):
        data[i] = hamming[i]*data[i]
    start_at = int(len(data)/8)
    stop_at = len(data)-start_at
    return data[start_at:stop_at]

count = 0
array_time = []
hamming_sig = []

for i in xrange(0,2*NUMBER_FRAME-1):
    tmp = 0
    R = []
    min = 0
    start_at = int(i * FRAME_LENGTH/2)
    stop_at = int((i + 2) * FRAME_LENGTH/2)
    # tmp = sum_of_squares(data[start_at:stop_at])
    tmp = np.sum(data[start_at:stop_at]**2)
    tmp = np.sqrt(abs(tmp))
    if tmp >= 1.5:
        tmp = (i+1)*FRAME_LENGTH/(2*samplerate)
        array_time.append(tmp)
        count += 1
        new_data = data[start_at: stop_at]
        new_sig.extend(new_data)
        # R = r_total(new_data)
        # list_f0.append(f0(R))
        # if count == 1:
        #     plt.plot(R)
        #     break
        # print start_at
        # print stop_at
        if status == 0:
            plt.plot([start_at/samplerate, start_at/samplerate], [-1, 1], color="red")
            print "RED"
            status = 1
    else:
        if status == 1:
            plt.plot([stop_at/samplerate, stop_at/samplerate], [-1, 1], color="blue")
            status = 0
            print "BLUE"
test_data = new_sig[0:800]
print "length of new_data", len(new_data)
prev_point = np.argmax(test_data)
prev_point = int(prev_point/2)
list_point.append(prev_point)
print prev_point
NUMBER_FRAME_NEW = int(len(new_sig)/400)
for i in xrange(0, NUMBER_FRAME_NEW-1):
    stop_at = prev_point + 100
    test_data = new_sig[prev_point:stop_at]
    start_at = int(np.argmin(test_data)/2) + prev_point
    print "Min_point: ", start_at
    stop_at = start_at + 500
    prev_point = np.argmax(new_sig[start_at:stop_at]) 
    prev_point = int(prev_point/2) + start_at
    list_point.append(prev_point)
    print prev_point
plt.plot(timeArray, data)
print "length of new_sig", len(new_sig)
print len(list_point)
# plt.plot(new_sig)

# myInt = float(new_sig[50]/window[50])
# window = [x / 2 for x in window]
print "hamming: ", new_sig[list_point[0]]
for i in xrange(0, len(list_point)-1):
    if i == 0:
        start_at = 0
        stop_at = list_point[i+1]
        window = np.hamming(list_point[1])
        fix_hamming(window, new_sig[start_at:stop_at])
        hamming_sig.extend(fix_new_sig_frame(window, new_sig[start_at:stop_at]))

    else:
        start_at = list_point[i-1]
        stop_at = list_point[i+1]
        window = np.hamming(list_point[i+1]-list_point[i-1])
        fix_hamming(window, new_sig[start_at:stop_at])
        fix_new_sig_frame(window, new_sig[start_at:stop_at])
        hamming_sig.extend(fix_new_sig_frame(window, new_sig[start_at:stop_at]))

# plt.plot(window)
scaled = np.int16(hamming_sig/np.max(np.abs(hamming_sig)) * 32767)
write('test.wav', samplerate, scaled)
# plt.plot(hamming_sig)
# plt.plot(new_sig)
# plt.plot(list_f0, 'ro')
# plt.plot(new_sig)
# plt.ylim( (-1, 1) )
# plt.xlim( (0, 20) )

plt.show()
# s = Sound()
# s.read(filename) 
# s.play()
# write('test.wav', 44100, new_sig)
