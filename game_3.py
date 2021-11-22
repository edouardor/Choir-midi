from threading import Thread
import pygame
import math

from shortvoiceController import q, get_current_note
from music21 import *  #or import music21?
import time

#TODO: add code to ask which midi file
#my_midi_file = 'Tourdion.mid'
my_midi_file = '/Users/eduardoratier/Downloads/CAT00058 BAJO.mid'
short_name_file = my_midi_file[my_midi_file.rfind('/')+1:]
#measuredStream = my_midi_file.makeNotation()

###MUSIC 21 code
score = converter.parse(my_midi_file)
#TODO: find tempo in midi-file (can be many: if more than one change code)
#mytempo = 320.0
#mm1 = tempo.MetronomeMark(number=mytempo) 
mm1 = score.flat.getElementsByClass('MetronomeMark')[0]
score.insert(0, mm1)
#TODO: ask for which part will be used - and after, code to ear (or mute) the different parts
bass_part = score.parts[0]
#bass_part_midi = bass_part.write('midi')
#my_midi_file = bass_part_midi

#print(len(my_midi_file.tracks[0].events))
#score.show('midi') not working here - but works on notebook - seems to be a vscode problem
###PYGAME code
pygame.init()
screenWidth, screenHeight = 1000, 512 #try with different set-ups
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption(short_name_file)
#screen.set_alpha(0) 
clock = pygame.time.Clock()
#TODO: find a way to sinchronize pixel movement with tempo
pixel_per_second = screenWidth / score.seconds
pixel_event = screenWidth / score.quarterLength

color_default = (9,180,237) #(138,2,0)
color_palette = [color_default,(138,0,133),(0,97,138),(9,180,237)]  #(138,0,133)
altura_notas = 16
running = True

freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024    # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)
# optional volume 0 to 1.0
pygame.mixer.music.set_volume(0.8)
all_displaid_notes_list = pygame.sprite.Group()


class note_display(pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y, longitud, color = color_default, espesor = altura_notas):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y - espesor/2     #el rectangulo se dibuja en el medio de la frecuencia
        self.longitud = longitud       
        self.color = color
        self.espesor = espesor
        self.percent = 0       
        #rect(surface, color, rect, width=0, border_radius=0)
        pygame.draw.rect(screen,self.color,pygame.Rect(self.pos_x,self.pos_y,self.longitud,self.espesor),2,4)
        
    def change_color(self, percent=0):
        self.percent += percent
        if percent>=0.04:
            self.color = color_palette[3]
        else:
            self.color = color_palette[3]  #int(percent*10)

    def dibuja(self):
        pygame.draw.rect(screen,self.color,pygame.Rect(self.pos_x,self.pos_y,self.longitud,self.espesor),0,4)

    def marco(self):
        pygame.draw.rect(screen,self.color,pygame.Rect(self.pos_x,self.pos_y,self.longitud,self.espesor),2,4)    


    @property
    def rect(self):  
        return pygame.Rect(self.pos_x, self.pos_y, self.longitud, self.espesor)        

class sing_display(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, radio = 5):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y  
        self.radio = radio

        pygame.draw.circle(screen, (0, 128, 255),(pos_x, pos_y), radio,5)

    @property
    def rect(self):  
        return pygame.Rect(self.pos_x, self.pos_y, 1, 2*math.pi*self.radio)                   


t = Thread(target=get_current_note)
t.daemon = True
t.start()
dt = 0.0
screen.fill((255, 255, 255)) #screen white at beginning?
#draw piano roll:
'''for thisNote in bass_part.getElementsByClass(["Note", "Rest"]): #or in bass.flat.notes ?

    if thisNote.isNote:    
        x, y = thisNote.offset, thisNote.pitch.frequency
        z = thisNote.seconds

        pygame.draw.rect(screen, (255, 0, 183), pygame.Rect(x * pixel_event, screenHeight - int(y), z*pixel_per_second, 15),5,2)'''

'''for thisNote in bass_part.flat.notes:
    #x = thisNote.offset * pixel_event
    #x = thisNote.midiTickStart * screenWidth * 4 /(score.seconds * 1000)
    x = thisNote.offset * pixel_per_second * 60 / mm1.number
    y = screenHeight - int(thisNote.pitch.frequency)
    longitud = thisNote.seconds * pixel_per_second

    note_sprite = note_display(x ,y, longitud)
    all_displaid_notes_list.add(note_sprite)

for mm in score.flat.getElementsByClass(['Note','MetronomeMark']):
    if type(mm).__name__ == 'MetronomeMark':
        actual_mm = mm.number
    else:
        x = mm.offset * pixel_per_second * 60 / actual_mm
        y = screenHeight - int(mm.pitch.frequency)
        longitud = mm.seconds * pixel_per_second
        note_sprite = note_display(x ,y, longitud)
        all_displaid_notes_list.add(note_sprite)'''
            
elapsed_time = 0
for n in score.flat.getElementsByClass(['Note','Rest']):
    if n.isNote:
        x = elapsed_time * pixel_per_second
        y = screenHeight - int(n.pitch.frequency)
        longitud = n.seconds * pixel_per_second
        note_sprite = note_display(x ,y, longitud)
        all_displaid_notes_list.add(note_sprite)

    elapsed_time += n.seconds    

pygame.display.flip() 
#pygame.event.clear()

pygame.mixer.music.load(my_midi_file)
pygame.event.wait()
pygame.mixer.music.play()

###Now the game starts:
while running:
    clock.tick(100) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            while True: #Infinite loop that will be broken when the user press the space bar again
                pygame.mixer.music.pause()
                event = pygame.event.wait()
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pygame.mixer.music.unpause()
                    break #Exit infinite loop        

    music_position = pygame.mixer.music.get_pos()
    dt = music_position *screenWidth /(score.seconds * 1000)        
    #vertical_line_future = note_display(dt+3,0,10,(238, 240, 223),screenHeight)
    #vertical_line_present = note_display(dt-2,0,10,(255, 255, 255),screenHeight)
    surface1 = screen.convert_alpha()
    surface1.fill([0,0,0,0])
    pygame.draw.line(surface1, (9,180,237, 10), (dt+8, 0), (dt+8, screenHeight), 1) #238, 240, 223, 10
    pygame.draw.line(surface1, (255, 255, 255, 70), (dt, 0), (dt, screenHeight), 1)
    screen.blit(surface1, (0,0))
    #pygame.draw.line(surface4, (0, 0, 0, 32), (0, 600), (800, 0), 5)
    #vertical_line_past = note_display(dt-100,0,10,(255, 255, 255,0),screenHeight)
    future_note = [sprite for sprite in all_displaid_notes_list if sprite.rect.left <= dt <= sprite.rect.right]
    if future_note:
        future_note[0].marco()
    '''actual_note = [sprite for sprite in all_displaid_notes_list if sprite.rect.left <= dt <= sprite.rect.right]
    if actual_note:
        actual_note[0].dibuja()'''
            # our user should be singing if there's a note on the queue
    if not q.empty():
        b = q.get()
        x = dt
        y = screenHeight - int(b['NotePitch'])
        sing_sprite = sing_display(x,y,4)
        #right_note = pygame.sprite.spritecollide(sing_sprite, all_displaid_notes_list, False)
        right_note = pygame.sprite.spritecollide(sing_sprite, future_note, False)
        if right_note:
            #length_note = right_note[0].rect.right - right_note[0].rect.left
            scanned = pixel_per_second / 60
            right_note[0].change_color(scanned)
            right_note[0].dibuja()


        #TODO: change the way the singing note is draw
        #pygame.draw.circle(screen, (0, 128, 255),(dt, screenHeight - int(b['NotePitch'])), 5,2)
          
        
    pygame.display.flip()                        
        #stoping the game if we reach the right end of the screen
    if dt > screenWidth:
        running = False

quit()        

    






