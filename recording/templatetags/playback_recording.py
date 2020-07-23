#!/usr/bin/env python3
"""
Play back an array and record at the same time. 

playrec()
https://python-sounddevice.readthedocs.io/en/0.3.15/usage.html#simultaneous-playback-and-recording
"""
from django import template
register = template.Library()

import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf

# Simultaneous Playback and Recording
@register.simple_tag
def play_rec(origin_dir):
    # reading the seed/collective voice
    # y, fs = sf.read(origin_dir, dtype='float32')
    # Playback and Recording
    # new_rec = sd.playrec(y, fs, channels=2)
    new_rec = origin_dir
    print(new_rec)
    return new_rec
'''
# save new recording
def save_rec(new_rec, new_dir):
    # save
    write(new_dir, fs, new_rec)
'''
# play new_record
@register.simple_tag
def play(y, fs=22500):
    # reading the seed/collective voice
    sd.playrec(y, fs, channels=2)
    status = sd.wait()
    return 1