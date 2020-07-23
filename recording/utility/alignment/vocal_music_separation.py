'''
Separat vocals (and other sporadic foreground signals) from accompanying instrumentation.

source:
https://librosa.org/librosa_gallery/auto_examples/plot_vocal_separation.html
'''

from __future__ import print_function
import numpy as np
import librosa

import librosa.display

# function: magphase_to_time 
# magphase: magnitude + phase
def magphase_to_time(mag, phase):
    # phase = np.cos(phase_angle) + 1.j * np.sin(phase_angle)
    return librosa.istft(mag * phase)

'''
define vocal separation function based on:
    1. nn_filter
    2. softmask
'''
def vocal_sep(y, fs):
    # compute the spectrogram magnitude and phase
    S_full, phase = librosa.magphase(librosa.stft(y))
    # We'll compare frames using cosine similarity, and aggregate similar frames
    # by taking their (per-frequency) median value.
    #
    # To avoid being biased by local continuity, we constrain similar frames to be
    # separated by at least 2 seconds.
    #
    # This suppresses sparse/non-repetetitive deviations from the average spectrum,
    # and works well to discard vocal elements.

    S_filter = librosa.decompose.nn_filter(S_full,
                                        aggregate=np.median,
                                        metric='cosine',
                                        width=int(librosa.time_to_frames(2, sr=fs)))

    # The output of the filter shouldn't be greater than the input
    # if we assume signals are additive.  Taking the pointwise minimium
    # with the input spectrum forces this.
    S_filter = np.minimum(S_full, S_filter)
    # We can also use a margin to reduce bleed between the vocals and instrumentation masks.
    # Note: the margins need not be equal for foreground and background separation
    margin_i, margin_v = 2, 20
    power = 2

    mask_i = librosa.util.softmask(S_filter,
                                margin_i * (S_full - S_filter),
                                power=power)

    mask_v = librosa.util.softmask(S_full - S_filter,
                                margin_v * S_filter,
                                power=power)

    # Once we have the masks, simply multiply them with the input spectrum
    # to separate the components
    S_foreground = mask_v * S_full
    S_background = mask_i * S_full

    # transfom signal back to time series (audio data)
    foreground = magphase_to_time(S_foreground, phase)
    background = magphase_to_time(S_background, phase)

    return foreground, background


