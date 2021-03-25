from ElementTree_pretty import prettify

import getJson
import tabLogger
import musicXML
import midiConverter
import StepAndOctave
import musicXML_ClassParser

#TODO add logger

def getAllKeys(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield (key, value)
            yield from getAllKeys(value)
        if type(value) is list:
            for x in value:
                if type(x) is dict:
                    yield (key, x)
                    yield from getAllKeys(x)
                else:
                    yield (key, x)      
        else:
            yield (key, value)

def midiNumberToNote(stringList): #assumes A = 440
    noteList = []
    for x in stringList:
        noteList.append( midiConverter.midiDic[x] )
    return noteList

def main():

    songSterrJson = getJson.getSongSterrJson()
    songData = musicXML.SongData(songSterrJson["meta"]["title"],songSterrJson["meta"]["artist"])

    tab_logger = tabLogger.setup_logger('tab_logger', 'debug_logfile.log')
    tab_logger.info("\n"+songSterrJson["meta"]["title"])

    #determine instrument TODO make better
    instrument = songSterrJson["data"]["part"]["instrument"]
    if(instrument == "bass" or instrument == "Electric Bass (finger)" or instrument == "Electric Bass (pick)" or instrument == "Fretless Bass"):
        instrument = musicXML.Bass( midiNumberToNote( songSterrJson["data"]["part"]["tuning"] ), songSterrJson["data"]["part"]["capo"])
    elif(instrument == "guitar" or instrument == "Distortion Guitar" or instrument == "Acoustic Guitar (steel)" or instrument == "Overdriven Guitar" or instrument
     == "Electric Guitar (clean)"):
        instrument = musicXML.Guitar( midiNumberToNote(songSterrJson["data"]["part"]["tuning"] ), songSterrJson["data"]["part"]["capo"])
    else:
        print("New instrument found:",instrument)
        return

    #get all measures
    for x in range( len( songSterrJson["data"]["part"]["measures"] ) ) :
        songData.jsonMeasures.append( songSterrJson["data"]["part"]["measures"][x] )

    #start to process the data and turn it into a py class
    for x in songData.jsonMeasures:
        tab_logger.info(x)
        tmpMeasure = musicXML.Measure(x["index"])

        if [*x].count("signature"):
            tmpMeasure.timeSig = x["signature"]
        if [*x].count("marker"):
            tmpMeasure.rehearsal_mark = x["marker"]
        if [*x].count("repeatStart"):
            tmpMeasure.repeatStart = True
        if [*x].count("repeat"):
            tmpMeasure.repeatEnd = True
            tmpMeasure.repeatTimes = x["repeat"]
        if [*x].count("alternateEnding"):
            tmpMeasure.alternateEnding = True
       
        for key, value in getAllKeys(x):
            tmpMeasure.dictKeys.append(key)
            #print(key,value)

            #if beats process everything for chords and length
            if key == 'beats':
                #type and duration
                chordClass = musicXML.Chord( value['type'], value['duration'] )
                if [*value].count("dotted") > 0:
                    chordClass.dotted = 1
                if [*value].count("palmMute") > 0:
                    chordClass.palmMute = True
                #notes decode from string fret to note
                for note in value['notes']:
                    noteClass = musicXML.Note()
                    if [*note].count("string") > 0:
                        noteClass.string = note['string']
                        noteClass.fret = note['fret']
                    if [*note].count("hp") > 0:
                        noteClass.hp = True
                    if [*note].count("dead") > 0:
                        noteClass.muted = True
                    if [*note].count("tie") > 0:
                        noteClass.tie = True
                    if [*note].count("staccato") > 0:
                        noteClass.staccato = True
                    stepAndOctaveDict = StepAndOctave.getNoteNameAndNumber(note,instrument.tuning,instrument.capo)
                    noteClass.step = stepAndOctaveDict["step"]
                    noteClass.octave = stepAndOctaveDict["octave"]
                    chordClass.notes.append(noteClass)
                tmpMeasure.chords.append(chordClass)
                if [*value].count("tempo") :#tempo
                    chordClass.tempo = value["tempo"]

        songData.classMeasures.append(tmpMeasure)
    
    musicXML_Class = musicXML.musicXML(instrument,songData)

    #for measure in musicXML_Class.songData.classMeasures: #log this add other variables, keep track of new tags
    #    for note in measure.notes:
    #        print(note.notes)
    #    print("")

    #preprocess musicXML class for tie, slur TODO
    musicXML.preProcessMusicXML(musicXML_Class)

    #parse class to musescore xml
    xml_music = musicXML_ClassParser.parseClass(musicXML_Class)

    filename = musicXML_Class.songData.songName + ".musicxml"
    file = open( ("Tab to Sheet\\sheet music xml" + "\\" + filename), "w")
    file.write( prettify(xml_music) )
    file.close

    return 0

if __name__ == "__main__":
    main()