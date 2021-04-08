from PyQt5 import QtWidgets, QtGui, QtCore, uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import math
import itertools
import numpy as np
import pyaudio
#import modulated_oscillator as m_o
import oscillators
import components
#import envelopes

BUFFER_SIZE = 256
SAMPLE_RATE = 44100
NOTE_AMP = 1

def get_sin_oscillator(freq, amp=1, phase=0, sample_rate=44100):
    phase = (phase / 360) * 2 * math.pi
    increment = (2 * math.pi * freq)/ sample_rate
    return (math.sin(phase + v) * amp for v in itertools.count(start=0, step=increment))

def get_samples(notes_dict, num_samples=BUFFER_SIZE):
    return [sum([int(next(osc) * 32767) \
            for _, osc in notes_dict.items()]) \
            for _ in range(num_samples)]

def osc_function(freq, amp, sample_rate, attack_duration, decay_duration, sustain_level, \
                 release_duration=0.3):
    return iter(
        components.Chain(
            oscillators.SineOscillator(freq=freq, 
                    amp=amp, sample_rate=sample_rate),
            components.modifiers.ModulatedVolume(
                components.envelopes.ADSREnvelope(attack_duration=(float(attack_duration)) / 10000, decay_duration=(float(decay_duration)) / 10000, sustain_level=(float(sustain_level)) / 10,
                 release_duration=(float(release_duration)) / 10000, sample_rate=sample_rate)
            )
        )
    )

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('C:\\Users\\Sam\\AppData\\Local\\Programs\\Python\\Python38\\Music_Programs\\Music_Programs\\ADSR_Grapher\\embeddedGraphTest.ui', self) #TODO change to relative path

        #freq line edit val
        self.onlyDouble = QtGui.QDoubleValidator()
        self.freqLineEdit.setValidator(self.onlyDouble)

        self.notes_dict = {}

        self.stream = pyaudio.PyAudio().open(
            rate=SAMPLE_RATE,
            channels=1,
            format=pyaudio.paInt16,
            output=True,
            frames_per_buffer=BUFFER_SIZE
        )

        #init graph
        self.sample_rate = 2048
        self.osc = get_sin_oscillator(freq=1, sample_rate=512)
        self.samples = [next(self.osc) for i in range(self.sample_rate*4)]

        self.attack_length = self.sample_rate
        self.decay_length = self.sample_rate
        self.sustain_level = .4
        self.sustain_length = self.sample_rate
        self.release_length = self.sample_rate
        self.attack = np.linspace(0, 1, self.attack_length)
        self.decay = np.linspace(1, self.sustain_level, self.decay_length)
        self.sustain = np.full((self.sustain_length, ), self.sustain_level)
        self.release = np.linspace(self.sustain_level, 0, self.release_length)

        self.adsr = np.concatenate( (self.attack, self.decay,self.sustain,self.release) )

        self.graphWidget_ADSR.setTitle("ADSR Curve")

        self.pen = pg.mkPen(color=(255, 0, 0))
        self.attack_start = 0
        self.attack_end = len(self.attack)
        self.attack_line = self.graphWidget_ADSR.plot(range(self.attack_start,self.attack_end), self.attack, pen=self.pen)
        self.attack_line_main = self.graphWidget_ADSR_SIG.plot(range(self.attack_start,self.attack_end), self.attack, pen=self.pen)

        self.pen = pg.mkPen(color=(0, 255, 255))
        self.decay_start = len(self.attack)
        self.decay_end = len(self.attack)+len(self.decay)
        self.decay_line = self.graphWidget_ADSR.plot(range(self.decay_start,self.decay_end), self.decay, pen=self.pen)
        self.decay_line_main = self.graphWidget_ADSR_SIG.plot(range(self.decay_start,self.decay_end), self.decay, pen=self.pen)

        self.pen = pg.mkPen(color=(255, 125, 0))
        self.sus_start = len(self.attack)+len(self.decay)
        self.sus_end = len(self.attack)+len(self.decay)+len(self.sustain)
        self.sus_line = self.graphWidget_ADSR.plot(range(self.sus_start,self.sus_end), self.sustain, pen=self.pen)
        self.sus_line_main = self.graphWidget_ADSR_SIG.plot(range(self.sus_start,self.sus_end), self.sustain, pen=self.pen)

        self.pen = pg.mkPen(color=(0, 255, 125))
        self.rel_start = len(self.attack)+len(self.decay)+len(self.sustain)
        self.rel_end = len(self.attack)+len(self.decay)+len(self.sustain)+len(self.release)
        self.rel_line = self.graphWidget_ADSR.plot(range(self.rel_start,self.rel_end), self.release, pen=self.pen)
        self.rel_line_main = self.graphWidget_ADSR_SIG.plot(range(self.rel_start,self.rel_end), self.release, pen=self.pen)


        self.graphWidget_SIG.setTitle("Input Signal Curve")
        self.SIG_line = self.graphWidget_SIG.plot(range(0,self.sample_rate*4), self.samples)

        self.graphWidget_ADSR_SIG.setTitle("ADSR * Input Signal Curve")
        self.ADSR_SIG_line = self.graphWidget_ADSR_SIG.plot(range(0,len(self.adsr)), self.adsr*self.samples)

        #button to play sound
        self.b1.clicked.connect(self.play_sound)
        self.b2.clicked.connect(self.play_ADSRsound)

        #timer for updating graphs
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def play_sound(self):
        self.notes_dict[0] = get_sin_oscillator(freq=float(self.freqLineEdit.text()), amp=1) #type generator
        samples = get_samples(self.notes_dict)
        samples = np.int16(samples).tobytes()
        self.stream.write(samples)

    def play_ADSRsound(self):

        self.notes_dict[0] = osc_function( freq=float( self.freqLineEdit.text() ), amp=1, sample_rate = SAMPLE_RATE,attack_duration=self.attack_length, decay_duration=self.decay_length, sustain_level=self.sustain_level, release_duration=self.release_length ) 
        samples = get_samples(self.notes_dict)
        samples = np.int16(samples).tobytes()
        self.stream.write(samples)

    def update_plot_data(self):
        self.sample_rate = self.sample_rate #+ 50

        self.attack_length = self.dial_attack.value()
        self.decay_length = self.dial_decay.value()
        self.sustain_level = self.dial_sustain.value()
        self.sustain_length = self.sample_rate #keeping this a constant for now tied to sample rate of input signal
        self.release_length = self.dial_release.value()
        self.attack = np.linspace( 0, 1 , self.attack_length ) 
        self.decay = np.linspace( 1, self.dial_sustain.value()/10, self.decay_length )
        self.sustain = np.full(( self.sustain_length, ), self.dial_sustain.value()/10 )
        self.release = np.linspace( self.dial_sustain.value()/10, 0, self.release_length )

        self.adsr = np.concatenate( (self.attack, self.decay,self.sustain,self.release) )

        osc = get_sin_oscillator(freq=float(self.freqLineEdit.text()) , sample_rate=2048)
        self.samples = [next(osc) for i in range(len(self.adsr))]

        self.pen = pg.mkPen(color=(255, 0, 0))
        self.attack_start = 0
        self.attack_end = len(self.attack)
        self.attack_line.setData(range(self.attack_start,self.attack_end), self.attack, pen=self.pen)
        self.attack_line_main.setData( range(self.attack_start,self.attack_end), self.attack, pen=self.pen )

        self.pen = pg.mkPen(color=(0, 255, 255))
        self.decay_start = len(self.attack)
        self.decay_end = len(self.attack)+len(self.decay)
        self.decay_line.setData(range(self.decay_start,self.decay_end), self.decay, pen=self.pen)
        self.decay_line_main.setData( range(self.decay_start,self.decay_end), self.decay, pen=self.pen )

        self.pen = pg.mkPen(color=(255, 125, 0))
        self.sus_start = len(self.attack)+len(self.decay)
        self.sus_end = len(self.attack)+len(self.decay)+len(self.sustain)
        self.sus_line.setData(range(self.sus_start,self.sus_end), self.sustain, pen=self.pen)
        self.sus_line_main.setData( range(self.sus_start,self.sus_end), self.sustain, pen=self.pen )

        self.pen = pg.mkPen(color=(0, 255, 125))
        self.rel_start = len(self.attack)+len(self.decay)+len(self.sustain)
        self.rel_end = len(self.attack)+len(self.decay)+len(self.sustain)+len(self.release)
        self.rel_line.setData(range(self.rel_start,self.rel_end), self.release, pen=self.pen)
        self.rel_line_main.setData( range(self.rel_start,self.rel_end), self.release, pen=self.pen )


        self.graphWidget_SIG.setTitle("Input Signal Curve")

        self.graphWidget_ADSR_SIG.setTitle("ADSR * Input Signal Curve")

        self.SIG_line.setData(range(0,len(self.adsr)), self.samples)
        self.ADSR_SIG_line.setData(range(0,len(self.adsr)), self.adsr*self.samples)
        #self.ADSR_over_SIG.setData(range(0,len(self.adsr)), self.adsr)

        #print("att value: ",float(self.sustain_level) / 10 )
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()