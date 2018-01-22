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

def handling(filename, energy):
    FRAME_DURATION = 0.04
    list_f0 = []
    new_sig = []
    fix_data = []
    R = []
    samplerate, data = wavfile.read(filename)
    data = data / (2. ** 15)
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
    for i in xrange(0,2*NUMBER_FRAME-1):
        tmp = 0
        min = 0
        start_at = int(i * FRAME_LENGTH/2)
        stop_at = int((i + 2) * FRAME_LENGTH/2)
        tmp = sum_of_squares(data[start_at:stop_at])
        # tmp = np.sum(data[start_at:stop_at]**2)
        tmp = np.sqrt(abs(tmp))
        if tmp >= energy:
            tmp = (i+1)*FRAME_LENGTH/(2*samplerate)
            new_data = data[start_at: stop_at]
            new_sig.extend(new_data)
            R = r_total(FRAME_LENGTH, new_data, K)
            list_f0.append(f0(R, samplerate))
            if status == 0: #co tieng noi
                status = 1
        else:
            if status == 1: #diem khong co tieng noi
                status = 0
                status = 0
    return list_f0

def r_item(frame_length, k, arr):
    total = 0
    for n in xrange(0, (frame_length-k-1)):
        total = total + arr[n]*arr[n+k]
    return total

def r_total(frame_length, new_data, k_limit):
    new_r = []
    for k in xrange(0, k_limit):
        new_r.append(r_item(frame_length, k, new_data))
    return new_r
def max_of_arr(arr):
    result = 0
    flag = [-2,-2]
    for i in arr:
        if i > flag:
            result = i
            flag = i
    return result

def f0(r, samplerate):
    star_point = int(samplerate/450)
    end_point = int(samplerate/80)
    point = np.argmax(r[star_point:end_point])+star_point
    return samplerate/point

def sum_of_squares(xs):
    total = 0
    for i in xs:
        squared = i * i
        total += squared
    return total
count = 0

