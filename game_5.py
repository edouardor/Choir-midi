from threading import Thread
import pygame
#from pygame.locals import *
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

pixel_per_second = screenWidth / score.seconds
#pixel_event = screenWidth / score.quarterLength
color_default = (9,180,237)
altura_notas = 16
PXS = 10 #minimum number of pixels for 1 second note
pages = int(PXS * score.seconds/screenWidth) +1

running = True

freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024    # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)
# optional volume 0 to 1.0
pygame.mixer.music.set_volume(0.8)
all_displaid_notes_list = []



class Colored_rect(pygame.Rect):
   
    def __init__(self,x,y,w,h,color,collided=0): 
        super().__init__(x,y,w,h)
        self.color = color
        self.collided = collided                         

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
            
elapsed_time = 0
for n in score.flat.getElementsByClass(['Note','Rest']):
    if n.isNote:
        x = elapsed_time * pixel_per_second
        y = screenHeight - int(n.pitch.frequency) - altura_notas / 2
        longitud = n.seconds * pixel_per_second
        note_rect = Colored_rect(x ,y, longitud, altura_notas,color_default)
        pygame.draw.rect(screen, color_default, note_rect, 2,4)
        all_displaid_notes_list.append(note_rect)

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

    surface1 = screen.convert_alpha()
    surface1.fill([0,0,0,0])
    pygame.draw.line(surface1, (9,180,237, 10), (dt+8, 0), (dt+8, screenHeight), 1) #238, 240, 223, 10
    pygame.draw.line(surface1, (255, 255, 255, 70), (dt, 0), (dt, screenHeight), 1)
    screen.blit(surface1, (0,0))

    # our user should be singing if there's a note on the queue
    if not q.empty():
        b = q.get()
        x = dt
        y = screenHeight - int(b['NotePitch']) 
        sing_sprite = sing_display(x,y,4)

    for note_rect in all_displaid_notes_list:
        color = note_rect.color
        if note_rect.collidepoint(x, y):
            note_rect.collided += 1
            green = color[1]-note_rect.collided//(200)
            if green <0: green = 0
            color = (0,green,255)
            note_rect.color = color
            #print(green)
            pygame.draw.rect(screen, color, note_rect, 0,4)
        else:
            pygame.draw.rect(screen, color_default, note_rect, 2,4)
          
        
    pygame.display.flip()                        
    #stoping the game if we reach the right end of the screen
    if dt > screenWidth:
        running = False

quit()        

    






