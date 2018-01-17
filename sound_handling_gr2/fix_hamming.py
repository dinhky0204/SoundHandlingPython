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

def sound_analy(filename, FRAME_DURATION):
    samplerate, data = wavfile.read(filename)
    fix_data = []
    data = data / (2. ** 15)
    FRAME_LENGTH = FRAME_DURATION * samplerate
    NUMBER_FRAME = int(len(data) / FRAME_LENGTH)
    TIME = (float)(len(data) / samplerate)
    print "Frame length: ", FRAME_LENGTH
    print "Number frame: ", NUMBER_FRAME
    print "Length: ", len(data)
    print "Samplerate: ", samplerate
    if type(data[0]) is np.ndarray:
        for i in xrange(0, (len(data)-1)):
            fix_data.append(data[i][0])
        return (FRAME_LENGTH, NUMBER_FRAME, fix_data, samplerate, FRAME_LENGTH)
    else:    
        return (FRAME_LENGTH, NUMBER_FRAME, data, samplerate, FRAME_LENGTH)

def sum_of_squares(xs):
    sum_of_squares = 0
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
def fix_hamming(hamming, data):  #data_frame
    base_point = hamming[0]
    start_at = int(len(data)*1/10)
    data_len = int(len(data)*9/10)
    index = float((np.amax(hamming)-base_point)/np.amax(data[start_at:data_len]))
    for i in xrange(0, len(hamming)):
        hamming[i] = float((hamming[i]-base_point)/index)
    return hamming
def fix_new_sig_frame(hamming, data):
    # print "length hamming: ", len(hamming)
    # print "length data: ", len(data)
    for i in xrange(0, len(hamming)):
        data[i] = hamming[i]*data[i]
    start_at = int(len(data)/8)
    stop_at = len(data)-start_at
    return data[start_at:stop_at]
def extend_hamming_sig(hamming_sig, extend_data):
    extend_space = int(len(extend_data)/5)
    start_point = len(hamming_sig) - extend_space
    for i in xrange(0, extend_space):
        hamming_sig[i + start_point] += extend_data[i]
    end_point = len(extend_data) -1
    hamming_sig.extend(extend_data[extend_space : end_point])
    # print len(hamming_sig)
    return hamming_sig