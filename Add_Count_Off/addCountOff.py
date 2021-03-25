import Music_Programs.BPM_Detector.bpm_detection.bpm_detection as bpm_tool
import Music_Programs.Audio_Grapher.audioGrapher as audiograph
import Music_Programs.Audacity.pipeclient as pipeclient

import librosa
from pyAudioAnalysis import ShortTermFeatures, MidTermFeatures

from scipy.io.wavfile import read
import numpy as np
import tkinter as tk
from tkinter import filedialog
import math, sys, psutil, subprocess

def addCountOff():
    
    #load audio file as WAV
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename()
    Fs, data, wavfilename = audiograph.readAudioFileAsWAV(filename,normalized=True) #returns data and saves as file.wav

    if np.shape(data)[1] > 0:
        data = data[:,0] #only need one channel
    
    #determine first attack might be a better way to do this with SilenceFinder: command in audacity
    attackTime = 0
    i = 0
    for x in data:
        if( abs(x) > 1000):
            #print("index:",i,"value:", x)
            #print("attackTime: ",attackTime)
            attackTime = (float(i/Fs))
            break
        i = i + 1

    print("Finding BPM")
    #add bpm database to look up and skip calculations?

    #determine start bpm and TODO time sig works for 4/4
    breakFile = True
    if (not breakFile):
        bpm, correl = bpm_tool.bpm_detector(data, Fs)
        bpm = np.round(bpm)[0]
    else: #this is faster but seems to be slightly off
        #cut to small chunks if too large
        nsamps = len(data)
        window_size = 5 #window size in sec
        window_samps = int(window_size * Fs)
        samps_ndx = 0  # First sample in window_ndx
        max_window_ndx = math.floor(nsamps / window_samps)
        bpms = np.zeros(max_window_ndx)

        # Iterate through all windows
        for window_ndx in range(0, max_window_ndx):

            # Get a new set of samples
            # print(n,":",len(bpms),":",max_window_ndx_int,":",Fs,":",nsamps,":",samps_ndx)
            chunk = data[samps_ndx : samps_ndx + window_samps]
            if not ((len(chunk) % window_samps) == 0):
                raise AssertionError(str(len(chunk)))

            bpm, correl_temp = bpm_tool.bpm_detector(chunk, Fs)
            if bpm is None:
                continue
            bpms[window_ndx] = bpm
            correl = correl_temp

            # Iterate at the end of the loop
            samps_ndx = samps_ndx + window_samps

        bpms = bpms[bpms != 0] #remove zeros before calculating median
        #print("bpm_tool bpms:",bpms)
        bpm = round(np.median(bpms)) #Find better way to average TODO

    print("Tempo using bpm_tool:", bpm)
    #print("correl::",correl)

    y, sr = librosa.load(wavfilename,sr=None)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    #print("beats:",beats)
    print("Tempo using librosa.beat.beat_track:", round(tempo) )

    onset_env = librosa.onset.onset_strength(y, sr=sr)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr) #more accurate but still slightly off
    print("Tempo using librosa.beat.tempo:", np.round(tempo)[0] )

    
    #shortFeat, featNames = ShortTermFeatures.feature_extraction(y,sr,window_samps,window_samps)
    #print(shortFeat)
    #bpm, ratio = MidTermFeatures.beat_extraction(shortFeat,window_size)
    #print("pyAudioAnalysis bpm:",bpm)
    #print("confidence ratio:",ratio)
    

    #add more bpm_detector algoritms and compare against TODO

    ''' #TODO fix starting audacity in windows or delele this sections
    #open adaucity if audacity is not open
    openPipe = True
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() == "audacity.exe":
                openPipe = False
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                openPipe = openPipe
    if openPipe:
        cmd_args = []
        cmd_args.append("\"C:\\Program Files (x86)\\Audacity\\audacity.exe\"")
        cmd_args.append('start ')
        cmd_args.append('/wait ')
        
        print(cmd_args)
        child = subprocess.Popen(cmd_args)
    '''

    #open pipe
    try:
        client = pipeclient.PipeClient()
    except:
        print("Is Audacity open?")
        sys.exit(-1)

    #add song
    wavfilename = wavfilename.replace("\\","\\\\")
    cmdString =  "Import2: filename=" + wavfilename
    client.write(cmdString)

    #cut to first attack
    cmdString = "SelectTime:End=" + str(0) + " RelativeTo=" + "SelectionStart" " Start=" + str(attackTime)
    client.write(cmdString)
    cmdString = "Delete:"
    client.write(cmdString)

    #Have to select something or the RhythmTrack will delete everything ~_~
    cmdString = "SelectTime:End=" + str(0) + " RelativeTo=" + "SelectionStart" " Start=" + str(.001)
    client.write(cmdString)

    #find if it is a pickup measure TODO
        #calculate and cut count off, if so add offset para

    #generate count off
    cmdString = "RhythmTrack:bars=" + str(1) + " click-track-dur=0 click-type=Metronome high=84 low=80 offset=0 swing=0 tempo=" + str(bpm) + " timesig=4"
    client.write(cmdString)

    #Add option to add click track TODO
    #generate count off
    #cmdString = "RhythmTrack:bars=" + str(?) + " click-track-dur=0 click-type=Metronome high=84 low=80 offset=0 swing=0 tempo=" + str(bpm) + " timesig=4"
    #client.write(cmdString)

    #Have to select before export
    cmdString = "SelectAll:"
    client.write(cmdString)

    #export and save as wav
    filename = filename.replace("\\","\\\\")
    filename = filename.replace(".","_count_off.")
    cmdString = "Export2: filename=\"" + filename + "\"" + " NumChannels=" + str(2)
    client.write(cmdString)

    #clear track
    cmdString = "RemoveTracks:"
    client.write(cmdString)

if __name__ == "__main__":
    addCountOff()