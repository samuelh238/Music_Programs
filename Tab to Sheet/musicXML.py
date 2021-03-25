class Note():
    """Note class holds all tags and data from note tag in songsterr json"""
    def __init__(self):
        self.step = "Rest"
        self.octave = ""
        self.string = ""
        self.fret = ""
        self.tie = False
        self.tie_start = False
        self.tie_end = False
        self.hp = False
        self.hp_start = False
        self.hp_end = False
        self.muted = False
        self.staccato = False

class Chord(): #another tag is voices but we will just assume there is only ever one voice, more than one voice and we would need another class on top of notes
    """Chord class holds all tags and data from beat tag in songsterr json"""
    def __init__(self,noteType, duration):
        self.noteType = noteType
        self.duration = duration
        self.notes = [] #more than one note equals chord being played, holds Note class
        self.tempo = None #{'type': 4, 'bpm': 120.1}
        self.dotted = 0
        self.palmMute = False #needs a stop and start tag TODO
        #Will add more as I learn to process more tags

class Measure():
    """Measure class holds all tags and data from Measure tag in songsterr json"""
    def __init__(self,number):
        self.number = number
        self.dictKeys = []
        self.chords = [] #holds all note objects in the measure
        self.timeSig = None
        self.rehearsal_mark = None #marker dict in json 'marker': {'text': 'Chorus', 'width': 41}
        self.repeatStart = None
        self.repeatEnd = None
        self.alternateEnding = None
        self.repeatTimes = 1
        #Will add more as I learn to process more tags
        

class SongData():

    def __init__(self,songName,artist):
        self.songName = songName
        self.artist = artist
        self.classMeasures = [] #hold measure classes, each measure class has an array of notes
        self.jsonMeasures = [] #holds raw json from songsterr


class String_Instrument():
    """subclass for all string instruments """

    def __init__(self,tuning,capo):
        self.tuning = tuning
        self.numStrings = len(self.tuning)
        self.capo = capo

class Bass(String_Instrument):

    def __init__(self,tuning,capo):
        super(Bass, self).__init__(tuning,capo)
        self.name = "Bass Guitar"

class Guitar(String_Instrument):

    def __init__(self,tuning,capo):
        super(Guitar, self).__init__(tuning,capo)
        self.name = "Guitar"



        
        

class musicXML():

    def __init__(self,instrument,songData):
        self.instrument = instrument
        self.songData = songData
        
def preProcessMusicXML(musicXMLClass):

    #Flags to see if the prev note has the value
    prevHp = False
    prevChord = None

    for measure in musicXMLClass.songData.classMeasures:
        for chord in measure.chords:
            for note in chord.notes:

                #hp (slur) add start tag if first one, if last one set stop tag
                if note.hp:
                    if not prevHp:
                        note.hp_start = True
                    prevHp = True
                else:
                    if prevHp:
                        note.hp_end = True
                    prevHp = False

                #tie, modify current note step value and add tie start tag to prev note
                if note.tie: #songsterr only marks end of ties and the notes are not always right
                    note.tie_end = True
                    #print("prevChord",prevChord.notes[0].string)
                    for prevNote in prevChord.notes:
                        if prevNote.string == note.string:
                            prevNote.tie_start = True #get prev note
                            note.string = prevNote.string
                            note.fret = prevNote.fret
                            note.step = prevNote.step
                            note.octave = prevNote.octave

                    #get prev chord and find the note with the matching string, fret may not be right
                    #prevNote.tie_start = True #get prev note
                    #note.string = prevNote.string
                    #note.fret = prevNote.fret


            prevChord = chord

    return 0