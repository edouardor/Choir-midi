from threading import Thread
import pygame

from shortvoiceController import q, get_current_note
from music21 import *  #or import music21?
import fluidsynth
import time

#TODO: add code to ask which midi file
my_midi_file = 'Tourdion.mid'

###MUSIC 21 code
score = converter.parse(my_midi_file)
#TODO: find tempo in midi-file (can be many: if more than one change code)
mytempo = 320.0
mm1 = tempo.MetronomeMark(number=mytempo) 
score.insert(0, mm1)
#TODO: ask for which part will be used - and after, code to ear (or mute) the different parts
bass_part = score.parts[3]

###PYGAME code
pygame.init()
screenWidth, screenHeight = 1024, 512 #try with different set-ups
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
#TODO: find a way to sinchronize pixel movement with tempo
pixel_per_second = screenWidth / score.seconds
pixel_event = screenWidth / score.quarterLength
dt = 0
time_lapse = 0.1
running = True

t = Thread(target=get_current_note)
t.daemon = True
t.start()

screen.fill((255, 255, 255)) #screen white at beginning?
#draw piano roll:
for thisNote in bass_part.getElementsByClass(["Note", "Rest"]): #or in bass.flat.notes ?

    if thisNote.isNote:    
        x, y = thisNote.offset, thisNote.pitch.frequency
        z = thisNote.seconds

        pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(x * pixel_event, screenHeight - int(y), z*pixel_per_second, 15))

pygame.event.clear()
pygame.event.wait()

###Now the game starts:






