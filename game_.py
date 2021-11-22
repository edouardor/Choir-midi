from threading import Thread
import pygame
#from pygame.locals import *
import math

from shortvoiceController import q, get_current_note
from music21 import *  #or import music21?
import time
import datetime

import copy

pygame.font.init()

#TODO: add code to ask which midi file
#my_midi_file = 'Tourdion.mid'
my_midi_file = '/Users/eduardoratier/Downloads/CAT00058 CORO.mid' #CAT00058 CAT00514
short_name_file = my_midi_file[my_midi_file.rfind('/')+1:]
#measuredStream = my_midi_file.makeNotation()

###MUSIC 21 code
score = converter.parse(my_midi_file)
key = score.analyze('key')
print(key.tonic.name, key.mode)


#TODO: ask for which part will be used - and after, code to ear (or mute) the different parts


#as an example:
start = 130
start = max(1,start) #to avoid beginning by 0 or negativve number
end = 233
part = 3

Repeat = True

def shorten(score, part, start, end):
    score_part = score.parts[part]
    score_part = score_part.makeMeasures()
    short_score_part = score_part.measures(start,end)
    # to copy metronome marks if needed:
    '''if part !=0:
        short_score_part_0 = score.parts[0].measures(start,end)
        for mm in short_score_part_0.flat.getElementsByClass('MetronomeMark'):
            try:
                short_score_part.insertAndShift(mm.offset,mm)
            except:
                continue  #the metronome mark already exists'''  

    #insert first metronome mark if needed:
    score_with_measures = score.makeMeasures()
    start_measure = score_with_measures.getElementsByClass('Measure')[start -1] #first measure has an 0 index
    mm_start = [mm for mm in score_with_measures.flat.getElementsByClass('MetronomeMark') if mm.offset <= start_measure.offset][-1]
    short_score_part.insertAndShift(0,mm_start)
    return short_score_part

def draw_notes():
    all_displaid_notes_list = []
    elapsed_time = 0    
    for n in short_score_part.flat.getElementsByClass(['Note','Rest']):
        if n.isNote:
            font = pygame.font.SysFont('Comic Sans MS', 10)
            x = elapsed_time * PXS #pixel_per_second
            #y = screenHeight - int(n.pitch.midi)*ZOOM - altura_notas / 2
            y = place_note(n.pitch.midi) - altura_notas / 2
            longitud = n.seconds * PXS #pixel_per_second
            note_rect = Colored_rect(x ,y, longitud, altura_notas,color_default)           
            pygame.draw.rect(stage, color_default, note_rect, 2,4)
            text = font.render(n.pitch.spanish, 1, (9, 180, 237))
            textpos = (x+5, y)
            stage.blit(text, textpos)
            all_displaid_notes_list.append(note_rect)
        elapsed_time += n.seconds
    return all_displaid_notes_list
def draw_notes2():
    tempos = short_score_part.flat.getElementsByClass('MetronomeMark')
    signatures= short_score_part.flat.getElementsByClass('TimeSignature')
    all_displaid_notes_list = []
    elapsed_time = 0

    for note in short_score_part.flat.getElementsByClass('Note'):
        ts = [ts for ts in signatures if ts.offset <= note.offset ][-1]
        tempo = [tempo for tempo in tempos if tempo.offset <= note.offset][-1]    
        elapsed_time = 60*note.offset * (ts.numerator / ts.denominator) / tempo.number
        font = pygame.font.SysFont('Comic Sans MS', 10)
        x = elapsed_time * PXS #pixel_per_second
        y = place_note(note.pitch.midi) - altura_notas / 2
        longitud = note.seconds * PXS #pixel_per_second
        note_rect = Colored_rect(x ,y, longitud, altura_notas,color_default)           
        pygame.draw.rect(stage, color_default, note_rect, 2,4)
        text = font.render(note.pitch.spanish, 1, (9, 180, 237))
        textpos = (x+5, y)
        stage.blit(text, textpos)
        all_displaid_notes_list.append(note_rect)
    return all_displaid_notes_list

def draw_notes3():
    all_displaid_notes_list = []
    for note in short_score_part.flat.getElementsByClass('Note'):
        elapsed_time = o2t(note.offset)
        font = pygame.font.SysFont('Comic Sans MS', 10)
        x = elapsed_time * PXS #pixel_per_second
        y = place_note(note.pitch.midi) - altura_notas / 2
        longitud = note.seconds * PXS #pixel_per_second
        note_rect = Colored_rect(x ,y, longitud, altura_notas,color_default)           
        pygame.draw.rect(stage, color_default, note_rect, 2,4)
        text = font.render(note.pitch.spanish, 1, (9, 180, 237))
        textpos = (x+5, y)
        stage.blit(text, textpos)
        all_displaid_notes_list.append(note_rect)
    return all_displaid_notes_list

def draw_measures():

    tempos = short_score_part.flat.getElementsByClass('MetronomeMark')
    signatures= short_score_part.flat.getElementsByClass('TimeSignature')
    measures = short_score_part.getElementsByClass('Measure')
    elapsed_time = 0

    for me in measures:
        x = elapsed_time * PXS
        ts = [ts for ts in signatures if ts.offset <= me.offset ][-1]
        tempo = [tempo for tempo in tempos if tempo.offset <= me.offset][-1]
        elapsed_time += 240 * (ts.numerator / ts.denominator) / tempo.number 
        pygame.draw.line(stage, (9,180,237, 10), (x, 0), (x, screenHeight), 1)     
        font = pygame.font.SysFont('Comic Sans MS', 10)
        text = font.render(str(me.number), 1, (9, 180, 237))
        textpos = (x+5, stageHeight-20)
        stage.blit(text,(textpos))

    '''elapsed_time = 0
    xant = 0
    for me in short_score_part.semiFlat.sorted.getElementsByClass('Measure'):  #se podria hacer todo con semiFlat
        if type(tempo.MetronomeMark.number) != int:
            tempo.MetronomeMark = short_score_part.semiFlat.getElementsByClass('MetronomeMark')[0]
        x = elapsed_time * PXS
        if x != xant:  #sometimes there is nothing between measures, so no time between them
            pygame.draw.line(stage, (9,180,237, 10), (xant, 0), (xant, screenHeight), 1)
            font = pygame.font.SysFont('Comic Sans MS', 10)
            text = font.render(str(me.number - 1), 1, (9, 180, 237))
            textpos = (xant+5, stageHeight-20)
            stage.blit(text,(textpos))
            xant = x
        try:
            elapsed_time += me.seconds
        except:
            tempo.MetronomeMark = short_score_part.semiFlat.getElementsByClass('MetronomeMark')[0]
            ts = short_score_part.semiFlat.getElementsByClass('TimeSignature')[0]
            elapsed_time += 240 * (ts.numerator / ts.denominator) / tempo.MetronomeMark.number'''             

      
def draw_scale():
    if key.mode == 'major':
        sc = scale.MajorScale(pitch.Pitch(key.tonic.name))
    else:
        sc = scale.MinorScale(pitch.Pitch(key.tonic.name))
    for p in sc.getPitches(minNote.nameWithOctave, maxNote.nameWithOctave):
        y = place_note(p.midi)
        #y = screenHeight - int(sc.pitchFromDegree(i).frequency)/4 + altura_notas/2#el 2 es a lo bruto 
        pygame.draw.line(stage, (0,0,100, 10), (0,y), (stageWidth, y), 1)
        #y = screenHeight - int(sc.pitchFromDegree(i).frequency)/2 + altura_notas/2#el 2 es a lo bruto 
        #pygame.draw.line(stage, (0,0,255, 10), (0,y), (screenWidth, y), 1)    

def place_note(pitch_midi):
    a = -(stageHeight*.60)/(max_midi_note - min_midi_note)
    b = (stageHeight*.40) / 2 - a * max_midi_note
    
    return a * pitch_midi + b

def fmtomidi(fm):
    return 12*math.log2(fm/440) + 69


def o2t(x):
    offset2sig = []
    offsets = []
    offset2time = []
    for ts in short_score_part.flat.getElementsByClass('TimeSignature'):
        offset2sig.append((ts.offset,ts.numerator/ts.denominator))
        offsets.append(ts.offset)
    for mm in short_score_part.flat.getElementsByClass('MetronomeMark'):
        ts_offset = max([z for z in offset2sig if z[0]<=mm.offset])
        if ts_offset[0] == mm.offset:
            offset2time.append((ts_offset[0],ts_offset[1] * 60.0 / mm.number))
        else:
            offset2time.append((mm.offset,ts_offset[1] * 60.0 / mm.number))
    offsets = [o for (o,t) in offset2time]                    
    closeoff =[offset for offset in offsets if offset <= x][-1]
    for i in range(offsets.index(closeoff),-1, -1):
        if i == offsets.index(closeoff):
            elapsed_time = (x - closeoff) * offset2time[i][1]
        else:
            elapsed_time += (offset2time[i+1][0] - offset2time[i][0])*offset2time[i][1]
    return elapsed_time         

short_score_part = shorten(score, part, start, end)
#score = score.makeMeasures()
#short_score = score_with_measures.flat.measures(start,end)
short_score = score.measures(start,end) #tarda mucho
short_score_midi = short_score.write('midi')
my_midi_file = short_score_midi



#to find where the notes should be placed on the screen:
list_midi_notes = [note.pitch.midi for note in short_score_part.flat.getElementsByClass('Note')]
min_midi_note = min(list_midi_notes)
max_midi_note = max(list_midi_notes)
minNote = note.Note(min_midi_note)
maxNote = note.Note(max_midi_note)

#short_score_part.show('text')
#print(short_score_part.flat.seconds)



pygame.init()
screenWidth, screenHeight = 1000, 512 #try with different set-ups
screen = pygame.display.set_mode((screenWidth, screenHeight))

#screen.set_alpha(0) 
clock = pygame.time.Clock()

pixel_per_second = screenWidth / short_score_part.flat.seconds
#pixel_event = screenWidth / score.quarterLength
color_default = (9,180,237)
altura_notas = 16
PXS = max(20,pixel_per_second)
stageHeight = screenHeight 
stageWidth = int(PXS * short_score_part.flat.seconds) 
running = True

freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024    # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)
# optional volume 0 to 1.0
pygame.mixer.music.set_volume(0.8)


     


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

stage = pygame.Surface((stageWidth, stageHeight)) 
stage.fill((0,0,0))
draw_scale()
all_displaid_notes_list = draw_notes()
draw_measures()
    

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
    pygame.display.set_caption(short_name_file + " page: " + str(stage_page + 1))
    screen.blit(stage,(-stage_page * screenWidth,0))
    rel_x = x % screenWidth
    pygame.draw.line(screen, (9,180,237, 10), (rel_x, 0), (rel_x, stageHeight), 1)                      

    #last page:
    last_page = int(stageWidth // screenWidth)
    if stage_page == last_page: #clear the remaining screen
        last_x = stageWidth%screenWidth
        clear_screen = pygame.Rect(last_x, 0, screenWidth - last_x, screenHeight)
        pygame.draw.rect(screen, (0,0,0), clear_screen)
        #draw double line to finish
        pygame.draw.line(screen, (9,180,237, 10), (last_x, 0), (last_x, screenHeight), 1)
        pygame.draw.line(screen, (9,180,237, 10), (last_x+2, 0), (last_x+2, screenHeight), 1) 

    # our user should be singing if there's a note on the queue
    if not q.empty():
        b = q.get()
         
        #y = screenHeight - int(b['NoteMidi']*ZOOM) 
        y = place_note(fmtomidi(b['NotePitch']))
        sing_sprite = sing_display(x,y,4)
    else:
        y = 0    

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
    #stoping the game if we reach the right end of the stage
    if music_position * PXS > stageWidth:
        if Repeat: 
            x = 0
            event = pygame.event.wait()
            stage.fill((0,0,0))
            all_displaid_notes_list = draw_notes()
            draw_measures()
            draw_scale()
            pygame.mixer.music.play()


            #screen.fill((255,255,255))
        else:
            running = False    

quit()        

    






