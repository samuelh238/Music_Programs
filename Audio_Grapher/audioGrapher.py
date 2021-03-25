import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile
import pydub
import tkinter as tk
from tkinter import filedialog
import audioop
import os

def readMP3(f, normalized=False):
    
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y

def writeMP3(f, sr, x, normalized=False):
    
    """numpy array to MP3"""
    channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
    if normalized:  # normalized array - each item should be a float in [-1, 1)
        y = np.int16(x * 2 ** 15)
    else:
        y = np.int16(x)
    song = pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
    song.export(f, format="mp3", bitrate="320k")

def readAudioFileAsWAV(filename, normalized=False):
    ext = filename.split(".")[-1:][0]
    if(ext == "mp3"):    
        #Fs, data, a = readMP3(filename, normalized=normalized)
        a = pydub.AudioSegment.from_mp3(filename)
        #convert to wav
        a.export("file.wav", format="wav") #wav has differnt graph than mp3
        filename = os.getcwd() + "\\file.wav"
        #read wav file
        Fs, data = scipy.io.wavfile.read("file.wav")
    elif(ext == "wav"):
        Fs, data = scipy.io.wavfile.read(filename)
    else:
        raise Exception("file ext not supported")
    return Fs, data, filename

def graphMP3_amp(filename=None):

    if(filename==None):
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename()
        
    ext = filename.split(".")[-1:][0]
    if(ext == "mp3"):    
        Fs, data = readMP3(filename,normalized=True)
    elif(ext == "wav"):
        Fs, data = scipy.io.wavfile.read(filename)
    else:
        raise Exception("file ext not supported")

    print("Sampling Frequency is: ", Fs)
    for x in range( 0, len( data[0] ) ):
        oneChannleData = data[:,x]
        plt.figure()
        plt.plot(oneChannleData)
        plt.xlabel("Sample Index")
        plt.ylabel("Amplitude")
        plt.title(filename.split("/")[-1:][0] + " channel " + str(x) )
        plt.show()

#can be slow with big files
def graphMP3_freq(filename=None):

    if(filename==None):
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename()
        
    ext = filename.split(".")[-1:][0]
    if(ext == "mp3"):    
        Fs, data = readMP3(filename,normalized=True)
    elif(ext == "wav"):
        Fs, data = scipy.io.wavfile.read(filename)
    else:
        raise Exception("file ext not supported")

    print("Sampling Frequency is: ", Fs)
    for x in range( 0, len( data[0] ) ):
        oneChannleData = data[:,x]
        plt.figure()
        plt.specgram(oneChannleData, NFFT=1024, Fs=Fs, noverlap=900)
        plt.xlabel('Time (sec)')
        plt.ylabel('Frequency (Hz)')
        plt.title(filename.split("/")[-1:][0] + " channel " + str(x) )
        plt.show()
    
if __name__ == "__main__":
    #test
    graphMP3_amp("test.wav")
    graphMP3_freq("test.wav")
