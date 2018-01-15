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

class handling:
    def sound_analy(self, filename, FRAME_DURATION):
        samplerate, data = wavfile.read(filename)
        data = data / (2. ** 15)
        FRAME_LENGTH = FRAME_DURATION * samplerate
        NUMBER_FRAME = int(len(data) / FRAME_LENGTH)
        TIME = (float)(len(data) / samplerate);
        print "Frame length: ", FRAME_LENGTH
        print "Number frame: ", NUMBER_FRAME
        print "Length: ", len(data)
        print "Samplerate: ", samplerate
        
        return (FRAME_LENGTH, NUMBER_FRAME, data, samplerate)

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
    def fix_hamming(self, hamming, data):  #data_frame
        base_point = hamming[0]
        start_at = int(len(data)*1/5)
        data_len = int(len(data)*4/5)
        index = float((np.amax(hamming)-base_point)/np.amax(data[start_at:data_len]))
        for i in xrange(0, len(hamming)):
            hamming[i] = float((hamming[i]-base_point)/index)
        return hamming
    def fix_new_sig_frame(self, hamming, data):
        # print "length hamming: ", len(hamming)
        # print "length data: ", len(data)
        for i in xrange(0, len(hamming)):
            data[i] = hamming[i]*data[i]
        start_at = int(len(data)/8)
        stop_at = len(data)-start_at
        return data[start_at:stop_at]

class mclass:
    def __init__(self,  window):
        self.window = window
        self.filename = tkFileDialog.askopenfilename(initialdir="/home/dinhky/PycharmProjects/", title="Select sound file",
                                                filetypes=(("wav files", "*.wav"), ("all files", "*.*")))
        self.new_sig = []
        self.hamming_sig = []
        self.samplerate = 0
        if not self.filename:
            print "Exit!"
            self.window.destroy()
        else:
            self.box = Entry(window)
            lbl3 = Label(window, text="Energy", width=6, font=("Helvetica", 14))
            lbl3.pack(side=TOP, anchor=N, pady=5)
            self.fig = Figure(figsize=(6, 6))
            self.button = Button(window, text="CHECK", bg = "#497e1e", fg="white", command=self.plot)
            self.psola_hadling = Button(window, text="TD-PSOLA", bg = "#497e1e", fg="white", command=self.mul_hamming)
            self.play_sound = Button(window, text="PLAY", bg = "#497e1e", fg="white", command=self.play_sound)
            self.quit_btn = Button(window, text="QUIT", bg= "red", fg="black", command=self.window.quit)
            self.box.pack()
            self.quit_btn.pack(side="bottom")
            self.button.pack()
            self.psola_hadling.pack()
            self.play_sound.pack()
    def min_array(self, data):
        tmp = 1
        data = data.ravel()
        for i in data:
            if i < tmp:
                tmp = i
        return tmp  
    def play_sound(self):
        print "play"
        spf = wave.open("test.wav",'r')
        mixer.init(spf.getframerate())
        try:
            d1 = mixer.Sound("test.wav")
        except:
            prompt = "Error: Sound file not found"
        d1.play()

    def max_of_frame(self, new_sig):
        list_point = []
        test_data = new_sig[0:800]
        prev_point = np.argmax(test_data)
        prev_point = int(prev_point/2)
        list_point.append(prev_point)
        # print prev_point
        NUMBER_FRAME_NEW = int(len(new_sig)/400)
        for i in xrange(0, NUMBER_FRAME_NEW-1):
            stop_at = prev_point + 100
            test_data = new_sig[prev_point:stop_at]
            start_at = int(np.argmin(test_data)/2) + prev_point
            # print "Min_point: ", start_at
            stop_at = start_at + 500
            prev_point = np.argmax(new_sig[start_at:stop_at]) 
            prev_point = int(prev_point/2) + start_at
            list_point.append(prev_point)
            # print prev_point
        return list_point
    def mul_hamming(self):
        hd = handling()
        self.hamming_sig = []
        list_point = self.max_of_frame(self.new_sig)
        for i in xrange(0, len(list_point)-1):
            if i == 0:
                start_at = 0
                stop_at = list_point[i+1]
                window = np.hamming(list_point[1])
                window = hd.fix_hamming(window, self.new_sig[start_at:stop_at])
                self.hamming_sig.extend(hd.fix_new_sig_frame(window, self.new_sig[start_at:stop_at]))
            else:
                start_at = list_point[i-1]
                stop_at = list_point[i+1]
                # print "start: ", list_point[i-1]
                # print "stop: ", list_point[i+1]
                if list_point[i-1] != list_point[i+1]:
                    window = np.hamming(list_point[i+1]-list_point[i-1])
                    hd.fix_hamming(window, self.new_sig[start_at:stop_at])
                    hd.fix_new_sig_frame(window, self.new_sig[start_at:stop_at])
                    self.hamming_sig.extend(hd.fix_new_sig_frame(window, self.new_sig[start_at:stop_at]))
        # print self.hamming_sig[0:200]
        scaled = np.int16(self.hamming_sig/np.max(np.abs(self.hamming_sig)) * 32767)
        write('test.wav', self.samplerate, scaled)
        plt.plot(self.hamming_sig)
        plt.show()
    def plot_new_sig(self):
        plt.plot(self.new_sig)
        plt.show()
    def plot (self):
        self.new_sig = []
        self.hamming_sig = []
        print "Nang luong ====>", self.box.get()
        hd = handling()
        FRAME_DURATION = 0.04
        status = 1
        new_data = np.array([])
        return_value_of_handling = hd.sound_analy(self.filename, FRAME_DURATION)
        FRAME_LENGTH = return_value_of_handling[0]
        NUMBER_FRAME = return_value_of_handling[1]
        data = return_value_of_handling[2]
        self.samplerate = return_value_of_handling[3]
        print len(data)
        a = self.fig.add_subplot(111)
        a.clear()
        timeArray = np.arange(0, len(data), 1)
        timeArray = timeArray / float(self.samplerate)
        a.plot(timeArray, data, color="blue")
        print "data: ", data.shape
        for i in xrange(0, (2 * NUMBER_FRAME - 1)):
            start_at = int(i * FRAME_LENGTH / 2)
            stop_at = int((i + 2) * FRAME_LENGTH / 2)
            tmp = np.sum(data[start_at:stop_at]**2)
            tmp = np.sqrt(abs(tmp))
            # test = hd.min_of_square(data[start_at:stop_at])
            # tmp = 0.046
            # print tmp
            if tmp >= float(self.box.get()):
                self.new_sig.extend(data[start_at:stop_at])
                if status == 1:
                    # print (i) * FRAME_LENGTH / (2 * samplerate), (i) * FRAME_LENGTH / (2 * samplerate)
                    a.plot([(i) * FRAME_LENGTH / (2 * self.samplerate), (i) * FRAME_LENGTH / (2 * self.samplerate)], [-1, 1],
                             color="red")
                    status = 0
                # elif np.min(data[start_at:stop_at]) == 0:
                #     a.plot([(i) * FRAME_LENGTH / (2 * samplerate), (i) * FRAME_LENGTH / (2 * samplerate)], [-1, 1],
                #              color="yellow")
                #     status = 0
            elif tmp < float(self.box.get()):
                if status == 0:
                    # print (i) * FRAME_LENGTH / (2 * samplerate), (i) * FRAME_LENGTH / (2 * samplerate) 
                    a.plot([(i+1) * FRAME_LENGTH / (2 * self.samplerate), (i+1) * FRAME_LENGTH / (2 * self.samplerate)], [-1, 1],
                             color="blue")
                    status = 1
                # elif np.min(data[start_at:stop_at]) == 0:
                #     a.plot([(i) * FRAME_LENGTH / (2 * samplerate), (i) * FRAME_LENGTH / (2 * samplerate)], [-1, 1],
                #              color="yellow")
                #     status = 0
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
