
import aubio
import numpy as np
import pyaudio

import time
import argparse

import queue

import music21  # yes! new favorite library

parser = argparse.ArgumentParser()
parser.add_argument("-input", required=False, type=int, help="Audio Input Device")
args = parser.parse_args()
args.input = 0
if args.input== None:
    print("No input device specified. Printing list of input devices now: ")
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print("Device number (%i): %s" % (i, p.get_device_info_by_index(i).get('name')))
    print("Run this program with -input 1, or the number of the input you'd like to use.")
    exit()

# PyAudio object.
p = pyaudio.PyAudio()

# Open stream.
stream = p.open(format=pyaudio.paFloat32,
                channels=1, rate=44100, input=True,
                input_device_index=args.input, frames_per_buffer=4096)
#time.sleep(1)

# Aubio's pitch detection.
pDetection = aubio.pitch("default", 2048, 2048//2, 44100)
# Set unit.
pDetection.set_unit("Hz")
pDetection.set_silence(-40)

q = queue.Queue()


def get_current_note(volume_thresh=0.01, printOut=False):
    """Returns the Note Currently Played on the q object when audio is present
    
    Keyword arguments:

    volume_thresh -- the volume threshold for input. defaults to 0.01
    printOut -- whether or not to print to the terminal. defaults to False
    """
    current_pitch = music21.pitch.Pitch()

    while True:

        data = stream.read(1024, exception_on_overflow=False)
        samples = np.fromstring(data,
                                dtype=aubio.float_type)
        pitch = pDetection(samples)[0]

        # Compute the energy (volume) of the
        # current frame.
        volume = np.sum(samples**2)/len(samples) * 100

        if pitch and volume > volume_thresh:  # adjust with your mic!
            current_pitch.frequency = pitch   # pitch es la frecuencia dada por aubio, y se transforma en una instancia de current_pitch de Music21
        else:
            continue

        if printOut:
            print(current_pitch, pitch)
        
        else:
            current = current_pitch.nameWithOctave
            current_midi = current_pitch.midi
            q.put({'Note': current, 'Cents': current_pitch.microtone.cents, 'NotePitch': pitch, 'NoteMidi': current_midi}) #añadido NotePitch

if __name__ == '__main__':
    get_current_note(volume_thresh=0.001, printOut=True)

'''from threading import Thread
import pygame

#from shortvoiceController import q, get_current_note

pygame.init()

screenWidth, screenHeight = 288, 512
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False

    screen.fill((0, 0, 0))

    # draw line to show visually how far away from note voice is
    pygame.draw.line(screen, (255, 255, 255), (10, 290), (10, 310))
    pygame.draw.line(screen, (255, 255, 255), (screenWidth - 10, 290),
                     (screenWidth - 10, 310))
    pygame.draw.line(screen, (255, 255, 255), (10, 300),
                     (screenWidth - 10, 300))

    # our user should be singing if there's a note on the queue
    if not q.empty():
        b = q.get()
        if b['Cents'] < 15:
            pygame.draw.circle(screen, (0, 128, 0), 
                               (screenWidth // 2 + (int(b['Cents']) * 2),300),
                               5)
        else:
            pygame.draw.circle(screen, (128, 0, 0),
                               (screenWidth // 2 + (int(b['Cents']) * 2), 300),
                               5)

        noteText = noteFont.render(b['Note'], True, (0, 128, 0))
        if b['Note'] == noteHeldCurrently:
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
            noteHeld = 1
        screen.blit(noteText, (50, 400))

    screen.blit(titleText, (10,  80))
    screen.blit(titleCurr, (10, 120))
    pygame.display.flip()
    clock.tick(30)'''    