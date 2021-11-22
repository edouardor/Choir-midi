from music21 import * 
my_midi_file = '/Users/eduardoratier/Downloads/CAT00514 CORO.mid'


score = converter.parse(my_midi_file)

start = 0
start = max(1,start) #to avoid beginning by 0 or negativve number
end = 11
part = 3

Repeat = True

def speed_shorten(score, part, start, end):
    
    score_part = score.parts[part]
    score_part = score_part.makeMeasures()
    short_score_part = score_part.measures(1,22)
#score.show('text')
def shorten(score, part, start, end):
    score_part = score.parts[part]
    short_score_part = score_part.measures(start,end)
    # to copy metronome marks if needed:
    if part !=0:
        short_score_part_0 = score.parts[0].measures(start,end)
        for mm in short_score_part_0.flat.getElementsByClass('MetronomeMark'):
            try:
                short_score_part.insertAndShift(mm.offset,mm)
            except:
                continue  #the metronome mark already exists  

    #insert first metronome mark if needed:
    score = score.makeMeasures()
    start_measure = score.getElementsByClass('Measure')[start -1] #first measure has an 0 index
    mm_start = [mm for mm in score.flat.getElementsByClass('MetronomeMark') if mm.offset <= start_measure.offset][-1]
    short_score_part.insertAndShift(0,mm_start)
    return short_score_part

short_score = score.measures(start,end)
short_score_midi = short_score.write('midi')
my_midi_file = short_score_midi

short_score_part = shorten(score, part, start, end)
short_score_part.show('text')
print(short_score_part.flat.seconds)