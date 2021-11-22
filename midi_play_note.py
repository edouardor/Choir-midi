import fluidsynth
import time

# import pygame.midi and initialize the midi module before you use it.
# pygame.midi is not a default pygame module so you need to import it,
# and also pygame.init does not init it for you.
# from https://www.patreon.com/posts/midi-music-pygame-python-43826303
import pygame.midi

# initialize the midi module before you use it.
#  pygame.init does not do this for you.
pygame.midi.init()

fs = fluidsynth.Synth()
fs.start(driver = 'coreaudio')  # use DirectSound driver

sfid = fs.sfload(r'/Users/eduardoratier/ImportedSoundFonts/GeneralUser.sf2')  # replace path as needed
fs.program_select(0, sfid, 0, 0) #program_select(track, soundfontid, banknum, presetnum)

fs.noteon(0, 60, 80) #noteon(track, midinum, velocity)
fs.noteon(0, 67, 127)
fs.noteon(0, 76, 30)

time.sleep(3.0)

fs.noteoff(0, 60)
fs.noteoff(0, 67)
fs.noteoff(0, 76)

time.sleep(1.0)

fs.delete()

# print the devices and use the last output port.
'''for i in range(pygame.midi.get_count()):
    r = pygame.midi.get_device_info(i)
    (interf, name, is_input, is_output, is_opened) = r
    print (interf, name, is_input, is_output, is_opened)
    if is_output:
        last_port = i

# You could also use this to use the default port rather than the last one.
default_port = pygame.midi.get_default_output_id()
if default_port == -1:
    default_port = 1

midi_out = pygame.midi.Output(default_port, 0)

# select an instrument.
instrument = 19 # general midi church organ.
midi_out.set_instrument(instrument)

# play a note.
midi_out.note_on(note=62, velocity=127)
midi_out.note_off(note=62, velocity=0)

# sleep for a bit, and play another higher pitched note.
time.sleep(0.2)
midi_out.note_on(note=80, velocity=127)
midi_out.note_off(note=80, velocity=0)
time.sleep(0.2)

# play a note for longer.
midi_out.note_on(note=62, velocity=127)
time.sleep(0.8)
midi_out.note_off(note=62, velocity=0)


#otro:
import pygame.midi
import time

pygame.midi.init()
player = pygame.midi.Output(1)
player.set_instrument(0)
player.note_on(64, 127)
time.sleep(1)
player.note_off(64, 127)
del player
pygame.midi.quit()'''