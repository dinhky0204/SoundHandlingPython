import fix_hamming as handling
import f0_handling
import fix_f0 
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
        self.test_point = 0
        self.energy = 0
        self.number_frame = 0
        self.f0 = 110
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
            self.show_f0 = Button(window, text="SHOW F0", bg = "#497e1e", fg="white", command=self.show_f0)
            self.show_new_sig = Button(window, text="Dau huyen", bg = "#497e1e", fg="white", command=self.thanh_huyen)
            self.box.pack()
            self.quit_btn.pack(side="bottom")
            self.button.pack()
            self.psola_hadling.pack()
            self.play_sound.pack()
            self.show_new_sig.pack()
            self.show_f0.pack()
    def min_array(self, data):
        tmp = 1
        data = data.ravel()
        for i in data:
            if i < tmp:
                tmp = i
        return tmp  
    def show_f0(self):
        list_f0 = f0_handling.handling(self.filename, self.energy)
        plt.plot(list_f0, 'ro')
        list_f0_fix = f0_handling.handling('test.wav', 0)
        plt.plot(list_f0_fix, 'ro')
        plt.ylim( (0, 250) )
        plt.xlim( (0, 20) )
        plt.show()
        print list_f0

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
        start_at = 0
        stop_at = 0
        prev_point = 0
        while stop_at < len(new_sig):
            start_at = prev_point + int(self.samplerate/450)
            stop_at = prev_point + int(self.samplerate/80)
            test_data = new_sig[start_at:stop_at]
            prev_point = np.argmax(test_data) + start_at
            list_point.append(prev_point)
            print prev_point
        return list_point
    def mul_hamming(self):
        self.hamming_sig = []
        list_point = self.max_of_frame(self.new_sig)
        for i in xrange(0, len(list_point)-1):
            if i == 0:
                start_at = 0
                stop_at = list_point[i+1]
                window = np.hamming(list_point[1])
                window = handling.fix_hamming(window, self.new_sig[start_at:stop_at])
                self.hamming_sig.extend(handling.fix_new_sig_frame(window, self.new_sig[start_at:stop_at]))
            else:
                start_at = list_point[i-1]
                stop_at = list_point[i+1]
                # print "start: ", list_point[i-1]
                # print "stop: ", list_point[i+1]
                if list_point[i-1] != list_point[i+1]:
                    window = np.hamming(list_point[i+1]-list_point[i-1])
                    handling.fix_hamming(window, self.new_sig[start_at:stop_at])
                    handling.fix_new_sig_frame(window, self.new_sig[start_at:stop_at])
                    self.hamming_sig = handling.extend_hamming_sig(self.hamming_sig, handling.fix_new_sig_frame(window, self.new_sig[start_at:stop_at]))
                    # self.hamming_sig.extend(handling.fix_new_sig_frame(window, self.new_sig[start_at:stop_at]))
        # print self.hamming_sig[0:200]
        scaled = np.int16(self.hamming_sig/np.max(np.abs(self.hamming_sig)) * 32767)
        write('test.wav', self.samplerate, scaled)
        plt.plot(self.hamming_sig)
        plt.show()
    def thanh_huyen(self):
        sig_thanh_huyen = []
        start_at = 0
        stop_at = 0
        space_extend = []
        number_sample_prev_frame = 0
        new_f0 = np.arange(110, 85, -0.1)
        max_points = self.max_of_frame(self.new_sig)
        space_extend = fix_f0.extend_space(new_f0, max_points, self.samplerate)
        print "len of maxpoint: ", len(max_points)
        for i in xrange(0, len(max_points)):
            if i == 0:
                start_at = 0
                stop_at = int((max_points[i+1] + max_points[i])/2)
                window = np.hamming(stop_at+1)
                window = handling.fix_hamming(window, self.new_sig[start_at:stop_at])
                sig_thanh_huyen.extend(handling.fix_new_sig_frame(window, self.new_sig[start_at:stop_at]))
                number_sample_prev_frame = len(handling.fix_new_sig_frame(window, self.new_sig[start_at:stop_at]))
                # sig_thanh_huyen.extend(handling.fix_new_sig_frame(window, self.new_sig[start_at:stop_at]))
            elif i == (len(max_points)-1):
                if max_points[i-1] != max_points[i]:
                    start_at = int((max_points[i]+max_points[i-1])/2)
                    stop_at = len(self.new_sig) - 1
                    window = np.hamming((stop_at-start_at+1))
                    window = handling.fix_hamming(window, self.new_sig[start_at:stop_at])
                    sig_thanh_huyen.extend(handling.fix_new_sig_frame(window, self.new_sig[start_at:stop_at]))
                    
            else:
                print space_extend[i]
                start_at = max_points[i-1]
                stop_at = max_points[i+1]
                if max_points[i-1] != max_points[i+1]:
                    window = np.hamming(max_points[i+1]-max_points[i-1])
                    handling.fix_hamming(window, self.new_sig[start_at:stop_at])
                    handling.fix_new_sig_frame(window, self.new_sig[start_at:stop_at])
                    number_sample_prev_frame = len(handling.fix_new_sig_frame(window, self.new_sig[start_at:stop_at]))
                    sig_thanh_huyen = fix_f0.ghep_frame_thanh_huyen(space_extend[i], sig_thanh_huyen, handling.fix_new_sig_frame(window, self.new_sig[start_at:stop_at]), number_sample_prev_frame)
                    # sig_thanh_huyen.extend(handling.fix_new_sig_frame(window, self.new_sig[start_at:stop_at]))
                
        # plt.plot(self.new_sig)
        scaled = np.int16(sig_thanh_huyen/np.max(np.abs(sig_thanh_huyen)) * 32767)
        write('test1.wav', self.samplerate, scaled)
        plt.plot(sig_thanh_huyen)
        # plt.plot(test_data)
        # plt.plot(list_f0)
        # plt.ylim(0, 150)
        plt.show()
    def plot (self):
        self.new_sig = []
        self.hamming_sig = []
        self.energy = float(self.box.get())
        print "Nang luong ====>", self.box.get()
        FRAME_DURATION = 0.04
        status = 1
        new_data = np.array([])
        return_value_of_handling = handling.sound_analy(self.filename, FRAME_DURATION)
        FRAME_LENGTH = return_value_of_handling[0]
        NUMBER_FRAME = return_value_of_handling[1]
        self.number_frame = NUMBER_FRAME
        data = return_value_of_handling[2]
        self.samplerate = return_value_of_handling[3]
        self.frame_len = return_value_of_handling[4]
        print len(data)
        a = self.fig.add_subplot(111)
        a.clear()
        timeArray = np.arange(0, len(data), 1)
        timeArray = timeArray / float(self.samplerate)
        # plt.plot(data)
        # plt.show()
        a.plot(timeArray, data, color="blue")
        for i in xrange(0, (2 * NUMBER_FRAME - 1)):
            start_at = int(i * FRAME_LENGTH / 2)
            stop_at = int((i + 2) * FRAME_LENGTH / 2)
            # tmp = np.sum(data[start_at:stop_at]**2)
            tmp = handling.sum_of_squares(data[start_at:stop_at])
            tmp = np.sqrt(abs(tmp))
            # test = hd.min_of_square(data[start_at:stop_at])
            # tmp = 0.046
            # print tmp
            if tmp >= float(self.box.get()):
                self.test_point = start_at
                stop_at = stop_at - int(FRAME_LENGTH/2)
                self.new_sig.extend(data[start_at:stop_at])
                if status == 1:
                    # print (i) * FRAME_LENGTH / (2 * samplerate), (i) * FRAME_LENGTH / (2 * samplerate)
                    a.plot([(i) * FRAME_LENGTH / (2 * self.samplerate), (i) * FRAME_LENGTH / (2 * self.samplerate)], [-1, 1],
                             color="red")
                    status = 0
            elif tmp < float(self.box.get()):
                if status == 0:
                    # print (i) * FRAME_LENGTH / (2 * samplerate), (i) * FRAME_LENGTH / (2 * samplerate) 
                    a.plot([(i+1) * FRAME_LENGTH / (2 * self.samplerate), (i+1) * FRAME_LENGTH / (2 * self.samplerate)], [-1, 1],
                             color="blue")
                    status = 1
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
