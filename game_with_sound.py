from threading import Thread
import pygame

from shortvoiceController import q, get_current_note
from music21 import *  #or import music21?
#import fluidsynth
import time

#TODO: add code to ask which midi file
my_midi_file = 'Tourdion.mid'

###FLUIDSYNTH code
'''fs = fluidsynth.Synth()
fs.start(driver = 'coreaudio')  # use DirectSound driver

sfid = fs.sfload(r'/Users/eduardoratier/ImportedSoundFonts/GeneralUser.sf2')  # replace path as needed
#TODO: change instrument, add tracks
fs.program_select(0, sfid, 0, 0) #program_select(track, soundfontid, banknum, presetnum)'''

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
endY = 0
time_lapse = score.seconds / screenWidth  #0.07
running = True
delta_time = 0

def play_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print("Music file %s loaded!" % music_file)
    except pygame.error:
        print("File %s not found! (%s)" % (music_file, pygame.get_error()))
        return
    pygame.mixer.music.play()
    #while pygame.mixer.music.get_busy():
        # check if playback has finished
    #    clock.tick(30)
# pick a midi music file you have ...
# (if not in working folder use full path)

'''import os
def music_files():
    music_dir = "/Users/eduardoratier/Documents/GitHub/singy-bird/"
    midi_files = os.listdir(music_dir)
    for one in midi_files:
        yield music_dir + one'''


freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024    # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)
# optional volume 0 to 1.0
pygame.mixer.music.set_volume(0.8)
'''for music_file in music_files():
    try:
        play_music(music_file)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        while True:
            action = raw_input('Enter Q to Quit, Enter to Skip. ').lower()
            if action == 'q':
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.stop()
                raise SystemExit
            else:
                break'''

t = Thread(target=get_current_note)
t.daemon = True
t.start()

screen.fill((255, 255, 255)) #screen white at beginning?
#draw piano roll:
for thisNote in bass_part.getElementsByClass(["Note", "Rest"]): #or in bass.flat.notes ?

    if thisNote.isNote:    
        x, y = thisNote.offset, thisNote.pitch.frequency
        z = thisNote.seconds

        pygame.draw.rect(screen, (255, 0, 183), pygame.Rect(x * pixel_event, screenHeight - int(y), z*pixel_per_second, 15),5,2)

#pygame.event.clear()

pygame.mixer.music.load(my_midi_file)
pygame.event.wait()
pygame.mixer.music.play()

###Now the game starts:
while running:
    clock.tick(60) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False
    
    #time=pygame.time.get_ticks()
    # en 1 s tengo que avanzar pixel_per_second
    # como en 1 s hay 60 ticks, tengo que avanzar pixel_per_second/60 cada tick        
 
    #TODO: change time_lapse for correct tempo
    dt += pixel_per_second / 60
        #playing the midi file note by note
        #n = bass_part.flat.getElementAtOrBefore(dt)
        #fs.noteon(0, n.pitch.midi, 120)

            # our user should be singing if there's a note on the queue
    if not q.empty():
        startY = endY

        b = q.get()
        endY = screenHeight - int(b['NotePitch'])

        #TODO: change the way the singing note is draw
        pygame.draw.circle(screen, (0, 128, 255),(dt, screenHeight - int(b['NotePitch'])), 5,2)  
        #pygame.draw.rect(screen,(0, 128, 255) , pygame.Rect(dt,screenHeight - int(b['NotePitch']) , 5, 3))
        #pygame.draw.line(screen, (0, 0, 255), (dt-time_lapse,startY ), (dt, endY), 3)                                             
        #time.sleep(n.quarterLength*60.0/mytempo)
        #time.sleep(n.quarterLength*4.0)
        #fs.noteoff(0, n.pitch.midi)
        
    pygame.display.flip()                        
        #stoping the game if we reach the right end of the screen
    if dt > screenWidth:
        running = False

    #delta_time=pygame.time.get_ticks()-time     






