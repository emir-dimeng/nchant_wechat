'''
pydub--overlay
    https://github.com/jiaaro/pydub/blob/master/API.markdown

Overlay the shorter sound on the longer one, 
or by creating a silent AudioSegment with the appropriate duration, 
and overlaying both sounds on to that one.
'''
from pydub import AudioSegment

def overlay(rec1, rec2, fs, position1=0, position2=0):
    # Calculate the time difference to start ultering
    position = position1 - position2
    if position > 0:
        rec = rec1.overlay(rec2, position=position)
    else:
        start_time = position * (-1000)
        rec2 = rec2[start_time:]
        rec = rec1.overlay(rec2)
    return rec

