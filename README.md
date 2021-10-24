# Piano roll with voice pitch control

From a midi file with choir voices (typically SATB), you can choose the voice you want to sing which is displayed like a piano roll.
If you sing the correct pitch, the color of the note will change and you will earn points.

## Requirements

We use PyAudio, NumPy, Music21, PyGame, Tkinter and Aubio to do all voice analysis and drawing to the screen. You'll need to have all of these libraries installed in order to get everything to work.

Most of this should be `pip` installable.

You will also need a midi file, and optionally a mp3 file made with the midi file throught a DAW and a text file with the lyrics, both saved in the same directory and with the same name than the midi file, with mp3 and txt extensions. 
