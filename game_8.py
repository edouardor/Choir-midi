from threading import Thread
import pygame
#from pygame.locals import *
import math

from shortvoiceController import q, get_current_note
from music21 import *  #or import music21?
import time
import datetime

import copy

#TODO: add code to ask which midi file
#my_midi_file = 'Tourdion.mid'
my_midi_file = '/Users/eduardoratier/Downloads/CAT00058 BAJO.mid' #CAT00058 CAT00514
short_name_file = my_midi_file[my_midi_file.rfind('/')+1:]
#measuredStream = my_midi_file.makeNotation()

###MUSIC 21 code
score = converter.parse(my_midi_file)
#whole_score = whole_score.flat
score_to_play = copy.deepcopy(score)
#for mm in score.flat.getElementsByClass('MetronomeMark'):
#    score.insert(mm.offset,mm)
#TODO: ask for which part will be used - and after, code to ear (or mute) the different parts
#score = whole_score.measures(1,44)

#as an example:
start = 8
end = 13


short_score = score.measures(start,end)

#bass_part = score.parts[0]
'''def last_mm(score, beginning):
    
    for index,mm in enumerate(score.flat.getElementsByClass('MetronomeMark')):
        if mm.offset> beginning:
            return score.flat.getElementsByClass('MetronomeMark')[index - 1]
        else:
            return score.flat.getElementsByClass('MetronomeMark')[-1]'''
#bass_part_midi = bass_part.write('midi')
#my_midi_file = bass_part_midi

score = score.makeMeasures()
start_measure = score.getElementsByClass('Measure')[start -1]
mm_start = [mm for mm in score.flat.getElementsByClass('MetronomeMark') if mm.offset <= start_measure.offset][-1]

short_score.parts[0].insertAndShift(0,mm_start)
short_score_midi = short_score.write('midi')
my_midi_file = short_score_midi
score = short_score
score.show('text')
#print(len(my_midi_file.tracks[0].events))
#score.show('midi') not working here - but works on notebook - seems to be a vscode problem
###PYGAME code
pygame.init()
screenWidth, screenHeight = 1000, 512 #try with different set-ups
screen = pygame.display.set_mode((screenWidth, screenHeight))

#screen.set_alpha(0) 
clock = pygame.time.Clock()

pixel_per_second = screenWidth / score.flat.seconds
#pixel_event = screenWidth / score.quarterLength
color_default = (9,180,237)
altura_notas = 16
PXS = max(40,pixel_per_second) 
stageWidth = int(PXS * score.flat.seconds) 
running = True

freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024    # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)
# optional volume 0 to 1.0
pygame.mixer.music.set_volume(0.8)
all_displaid_notes_list = []

'''PLAYER_IMG = Surface((5, 5))
PLAYER_IMG.fill(Color('dodgerblue1'))

TRIANGLE_IMG = pg.Surface((50, 50), pg.SRCALPHA)
pg.draw.polygon(TRIANGLE_IMG, (240, 120, 0), [(0, 50), (25, 0), (50, 50)])

class Player(sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect(center=pos)
        # The sprite will be added to this layer in the LayeredUpdates group.
        self._layer = self.rect.bottom

class Triangle(pg.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = TRIANGLE_IMG
        self.rect = self.image.get_rect(center=pos)
        # The sprite will be added to this layer in the LayeredUpdates group.
        self._layer = self.rect.bottom '''       


class Colored_rect(pygame.Rect):
   
    def __init__(self,x,y,w,h,color,collided=0): 
        super().__init__(x,y,w,h)
        self.color = color
        self.collided = collided                         

class sing_display(pygame.sprite.Sprite):

    def __init__(self, x, y, radio = 5):
        super().__init__()
        self.x = x
        self.y = y
  
        self.radio = radio
        pygame.draw.circle(screen, (0, 128, 255),(x % screenWidth, y), radio,5)  

        pygame.draw.circle(stage, (190, 220, 250),(x, y), 3,3)

    @property
    def rect(self):  
        return pygame.Rect(self.x, self.y, 1, 2*math.pi*self.radio)                   


t = Thread(target=get_current_note)
t.daemon = True
t.start()
dt = 0.0
#screen.fill((255, 255, 255)) #screen white at beginning?
#draw piano roll stage:

stage = pygame.Surface((stageWidth, screenHeight)) #for now the stage has the same height than the screen
stage.fill((255,255,255))
elapsed_time = 0
for n in score.flat.getElementsByClass(['Note','Rest']):
    if n.isNote:
        x = elapsed_time * PXS #pixel_per_second
        y = screenHeight - int(n.pitch.frequency) - altura_notas / 2
        longitud = n.seconds * PXS #pixel_per_second
        note_rect = Colored_rect(x ,y, longitud, altura_notas,color_default)
        
        pygame.draw.rect(stage, color_default, note_rect, 2,4)
        #screen.blit(surfaces_list[page_index],(0,0))
        #pygame.display.flip()
        #clock.tick(100)
        all_displaid_notes_list.append(note_rect)

    elapsed_time += n.seconds

    #draw measures bar:
elapsed_time = 0
#score.semiFlat.show('text')
#for me in short_score.semiFlat.getElementsByClass('Measure'):
#    print(me.seconds)

for me in score.semiFlat.getElementsByClass('Measure'):  #se podria hacer todo con semiFlat
    #if math.isnan(me.seconds):
    #    me.seconds = 0.0
    x = elapsed_time * PXS
    pygame.draw.line(stage, (9,180,237, 10), (x, 0), (x, screenHeight), 1)
    elapsed_time += me.seconds 


                    
#pygame.event.clear()

pygame.mixer.music.load(my_midi_file)
pygame.event.wait()
pygame.mixer.music.play()


'''sp = midi.realtime.StreamPlayer(score_to_play)
sp.play()
t0 = datetime.datetime.now()'''

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
                #sp.stop()
                event = pygame.event.wait()
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    #pygame.mixer.music.unpause()
                    break #Exit infinite loop        
    #t1 = datetime.datetime.now()
    #real_elapsed_time = t1 - t0
    #alt_music_position = real_elapsed_time.seconds + real_elapsed_time.microseconds / 1000000
    music_position = pygame.mixer.music.get_pos() / 1000  # in seconds
    #print(alt_music_position,music_position)
    #dt = music_position *screenWidth /(score.seconds * 1000) 
    x = music_position * PXS
    stage_page = int(x // screenWidth) 
    pygame.display.set_caption(short_name_file + " page: " + str(stage_page))
    screen.blit(stage,(-stage_page * screenWidth,0))
    rel_x = x % screenWidth


    '''surface1 = pygame.Surface((screenWidth, screenHeight)) #screen.convert_alpha()
    surface1.fill((255,255,255))
    pygame.draw.line(surface1, (9,180,237, 10), (dt+8, 0), (dt+8, 20), 1) #238, 240, 223, 10
    pygame.draw.line(surface1, (255, 255, 255, 255), (dt, 0), (dt, 20), 1)
    screen.blit(surface1, (0,0))'''
    #pygame.display.flip()  
    pygame.draw.line(screen, (9,180,237, 10), (rel_x, 0), (rel_x, screenHeight), 1)                      



    # our user should be singing if there's a note on the queue
    if not q.empty():
        b = q.get()
         
        y = screenHeight - int(b['NotePitch']) 
        sing_sprite = sing_display(x,y,4)

    for note_rect in all_displaid_notes_list:
        color = note_rect.color
        if note_rect.collidepoint(x, y):
            note_rect.collided += 1
            green = color[1]-note_rect.collided//(10)
            if green <0: green = 0
            color = (0,green,255)
            note_rect.color = color
            #print(green)
            pygame.draw.rect(stage, color, note_rect, 0,4)
        else:
            pygame.draw.rect(stage, color_default, note_rect, 2,4)     
        
    pygame.display.update()                        
    #stoping the game if we reach the right end of the screen
    #if dt > screenWidth:
    #    running = False

quit()        

    






