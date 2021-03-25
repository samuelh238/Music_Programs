import re

#given a dict that is form string: x fret: y
#and tuning list
#return Note name "step" and octave number "octave"
stepList = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B" ] 
def getNoteNameAndNumber(tabForm, tuningList,capo):

    stepAndOctave = {
        "step" : "rest",
        "octave" : 0
        }

    if [*tabForm].count("rest") > 0:
        return stepAndOctave
    
    stringPitch = tuningList[ int(tabForm["string"]) ]
    
    #regex to split into step and octave number
    match = re.match(r"([a-z]+)([0-9]+)", stringPitch, re.I)
    if match:
        items = match.groups()
    else:
        print("Error could not parse step and octave")
    octave = int(items[1])
    stringPitch = items[0]
    stepIndex = stepList.index(stringPitch)
    stepIndex = (stepIndex + tabForm["fret"]) + capo
    while(stepIndex >= 12): #if we go over the list just adjust the octave
        stepIndex = stepIndex - 12
        octave = octave + 1
        
    stepAndOctave["step"] = stepList[stepIndex]
    stepAndOctave["octave"] = octave

    return stepAndOctave
