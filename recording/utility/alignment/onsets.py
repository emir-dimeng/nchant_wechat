'''
Superflux onsets
    It improves onset detection accuracy in the presence of vibrato
reference:
    Superflux (from librosa)
    -- Boeck and Widmer, 2013 <http://dafx13.nuim.ie/papers/09.dafx2013_submission_12.pdf>
    https://librosa.org/librosa_gallery/auto_examples/plot_superflux.html
'''

from __future__ import print_function
import numpy as np

import librosa
import librosa.display
import smoothing

'''
superflux
'''
def superflux(y, fs, window_length=51, polyorder=3):
    # These parameters are taken directly from the paper
    n_fft = 1024
    hop_length = int(librosa.time_to_samples(1./200, sr=fs))
    lag = 2
    n_mels = 138
    fmin = 27.5
    fmax = 16000.
    max_size = 3
    # The paper uses a log-frequency representation, 
    # but for simplicity, we'll use a Mel spectrogram instead.
    S = librosa.feature.melspectrogram(y, sr=fs, n_fft=n_fft, 
                                    hop_length=hop_length,
                                    fmin=fmin,
                                    fmax=fmax,
                                    n_mels=n_mels)
                                    
    # compute the onset strength envelope  
    # onset events using the librosa defaults.
    envelope_sf = librosa.onset.onset_strength(S=librosa.power_to_db(S, ref=np.max),
                                        sr=fs,
                                        hop_length=hop_length,
                                        lag=lag, max_size=max_size)
    # smoothing the envelope
    # window size 51, polynomial order 3
    envelope_sf = smoothing.smooth(envelope_sf, window_length, polyorder) 

    onset_sf = librosa.onset.onset_detect(onset_envelope=envelope_sf,
                                        sr=fs,
                                        hop_length=hop_length,
                                        units='time')
    return onset_sf

def default_onset(y, fs, window_length=51, polyorder=3):
    # These parameters are taken directly from the paper
    n_fft = 1024
    hop_length = int(librosa.time_to_samples(1./200, sr=fs))
    n_mels = 138
    fmin = 27.5
    fmax = 16000.
    # The paper uses a log-frequency representation, 
    # but for simplicity, we'll use a Mel spectrogram instead.
    S = librosa.feature.melspectrogram(y, sr=fs, n_fft=n_fft, 
                                    hop_length=hop_length,
                                    fmin=fmin,
                                    fmax=fmax,
                                    n_mels=n_mels)
                                    
    # compute the onset strength envelope  
    # onset events using the librosa defaults.
    env_default = librosa.onset.onset_strength(y=y, sr=fs, hop_length=hop_length)
    env_default = smoothing.smooth(env_default, window_length, polyorder) # window size 51, polynomial order 3
    onset_def = librosa.onset.onset_detect(y=env_default, sr=fs, hop_length=hop_length,
                                           units='time')
    return onset_def