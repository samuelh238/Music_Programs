from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from ElementTree_pretty import prettify
import datetime

import midiConverter
import musicXML

divisor = 32 #hardcoded to 32nd note division

def BaseXML(musicXML_Class):
    museScoreXml_root = Element("score-partwise")
    museScoreXml_root.set("version", "3.1")

    work = SubElement(museScoreXml_root, "work")
    workTitle = SubElement(work, "work-title")
    workTitle.text = musicXML_Class.songData.songName
    identification = SubElement(museScoreXml_root, "identification")
    creator = SubElement(identification, "creator")
    creator.set("type", "composer") #composer by default
    creator.text = musicXML_Class.songData.artist
    encoding = SubElement(identification, "encoding")
    software = SubElement(encoding , "software")
    software.text = "MuseScore 3.5.2" #hard coded will get version number later
    encodingDate = SubElement(encoding , "encoding-date")
    encodingDate.text = str(datetime.date.today())
    supports = SubElement(encoding , "supports")
    supports.set("element","accidental")
    supports.set("type","yes")
    supports = SubElement(encoding , "supports")
    supports.set("element","beam")
    supports.set("type","yes")
    supports = SubElement(encoding , "supports")
    supports.set("element","print")
    supports.set("attribute","new-page")
    supports.set("type","yes")
    supports.set("value","yes")
    
    #defaults
    defaults = SubElement(museScoreXml_root, "defaults")
    scaling = SubElement(defaults,"scaling")
    millimeters = SubElement(scaling,"millimeters")
    millimeters.text = "7.05556"
    tenths = SubElement(scaling,"tenths")
    tenths.text = "40"
    page_layout = SubElement(defaults,"page-layout")
    page_height = SubElement(page_layout,"page-height")
    page_height.text = "1584"
    page_width = SubElement(page_layout,"page-width")
    page_width.text = "1224"
    page_margins = SubElement(page_layout,"page-margins")   
    page_margins.set("type","even")
    left_margin = SubElement(page_margins,"left-margin")       
    left_margin.text = "56.6929"
    right_margin = SubElement(page_margins,"right-margin")      
    right_margin.text = "56.6929"
    top_margin = SubElement(page_margins,"top-margin")      
    top_margin.text = "56.6929"
    bottom_margin = SubElement(page_margins,"bottom-margin")       
    bottom_margin.text = "113.386"

    page_margins = SubElement(page_layout,"page-margins")   
    page_margins.set("type","odd")
    left_margin = SubElement(page_margins,"left-margin")       
    left_margin.text = "56.6929"
    right_margin = SubElement(page_margins,"right-margin")      
    right_margin.text = "56.6929"
    top_margin = SubElement(page_margins,"top-margin")      
    top_margin.text = "56.6929"
    bottom_margin = SubElement(page_margins,"bottom-margin")       
    bottom_margin.text = "113.386"

    word_font = SubElement(defaults,"word-font")
    word_font.set("font-family","FreeSerif")
    word_font.set("font-size","10")
    #lyric-font
 
    #credit #can be multiple
    credit = SubElement(museScoreXml_root, "credit")
    credit.set("page","1")
    credit_type = SubElement(credit,"credit-type")
    credit_type.text = "title"
    creditWords = SubElement(credit, "credit-words") #this one has a lot of settings
    creditWords.set("default-x","612")
    creditWords.set("default-y","1527.31")
    creditWords.set("justify","center")
    creditWords.set("valign","top")
    creditWords.set("font-size","24")
    creditWords.text = musicXML_Class.songData.songName

    credit = SubElement(museScoreXml_root, "credit")
    credit.set("page","1")
    credit_type = SubElement(credit,"credit-type")
    credit_type.text = "composer"
    creditWords = SubElement(credit, "credit-words") #this one has a lot of settings
    creditWords.set("default-x","1167.31")
    creditWords.set("default-y","1427.31")
    creditWords.set("justify","right")
    creditWords.set("valign","bottom")
    creditWords.set("font-size","12")
    creditWords.text = musicXML_Class.songData.artist

    credit = SubElement(museScoreXml_root, "credit")
    credit.set("page","1")
    creditWords = SubElement(credit, "credit-words") #this one has a lot of settings
    creditWords.set("default-x","56.6929")
    creditWords.set("default-y","1527.31")
    creditWords.set("justify","left")
    creditWords.set("valign","top")
    creditWords.set("font-size","18")
    creditWords.text = musicXML_Class.instrument.name

    #parts #hard code one insturment per part TODO
    partList = SubElement(museScoreXml_root, "part-list")
    scorePart = SubElement(partList, "score-part")
    scorePart.set("id", ("P" + str((1)) ) )
    partName = SubElement(scorePart, "part-name")
    partName.text = musicXML_Class.instrument.name
    scoreInstrument = SubElement(scorePart ,"score-instrument")
    partID = "P" + str((1)) + "-I" + "1"
    scoreInstrument.set("id",partID)
    instrumentName = SubElement(scoreInstrument,"instrument-name")
    instrumentName.text = musicXML_Class.instrument.name
    midiDevice = SubElement(scorePart ,"midi-device")
    midiDevice.set("id",partID)
    midiDevice.set("port","1")
    midiInstrument = SubElement(scorePart ,"midi-instrument")
    midiInstrument.set("id", partID)
    midiChannel = SubElement(midiInstrument, "midi-channel")
    midiChannel.text = str((1))
    midiProgram = SubElement(midiInstrument, "midi-program")
    midiProgram.text = str( midiConverter.getInstrumentNumber(musicXML_Class.instrument.name) )
    volume = SubElement(midiInstrument, "volume")
    volume.text = "78.7402"
    pan = SubElement(midiInstrument, "pan")
    pan.text = "0"

    return museScoreXml_root

def baseMeasureXML(museScoreXml_root,musicXML_Class):

    #part
    part = SubElement(museScoreXml_root, "part")
    part.set("id", ("P" + str(1) ) ) #TODO add part id to function

    #starting measure tags
    measure = SubElement(part, "measure")
    #measure.set("number", "1")
    print_muse = SubElement(measure, "print")
    staffLayout = SubElement(print_muse, "staff-layout")
    staffLayout.set("number","1")
    staffDistance = SubElement(staffLayout, "staff-distance")
    staffDistance.text = "100.00"
    #only display name if more than one part
    partNameDisplay = SubElement(print_muse, "part-name-display")
    displayText = SubElement(partNameDisplay, "display-text")
    displayText.text = musicXML_Class.instrument.name
    #accidental-text>flat</accidental-text>
    #displayText = SubElement(partNameDisplay, "display-text")
    #displayText.text = "1"
    
    attributes = SubElement(measure, "attributes")
    divisions = SubElement(attributes, "divisions")
    divisions.text = str(divisor) 
    key = SubElement(attributes, "key")
    fifths = SubElement(key, "fifths")
    fifths.text = "0" #determines key negative for flats lets leave it in C major and just add accidentals TODO find a way to get the key sig later
    mode = SubElement(key, "mode")
    mode.text = "none" #TODO determine mode/key

    
def getoctaveOffset(midiNum):
    if midiNum  >= 33 and midiNum <= 40:
        octaveOffset = 1
    else:
        octaveOffset = 0
    return octaveOffset

def parseClass(musicXML_Class):

    museScoreXml_root = BaseXML(musicXML_Class)
    baseMeasureXML(museScoreXml_root,musicXML_Class)
    midiNum = int(midiConverter.getInstrumentNumber(musicXML_Class.instrument.name))
    octaveOffset = 0

    measureXML = museScoreXml_root.find("part").find("measure")
    for num, measure in enumerate( musicXML_Class.songData.classMeasures ):
        if num == 0:
            measureXML = museScoreXml_root.find("part").find("measure")
        else:
            measureXML = SubElement(museScoreXml_root.find("part"), "measure")
        #measure tags
        measureXML.set("number", str(num+1))

        if measure.timeSig != None:
            time = SubElement( measureXML.find("attributes"), "time" ) #this is broken TODO
            beats = SubElement(time,"beats")
            beats.text = str( measure.timeSig[0] )
            beat_type = SubElement(time,"beat-type")
            beat_type.text = str( measure.timeSig[1] )

        if measure.rehearsal_mark != None:
            direction = SubElement( measureXML, "direction" )
            direction.set("placement","above")
            direction_type = SubElement(direction,"direction-type")
            rehearsal = SubElement(direction_type,"rehearsal")
            rehearsal.set("font-size","12")
            rehearsal.set("font-weight","bold")
            rehearsal.text = measure.rehearsal_mark['text']
        
        if measure.repeatStart != None:
            barline = SubElement(measureXML,"barline")
            barline.set("location","left")
            bar_style = SubElement(barline,"bar-style")
            bar_style.text = "heavy-light"
            repeat = SubElement(barline,"repeat")
            repeat.set("direction","forward")
            repeat.set("winged","none")

        if measure.repeatEnd != None:
            barline = SubElement(measureXML,"barline")
            barline.set("location","right")
            bar_style = SubElement(barline,"bar-style")
            bar_style.text = "light-heavy"
            ending = SubElement(barline,"ending")
            ending.set("number","1") #TODO add ending number likme this http://usermanuals.musicxml.com/MusicXML/MusicXML.htm#EL-MusicXML-repeat.htm#kanchor503
            ending.set("type","stop")
            repeat = SubElement(barline,"repeat")
            repeat.set("direction","backward")
            repeat.set("winged","none")

        
        if num == 0:
            #clefs http://usermanuals.musicxml.com/MusicXML/MusicXML.htm#EL-MusicXML-clef.htm#kanchor391
            if( int(midiConverter.getInstrumentNumber(musicXML_Class.instrument.name)) >= 33 and int(midiConverter.getInstrumentNumber(musicXML_Class.instrument.name)) <= 40 ):
                clef = SubElement(measureXML.find("attributes"), "clef")
                sign = SubElement(clef, "sign")
                sign.text = "F"
                line = SubElement(clef, "line")
                line.text = "4" 
            else:
                clef = SubElement(measureXML.find("attributes"), "clef")
                sign = SubElement(clef, "sign")
                sign.text = "G"
                line = SubElement(clef, "line")
                line.text = "2" 

            transpose = SubElement(measureXML.find("attributes"), "transpose")
            diatonic = SubElement(transpose, "diatonic")
            diatonic.text = "0"
            chromatic = SubElement(transpose, "chromatic")
            chromatic.text = "0"
            octaveOffset = getoctaveOffset( midiNum )
            octaveChange = SubElement(transpose, "octave-change") # -1 if bass
            octaveChange.text = "-"+str(octaveOffset) 

        for chord in measure.chords:

            #check some variable from the note class that can be set before looping through each note
            if chord.tempo != None:

                sound = SubElement(measureXML,"sound")
                sound.set( "tempo",str( chord.tempo['bpm'] ) )

            for noteNum,note in enumerate( chord.notes ):
                #note tags
                noteXML = SubElement(measureXML, "note")
                if len( chord.notes ) > 1 and noteNum > 0:
                    SubElement(noteXML,"chord")
                
                if note.step == "rest":
                    SubElement(noteXML,"rest")
                else:
                    pitch = SubElement(noteXML,"pitch")
                    step = SubElement(pitch,"step")
                    step.text = note.step[0]
                    alter = SubElement(pitch, "alter")
                    alter.text = "0"
                    octave = SubElement(pitch,"octave")
                    octave.text = str( note.octave + octaveOffset )
            
                duration = SubElement(noteXML,"duration")
                durationNum = midiConverter.getDuration( chord.duration[0],chord.duration[1] )
                duration.text = str( divisor *  durationNum )
                if note.tie_start:
                    tie = SubElement(noteXML,"tie")
                    tie.set("type","start")
                if note.tie_end:
                    tie = SubElement(noteXML,"tie")
                    tie.set("type","stop") 
                voice = SubElement(noteXML, "voice")
                voice.text = "1" #number of voices for the part not sure when parts will have more than one TODO
                noteType = SubElement(noteXML,"type")
                noteType.text = str( midiConverter.getType( durationNum ) )
                
                if chord.dotted > 0:
                    SubElement(noteXML,"dot")

                if len(note.step) > 1 and note.step != "rest":
                    accidental = SubElement(noteXML, "accidental")
                    if note.step[1] == "b":
                        accidental.text = "flat"
                        alter.text = "-1"
                    elif note.step[1] == "#":
                        accidental.text = "sharp"
                        alter.text = "1"
                    else:
                        accidental.text = "natural"
                        alter.text = "0"

                #add muted xml tags TODO

                notations = SubElement(noteXML,"notations")
                articulations = SubElement(notations,"articulations")
                if note.staccato:
                    staccato = SubElement(articulations,"staccato")
                    staccato.set("placement","below")
                if note.hp_start:
                    slur = SubElement(notations,"slur")
                    slur.set("number","1")
                    slur.set("type","start")
                if note.hp_end:
                    slur = SubElement(notations,"slur")
                    slur.set("number","1")
                    slur.set("type","stop")  
                if note.tie_start:
                    tied = SubElement(notations,"tied")
                    tied.set("type","start")
                if note.tie_end:
                    tied = SubElement(notations,"tied")
                    tied.set("type","stop")
                if chord.palmMute:
                    play = SubElement(noteXML,"play")
                    mute = SubElement(play,"mute")
                    mute.text = "palm" 
            
    #print( prettify(museScoreXml_root) )
    return museScoreXml_root