from threading import Thread
import pygame
import math
from shortvoiceController import q, get_current_note
from music21 import *
from tk_2 import App

my_app = App()
filename = my_app.filename
score = my_app.score
score_with_measures = my_app.score_with_measures
key = my_app.key
part = my_app.selected_part.get()
Repeat = my_app.repeat.get()
start = my_app.first_measure.get()
end = my_app.last_measure.get()
pygame.font.init()
 
my_midi_file = filename
short_name_file = my_midi_file[my_midi_file.rfind('/')+1:]

def shorten(score, score_with_measures, part, start, end):
    score_part = score.parts[part]
    score_part = score_part.makeMeasures()
    short_score_part = score_part.measures(start,end)  
    #insert first metronome mark:
    start_measure = score_with_measures.getElementsByClass('Measure')[start -1] #first measure has an 0 index
    mm_start = [mm for mm in score_with_measures.flat.getElementsByClass('MetronomeMark') if mm.offset <= start_measure.offset][-1]

    short_score_part.insertAndShift(0,mm_start)
    if part !=0:
        short_score_part_0 = score.parts[0].measures(start,end)
        for mm in short_score_part_0.flat.getElementsByClass('MetronomeMark'):
            try:
                short_score_part.insertAndShift(mm.offset,mm)
            except:
                continue  #the metronome mark already exists    

    return short_score_part, mm_start

def draw_note(n,elapsed_time, duration):
     
    font = pygame.font.SysFont('Comic Sans MS', 10)
    x = elapsed_time * PXS #pixel_per_second
    y = place_note(n.pitch.midi) - altura_notas / 2
    longitud = duration * PXS #pixel_per_second
    note_rect = Colored_rect(x ,y, longitud, altura_notas,color_default)           
    pygame.draw.rect(stage, color_default, note_rect, 2,4)
    text = font.render(n.pitch.spanish, 1, (9, 180, 237))
    textpos = (x+5, y)
    stage.blit(text, textpos)
    
    return note_rect           

def draw_notes():
    all_displaid_notes_list = []
    for element in sflatM:
        elapsed_time = element['offsetSeconds']
        x = elapsed_time * PXS
        duration = element['durationSeconds']

        if isinstance(element['element'], note.Note):
            n = element['element']
            note_rect = draw_note(n, elapsed_time, duration)
            all_displaid_notes_list.append(note_rect)

        elif isinstance(element['element'], chord.Chord):
            for n in element['element']:
                note_rect = draw_note(n, elapsed_time, duration)
                all_displaid_notes_list.append(note_rect)

        elif isinstance(element['element'],meter.TimeSignature):
            sign = element['element']
            draw_text(str(sign.numerator) + '/' + str(sign.denominator),(x+5,20))           
     
    return all_displaid_notes_list

def draw_measures():
    for element in sM:
        elapsed_time = element['offsetSeconds']
        x = elapsed_time * PXS
        if isinstance(element['element'], stream.Measure):
            me = element['element'] #me is a measure
            pygame.draw.line(stage, (0,0,100,10), (x, 0), (x, screenHeight), 1)     
            draw_text(str(me.number),(x+5, stageHeight-20))
        elif isinstance(element['element'], tempo.MetronomeMark):
            tmpo = element['element']
            draw_text(str(int(tmpo.number)),(x+5, 10))
   
     
def draw_scale():
    if key.mode == 'major':
        sc = scale.MajorScale(pitch.Pitch(key.tonic.name))
    else:
        sc = scale.MinorScale(pitch.Pitch(key.tonic.name))
    for p in sc.getPitches(minNote.nameWithOctave, maxNote.nameWithOctave):
        y = place_note(p.midi) 
        pygame.draw.line(stage, (0,0,100, 10), (0,y), (stageWidth, y), 1)    

def place_note(pitch_midi):
    a = -(stageHeight*.60)/(max_midi_note - min_midi_note)
    b = (stageHeight*.40) / 2 - a * max_midi_note
    return a * pitch_midi + b

def fmtomidi(fm):
    return 12*math.log2(fm/440) + 69

def mov_avg(numbers_list, window_size): #trailing moving averages to smooth input pitch
    moving_averages =[]
    for j in range(1,len(numbers_list)+1):
        if j < window_size:
            this_window = numbers_list[0:j]
        else:
            this_window = numbers_list[j-window_size  : j]
        window_average = sum(this_window) / len(this_window)
        moving_averages.append(window_average)      
    return moving_averages

def draw_text(my_text, text_pos):
    font = pygame.font.SysFont('Comic Sans MS', 10)
    text = font.render(my_text, 1, (9, 180, 237))
    stage.blit(text, text_pos) 


short_score_part, mm_start = shorten(score, score_with_measures,part, start, end)
sM = short_score_part.secondsMap  #for drawing Measures
sflatM = short_score_part.flat.secondsMap #for drawing Notes
short_score = score.measures(start,end)
 #tarda mucho
short_score.insertAndShift(0,mm_start) 
short_score_midi = short_score.write('midi')
my_midi_file = short_score_midi

#to find where the notes should be placed on the screen:
list_midi_notes = [note.pitch.midi for note in short_score_part.flat.getElementsByClass('Note')]
min_midi_note = min(list_midi_notes)
max_midi_note = max(list_midi_notes)
minNote = note.Note(min_midi_note)
maxNote = note.Note(max_midi_note)

pygame.init()
screenWidth, screenHeight = 1000, 512 #try with different set-ups
screen = pygame.display.set_mode((screenWidth, screenHeight))
 
clock = pygame.time.Clock()

pixel_per_second = screenWidth / short_score_part.flat.seconds
color_default = (9,180,237)
altura_notas = 16
PXS = max(40,pixel_per_second)
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

        pygame.draw.circle(stage, (190, 220, 250),(x, y), 2,2)

    @property
    def rect(self):  
        return pygame.Rect(self.x, self.y, 1, 2*math.pi*self.radio)                   


t = Thread(target=get_current_note)
t.daemon = True
t.start()
dt = 0.0
old_avg = 0
x = 0
n = 0
list_sung_notes = []

stage = pygame.Surface((stageWidth, stageHeight)) 
stage.fill((0,0,0))
draw_scale()
all_displaid_notes_list = draw_notes()
draw_measures()
    

pygame.mixer.music.load(my_midi_file)
pygame.event.wait()
pygame.mixer.music.play()

###Now the game starts:
while running:
    
    #clock.tick(100) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            while True: #Infinite loop that will be broken when the user press the space bar again
                #pygame.mixer.music.pause()
                #sp.stop()
                event = pygame.event.wait()
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    #pygame.mixer.music.unpause()
                    break #Exit infinite loop        
    music_position = pygame.mixer.music.get_pos() / 1000  # in seconds
    
    x = music_position * PXS
    y = 0
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
        y = place_note(fmtomidi(b['NotePitch']))
        list_sung_notes.append(y)
        window_size = 20
        last = mov_avg(list_sung_notes, window_size)[-1]
         #moving average to smooth intro
        #pygame.draw.line(stage, (190, 220, 250),(x_ant, old_avg),(x, new_avg), 1)
        
        sing_sprite = sing_display(x,last,4)
    else:
        list_sung_notes = []
        
      
          

    for note_rect in all_displaid_notes_list:
        color = note_rect.color
        if note_rect.collidepoint(x, y):
            note_rect.collided += 1
            green = color[1]-note_rect.collided//(10)
            if green <0: green = 0
            color = (0,green,255)
            note_rect.color = color
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
        else:
            running = False    

quit()        

    






