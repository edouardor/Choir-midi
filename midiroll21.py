from music21 import *  #luego no hara falta , ya que importaremos shortvoiceController
#import matplotlib
my_midi_file = 'Tourdion.mid'

score = converter.parse(my_midi_file)
screenWidth = 1024

#for part in score.parts:
#    print(part)
  #vamos digo yo
#score.show('text')
timeSignature = score.getTimeSignatures()[0]
print("Music time signature: {0}/{1}".format(timeSignature.beatCount, timeSignature.denominator))

mm1 = tempo.MetronomeMark(number=320) #porque lo digo yo - habrá que pedirlo en algún sitio
score.insert(0, mm1)
pixel_per_second = screenWidth / score.seconds
pixel_event = screenWidth / score.quarterLength
bass_part = score.parts[3]
#print(score.quarterLength, type(score.quarterLength))
#print(score.seconds)
'''for thisNote in bass_part.getElementsByClass(["Note", "Rest"]):
        #print(thisNote, thisNote.offset)
    if thisNote.isNote:
        x,y = thisNote.offset,thisNote.pitch.frequency
        z = thisNote.seconds
        print('x in pixels: {0}, duration in pixels: {1}'.format(x * pixel_event,z * pixel_per_second))

            #pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(x * pixel_per_second, screenHeight - int(y), z*pixel_per_second, 2))
actual_note = ""
actual_note_beginning = 0
for thisNote in bass_part.getElementsByClass(["Note", "Rest"]):
    print(thisNote, thisNote.offset)
    if thisNote != actual_note:
        actual_note_end = thisNote.offset
    

    
    if thisNote.isNote:
        #print(thisNote.offset,thisNote.pitch.frequency, thisNote.seconds)
        beginning_note = thisNote.offset
        actual_note = thisNote

import matplotlib.pyplot as plt
import matplotlib.lines as mlines

def extract_notes(midi_part):
    parent_element = []
    ret = []
    for nt in midi_part.flat.notes:        
        if isinstance(nt, note.Note):
            ret.append(max(0.0, nt.pitch.ps))
            parent_element.append(nt)
        elif isinstance(nt, chord.Chord):
            for pitch in nt.pitches:
                ret.append(max(0.0, pitch.ps))
                parent_element.append(nt)
    
    return ret, parent_element

def print_parts_countour(midi):
    fig = plt.figure(figsize=(12, 5))
    ax = fig.add_subplot(1, 1, 1)
    minPitch = pitch.Pitch('C10').ps
    maxPitch = 0
    xMax = 0
    
    # Drawing notes.
    for i in range(len(midi.parts)):
        top = midi.parts[i].flat.notes                  
        y, parent_element = extract_notes(top)
        if (len(y) < 1): continue
            
        x = [n.offset for n in parent_element]
        ax.scatter(x, y, alpha=0.6, s=7)
        
        aux = min(y)
        if (aux < minPitch): minPitch = aux
            
        aux = max(y)
        if (aux > maxPitch): maxPitch = aux
            
        aux = max(x)
        if (aux > xMax): xMax = aux
    
    for i in range(1, 10):
        linePitch = pitch.Pitch('C{0}'.format(i)).ps
        if (linePitch > minPitch and linePitch < maxPitch):
            ax.add_line(mlines.Line2D([0, xMax], [linePitch, linePitch], color='red', alpha=0.1))            

    plt.ylabel("Note index (each octave has 12 notes)")
    plt.xlabel("Number of quarter notes (beats)")
    plt.title('Voices motion approximation, each color is a different instrument, red lines show each octave')
    plt.show()

# Focusing only on 6 first measures to make it easier to understand.
print_parts_countour(score.measures(0, 6))'''

        
