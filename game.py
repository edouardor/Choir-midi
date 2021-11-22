from threading import Thread
import pygame

from shortvoiceController import q, get_current_note
from midiroll21 import score
#bass_part.show('text')
pygame.init()

screenWidth, screenHeight = 1024, 512
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
dt = 0 #para ir de izquierda a derecha
time_lapse = 0.1

pixel_per_second = screenWidth / score.seconds
pixel_event = screenWidth / score.quarterLength
bass_part = score.parts[3]

running = True

titleFont = pygame.font.Font(None, 34)
titleText = titleFont.render("Sing a", True, (0, 128, 0))
titleCurr = titleFont.render("Low Note", True, (0, 128, 0))

noteFont = pygame.font.Font(None, 55)

t = Thread(target=get_current_note)
t.daemon = True
t.start()


low_note = ""
high_note = ""
have_low = False
have_high = True

noteHoldLength = 20  # how many samples in a row user needs to hold a note
noteHeldCurrently = 0  # keep track of how long current note is held
noteHeld = ""  # string of the current note

centTolerance = 20  # how much deviance from proper note to tolerate
screen.fill((255, 255, 255))
#draw piano roll:
for thisNote in bass_part.getElementsByClass(["Note", "Rest"]):
        #print(thisNote, thisNote.offset)
    if thisNote.isNote:    
        x, y = thisNote.offset, thisNote.pitch.frequency
        z = thisNote.seconds

        pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(x * pixel_event, screenHeight - int(y), z*pixel_per_second, 15))

pygame.event.clear()
pygame.event.wait()


while running:

            #print(x * pixel_per_second,z*pixel_per_second)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False

           

    

    # draw line to show visually how far away from note voice is
    '''pygame.draw.line(screen, (255, 255, 255), (10, 290), (10, 310))
    pygame.draw.line(screen, (255, 255, 255), (screenWidth - 10, 290),
                     (screenWidth - 10, 310))
    pygame.draw.line(screen, (255, 255, 255), (10, 300),
                     (screenWidth - 10, 300))'''

    # our user should be singing if there's a note on the queue
    dt += time_lapse
    if not q.empty():
        b = q.get()
       
        '''if b['Cents'] < 15:
            pygame.draw.circle(screen, (0, 128, 0), 
                               (screenWidth // 2 + (int(b['Cents']) * 2),300),
                               5)
        else:
            pygame.draw.circle(screen, (128, 0, 0),
                               (screenWidth // 2 + (int(b['Cents']) * 2), 300),
                               5)'''

        pygame.draw.circle(screen, (0, 128, 255),
                               (dt, screenHeight - int(b['NotePitch'])), 3)
        if dt > screenWidth:
            running = False                       
                            
        noteText = noteFont.render(b['Note'], True, (0, 128, 0))
        '''if b['Note'] == noteHeldCurrently:
            noteHeld += 1
            if noteHeld == noteHoldLength:
                if not have_low:
                    low_note = noteHeldCurrently
                    have_low = True
                    titleCurr = titleFont.render("High Note", True, 
                                                 (128, 128, 0))
                else:
                    if int(noteHeldCurrently[-1]) <= int(low_note[-1]):
                        noteHeld = 0  # we're holding a lower octave note
                    elif int(noteHeldCurrently[-1]) and not high_note:
                        high_note = noteHeldCurrently
                        have_high = True
                        titleText = titleFont.render("Perfect!", True,
                                                     (0, 128, 0))
                        titleCurr = titleFont.render("%s to %s" % 
                                                     (low_note, high_note), 
                                                     True, (0, 128, 0))
        else:
            noteHeldCurrently = b['Note']
            noteHeld = 1'''
        screen.blit(noteText, (50, 400))

    screen.blit(titleText, (10,  80))
    screen.blit(titleCurr, (10, 120))
    pygame.display.flip()
    #clock.tick(60)