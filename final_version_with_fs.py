from threading import Thread
import pygame
import math
import time
from voice_input import q, get_current_note
from music21 import *
from tk_2 import App
import pygame.midi #to be able to play notes when game is paused
import fluidsynth

my_app = App()
filename = my_app.filename
score = my_app.score
score_with_measures = my_app.score_with_measures
key = my_app.key
part = my_app.selected_part.get()
Repeat = my_app.repeat.get()
Silence = my_app.silence.get()
start = my_app.first_measure.get()
end = my_app.last_measure.get()
pygame.font.init()
 
my_midi_file = filename
short_name_file = my_midi_file[my_midi_file.rfind('/')+1:]
# the lyrics of the song should be, if any, in the same directory 
text_file = my_midi_file[:my_midi_file.rfind('.')]+'.txt'
# the mp3 file of the song should be, if any, in the same directory
mp3_file = my_midi_file[:my_midi_file.rfind('.')]+'.mp3'
moving = False
def open_file(file_name):
    try:
        f = open(file_name, 'r')
        return f
    except FileNotFoundError:
        return False
"""
shorten(score, score_with_measures, part, start, end)

This function takes a score, a part, a start and an end measure and returns a shortened score.

Parameters
----------
score : music21.stream.Score
    The score to be shortened.
score_with_measures : music21.stream.Score
    The score with measures.
part : int
    The part to be shortened.
start : int
    The start measure.
end : int
    The end measure.

Returns
-------
short_score_part : music21.stream.Score
    The shortened score.
mm_start : music21.tempo.MetronomeMark
    The metronome mark of the start measure."""
    
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
     
    font = pygame.font.SysFont('Arial', 10)
    x = elapsed_time * PXS #pixel_per_second
    y = place_note(n.pitch.midi) - altura_notas / 2
    longitud = duration * PXS #pixel_per_second
    note_rect = Colored_rect(x ,y, longitud, altura_notas,color_default)          
    pygame.draw.rect(stage, color_default, note_rect, 2,4)
    text = font.render(n.pitch.spanish, 1, (9, 180, 237))
    textpos = (x+5, y)
    stage.blit(text, textpos)
    if lyrics_file:

        #text = font.render(n.lyrics[0].text, 1, (9, 180, 237))
        #textpos = (x+5, y+20)
        #stage.blit(text, textpos)
        draw_text(n.lyrics[0].text,(x+5, y+10),20)
    
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
"""
Here's what the above functions are doing:
1. We create a list of all the notes and chords in the piece.
2. We iterate through the list, and for each element, we draw a rectangle.
3. We return a list of all the rectangles we've drawn.
"""
def draw_measures():
    for element in sM:
        elapsed_time = element['offsetSeconds']
        x = elapsed_time * PXS
        if isinstance(element['element'], stream.Measure):
            me = element['element'] #me is a measure
            pygame.draw.line(stage, (4, 0, 143,10), (x, 0), (x, screenHeight-20), 1)     
            draw_text(str(me.number),(x, stageHeight-40))
        elif isinstance(element['element'], tempo.MetronomeMark):
            tmpo = element['element']
            draw_text(str(int(tmpo.number)),(x+5, 10))
   
     
def draw_scale():
    line_color = 0
    if key.mode == 'major':
        sc = scale.MajorScale(pitch.Pitch(key.tonic.name))
    else:
        sc = scale.MinorScale(pitch.Pitch(key.tonic.name))
    for p in sc.getPitches(minNote.nameWithOctave, maxNote.nameWithOctave):
        y = place_note(p.midi) 
        pygame.draw.line(stage, (0,min(line_color,255),140, 10), (0,y), (stageWidth, y), 2)    
        draw_text(p.spanish,(5,y - altura_notas / 2-10))
        line_color += 20
def place_note(pitch_midi):
    a = -(stageHeight*.60)/(max_midi_note - min_midi_note)
    b = (stageHeight*.40) / 2 - a * max_midi_note
    return a * pitch_midi + b

def midi_note(y):
    a = -(stageHeight*.60)/(max_midi_note - min_midi_note)
    b = (stageHeight*.40) / 2 - a * max_midi_note
    return int((y-b)/a)


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

def draw_text(my_text, text_pos, font_size = 20, on_stage = True):
    font = pygame.font.SysFont('Arial', font_size)
    text = font.render(my_text, 1, (9, 180, 237))
    if on_stage:
        stage.blit(text, text_pos)
    else:
        screen.blit(text, text_pos)

def redraw(best_score):
        stage.fill((0,0,0))
        all_displaid_notes_list = draw_notes()
        draw_measures()
        draw_scale() 
        draw_text('best score: '+str(best_score),(screenWidth / 2-25, 45), 15, False)

def insert_lyrics(words):
    count = 0
    for element in sflatM:
        if isinstance(element['element'], note.Note):
            n = element['element']
            try:
                n.addLyric(words[count])
                count+=1
            except:
                n.addLyric('-')    

        elif isinstance(element['element'], chord.Chord):
            for n in element['element']:
                try:
                    n.addLyric(words[count]) #misma letra para cada nota del acorde
                except:
                    n.addLyric('-')

            count+=1

# when paused, allow the user to press a rectangle to hear the note
def check_note():
    if event.type == pygame.MOUSEBUTTONDOWN:
        for note_rect in all_displaid_notes_list: 
            #print(event.pos,note_rect.x, note_rect.y)
            if note_rect.collidepoint((event.pos[0] + stage_page * screenWidth),event.pos[1]):
                #midi_note_number = midi_note(note_rect.y)
                #color = note_rect.color
                
                #note_rect.color = (0,0,255)
                #pygame.draw.rect(stage, (0,0,255), note_rect, 0,4)
                #pygame.draw.rect(stage, color_default, note_rect, 2,4)
                
                #pygame.display.flip()
                fs.noteon(0,midi_note(note_rect.y), 127)
                time.sleep(min(1,note_rect.w / PXS))
                fs.noteoff(0,midi_note(note_rect.y))
                #note_rect.color = color
                
                break      
    return
def check_rewind_moving(motion):
    moving = motion
    if event.type == pygame.MOUSEBUTTONDOWN:
        if rewind_line.collidepoint((event.pos[0] + stage_page * screenWidth),event.pos[1]):
            moving = True
            rewind_line_color = (0,255,0)
    
    elif event.type == pygame.MOUSEBUTTONUP:
        moving = False
        rewind_line_color = color_default
    
            # Make your image move continuously
    elif event.type == pygame.MOUSEMOTION and moving:
        rewind_line.move_ip(event.rel)
    
    return moving
        

short_score_part, mm_start = shorten(score, score_with_measures,part, start, end)


sM = short_score_part.secondsMap  #for drawing Measures
sflatM = short_score_part.flat.secondsMap #for drawing Notes

sound_file = open_file(mp3_file)
if not sound_file:
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

# to load lyrics if any
lyrics_file = open_file(text_file)
if lyrics_file:
    lyrics_lines = lyrics_file.readlines()
    lyrics_file.close()
    words = []
    for line in lyrics_lines[start-1:end]:
        words += [word for word in line.split() if word != '_']
    insert_lyrics(words)    

#open an mp3 file if any

if sound_file:
    music_start_time = score_with_measures.secondsMap[start-1]['offsetSeconds']
else:
    music_start_time = 0

pygame.init()
screenWidth, screenHeight = 1200, 800 #try with different set-ups
screen = pygame.display.set_mode((screenWidth, screenHeight))#,pygame.FULLSCREEN)
 
#clock = pygame.time.Clock()

pixel_per_second = screenWidth / short_score_part.flat.seconds
color_default = (116, 157, 214) #(9,180,237)
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
volume = 0.8    
if Silence:    
    pygame.mixer.music.set_volume(0)
else:
    pygame.mixer.music.set_volume(volume) 


class Colored_rect(pygame.Rect):
   
    def __init__(self,x,y,w,h,color,collided=0): 
        super().__init__(x,y,w,h)
        self.color = color
        self.collided = collided
        self.y = y                        

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
x = 0
#n = 0
score = 0
best_score = 0
list_sung_notes = []



stage = pygame.Surface((stageWidth, stageHeight)) 
stage.fill((0,0,0))
draw_scale()
all_displaid_notes_list = draw_notes()
draw_measures()
rewind_line = pygame.Rect(0,0,4,2*stageHeight)
       

if sound_file:
    pygame.mixer.music.load(sound_file)
else:    
    pygame.mixer.music.load(my_midi_file)

#to be changed if program is shared with other people
#should ask if there is a sound file sf2 somewhere
pygame.midi.init()

fs = fluidsynth.Synth()
fs.start(driver = 'coreaudio')  # use DirectSound driver

sfid = fs.sfload(r'/Users/eduardoratier/ImportedSoundFonts/GeneralUser.sf2')  # replace path as needed
fs.program_select(0, sfid, 0, 0) #program_select(track, soundfontid, banknum, presetnum)

pygame.mixer.music.play(-1,music_start_time) 
#beginning_time = time.time()
stime = time.time()
is_paused = False
delta = 0
elapsed = 0
paused_time = 0
pygame.event.clear()
rewind = False
rewind_line_color = color_default






###Now the game starts:
while running:
    
    #clock.tick(100)
    #stime = time.time()-beginning_time
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False
            break
        #now = time.time()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            while True: #Infinite loop that will be broken when the user press the space bar again
                if sound_file:
                    pygame.mixer.music.pause()
                    paused_time = time.time()
                    check_note()
                    #moving = check_rewind_moving(moving)
                    #moving = check_move_rewind()
                    pygame.event.clear()
                else:   
                    pygame.mixer.music.stop()
                #sp.stop()
                event = pygame.event.wait()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                    #pygame.mixer.music.unpause()
                        best_score = max(score, best_score)
                        redraw(best_score)
                        score = 0
                        pygame.mixer.music.play(-1, music_start_time)
                        rewind = True
                    elif  event.key == pygame.K_SPACE:
                        pygame.mixer.music.unpause() if sound_file else pygame.mixer.music.play()  
                        #paused_time -= time.time()
                        stime += time.time() - paused_time #gpt-4
                        break #Exit infinite loop 
                    '''elif event.key == pygame.K_BACKSPACE and sound_file:
                        elapsed = time.time() - stime + paused_time
                        delta = min(music_position, 5)
                        rewind = True
                        redraw(score)
                    
                        pygame.mixer.music.play(start=music_start_time + elapsed - delta)'''
        

        #pygame.mixer.music.play(start=music_start_time + elapsed - delta) 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            best_score = max(score, best_score)
            redraw(best_score)
            score = 0
            pygame.mixer.music.play(-1,music_start_time+elapsed-delta)
            
            
            
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE and sound_file:
            #pygame.mixer.music.rewind()
                
                elapsed = time.time() - stime #+ paused_time #gpt-4q
                



                delta = min(music_position, 5)
                rewind = True
                redraw(score)
                #pygame.mixer.music.set_pos(music_position * 1000)


                pygame.mixer.music.play(start=music_start_time+elapsed-delta)
                #pygame.mixer.music.play(-1,music_position-delta)
                #paused_time = 0
                stime += delta


        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN: 
            volume = max(0,volume-0.1)
            pygame.mixer.music.set_volume(volume) 
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP: 
            volume = min(1, volume+0.1)
            pygame.mixer.music.set_volume(volume)

        
        if event.type == pygame.MOUSEBUTTONDOWN:
            #if rewind_line.collidepoint((event.pos[0] + stage_page * screenWidth),event.pos[1]):
            if rewind_line.collidepoint(event.pos):  
                moving = True
                rewind_line_color = (0,255,0)
    
        elif event.type == pygame.MOUSEBUTTONUP:
            moving = False
            rewind_line_color = color_default
            #pygame.draw.rect(stage, rewind_line_color, rewind_line, 1)
    
            # Make your image move continuously
        elif event.type == pygame.MOUSEMOTION and moving:
            rewind_line.move_ip(event.rel)
            #pygame.draw.rect(stage, (9,180,237, 100), rewind_line, 1)
            #pygame.draw.rect(screen, rewind_line_color, rewind_line, 1)
            #pygame.display.update(rewind_line)
                
                #draw_text('rewind_touch'+ str(elapsed)[0:5],(screenWidth -150, 45), 15, False)            
                 
        
    music_position = pygame.mixer.music.get_pos() / 1000 + elapsed - delta # in seconds
    #music_position = stime
    x = music_position * PXS
    y = 0
    stage_page = int(x // screenWidth)  
    pygame.display.set_caption(short_name_file + " page: " + str(stage_page + 1))
    screen.blit(stage,(-stage_page * screenWidth,0))
    rel_x = x % screenWidth
    if rewind:
        #rewind_x = rel_x
        rewind_line = pygame.Rect(x,0,4,2*stageHeight)
        #pygame.draw.rect(screen, rewind_line_color, rewind_line, 1)
        #pygame.draw.line(stage, (9,180,237, 100), (rewind_x, 0), (rewind_x, stageHeight), 1)                      
        rewind = False
    #if moving:
    pygame.draw.rect(stage, rewind_line_color, rewind_line, 1)


    pygame.draw.line(screen, (9,180,237, 10), (rel_x, 0), (rel_x, stageHeight), 1)                      

    #wait for any key to be stroked before beginning
    '''if music_position == 0:
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                break'''
    
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
        window_size = 2
        last = mov_avg(list_sung_notes, window_size)[-1]
         #moving average to smooth intro
        #pygame.draw.line(stage, (190, 220, 250),(x_ant, old_avg),(x, new_avg), 1)
        
        sing_sprite = sing_display(x,last,4)
    else:
        list_sung_notes = []
        
    draw_text('q to quit, left arrow to rewind, up and down for volume' ,(screenWidth / 2-150, 65), 15, False)  
    if sound_file:
        draw_text('backspace to rewind 5 s, space to pause' ,(screenWidth / 2-129, 85), 15, False)

    draw_text(str(score),(screenWidth / 2, 0), 30, False)
    draw_text('elapsed: '+ str(elapsed)[0:5],(screenWidth -150, 45), 15, False)
    draw_text('paused  : '+ str(paused_time)[0:5],(screenWidth -150, 65), 15, False)
    draw_text('position:'+ str(music_position)[0:5],(screenWidth -150, 85), 15, False)
    draw_text('delta   :'+ str(delta)[0:5],(screenWidth -150, 105), 15, False)
    draw_text('stime   :'+ str(stime)[0:5],(screenWidth -150, 125), 15, False)
    if Repeat:
        draw_text('best score: '+str(best_score),(screenWidth / 2-25, 45), 15, False)      

    for note_rect in all_displaid_notes_list:
        color = note_rect.color
        if note_rect.collidepoint(x, y):
            score += 1
                        
            note_rect.collided += 1
            green = color[1]-note_rect.collided//(10) #less green
            if green <0: 
                green = 0
                #draw_text('+20',(x, y-20), 10, True)
                score +=19

            color = (0,green,255)
            note_rect.color = color
            pygame.draw.rect(stage, color, note_rect, 0,4)
        else:
            pygame.draw.rect(stage, color_default, note_rect, 2,4)     
        
    pygame.display.update()                        
    #stoping the game if we reach the right end of the stage
    if music_position * PXS > stageWidth:
        if Repeat: 
            pygame.mixer.music.stop()
            x = 0
            pygame.event.clear()
            '''while True:
                event = pygame.event.wait()
                if event.type == pygame.KEYDOWN:
                    break'''
            best_score = max(score, best_score)
            redraw(best_score)
            score = 0
            pygame.mixer.music.play(-1,music_start_time) 
            stime = time.time()
            is_paused = False
            delta = 0
            elapsed = 0

        else:
            running = False    

quit()        

    






