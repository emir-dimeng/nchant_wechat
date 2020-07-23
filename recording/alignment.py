import numpy as np
# import matplotlib.pyplot as plt
import soundfile as sf

import librosa
import librosa.display
from scipy.signal import savgol_filter
from pydub import AudioSegment
from pydub.playback import play
import os

'''
1. Separation:
    1.1. hspp_seq
    2.2. vocal_music_sep
2. Smoothing:
    smooth: savgol_filter
3. Onsets:
    3.1 superflux
    3.2 default_onsets
4. Overlay:
    overlay pydub
5. Alignment function:
    align
'''
'''
1.1
Separate an audio signal into its harmonic and percussive components.
reference: 
    Harmonic/Percussive Separation Using Median Filtering (Fitzgerald, 2010)
    Dreidger, Mueller and Disch, 2014 <http://www.terasoft.com.tw/conf/ismir2014/proceedings/T110_127_Paper.pdf>
source:
    https://librosa.org/librosa_gallery/auto_examples/plot_hprss.html
'''

# Separate an audio signal into its harmonic and percussive components
def hspp_sep(recording, fs, margin=20):
    # recording = harmonic + percussive
    # This technique is commonly used in MIR to suppress transients when analyzing pitch content
    # rec_harmonic, rec_percussive = librosa.effects.hpss(recording, margin=margin)
    rec_harmonic, rec_percussive = librosa.effects.hpss(recording, margin=margin)
    return rec_harmonic, rec_percussive

'''
1.2
Separat vocals (and other sporadic foreground signals) from accompanying instrumentation.

source:
https://librosa.org/librosa_gallery/auto_examples/plot_vocal_separation.html
'''
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

'''
2. Smoothing
'''
def smooth(x, loop=1, window_length=51, polyorder=1):
    smooth_x = x
    for i in range(loop):
        smooth_x = savgol_filter(smooth_x, window_length, polyorder) # window size 51, polynomial order 3
    return smooth_x

'''
3. Onsets
Superflux onsets
    It improves onset detection accuracy in the presence of vibrato
reference:
    Superflux (from librosa)
    -- Boeck and Widmer, 2013 <http://dafx13.nuim.ie/papers/09.dafx2013_submission_12.pdf>
    https://librosa.org/librosa_gallery/auto_examples/plot_superflux.html
'''

'''
3.1 superflux
'''
def superflux(y, fs, window_length=51, polyorder=1):
    # These parameters are taken directly from the paper
    n_fft = 1024
    hop_length = int(librosa.time_to_samples(1./200, sr=fs))
    lag = 2
    n_mels = 138
    fmin = 100
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
    envelope_sf = smooth(envelope_sf, 1, window_length, polyorder) 

    onset_sf = librosa.onset.onset_detect(onset_envelope=envelope_sf,
                                        sr=fs,
                                        hop_length=hop_length,
                                        units='time')
    first_onset = 0
    try:
        if onset_sf[0]>0.01:
            first_onset = onset_sf[0]
        else:
            first_onset = onset_sf[1]
    except:
        first_onset = 0
    return first_onset
'''
3.2 default method
'''
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
    env_default = smooth(env_default, 1, window_length, polyorder) # window size 51, polynomial order 3
    onset_def = librosa.onset.onset_detect(y=env_default, sr=fs, hop_length=hop_length,
                                           units='time')[0]
    return onset_def

'''
4.
pydub--overlay
    https://github.com/jiaaro/pydub/blob/master/API.markdown

Overlay the shorter sound on the longer one, 
or by creating a silent AudioSegment with the appropriate duration, 
and overlaying both sounds on to that one.
'''
def overlay(col_dir, y_dir, position_seed=0, position_y=0):
    # load autio data
    collective = AudioSegment.from_file(col_dir, format="wav")
    y = AudioSegment.from_file(y_dir, format="wav")
    # Calculate the time difference to start ultering
    position = position_seed - position_y
    print("onset_collective", position_seed)
    print("onset_new", position_y)
    if position > 0:
        rec = collective.overlay(y, position=position*1000)
    else:
        start_time = position * (-1000)
        y = y[start_time:]
        rec = collective.overlay(y)
    return rec

def align(rec_dir, collective_dir, seed_onset):
    # load audio data
    y, fs = librosa.load(rec_dir)
    collective, fs_c = librosa.load(collective_dir)
    # 1. separation
    y_harmonic, y_percussive = hspp_sep(y, fs)
    # 2. Smoothing
    y_percussive_smooth = smooth(y_percussive, 5, window_length=1001, polyorder=1)

    # y_harmonic = hspp_sep(y, fs)
    # 2+3. smoothing + onsets
    y_onset = superflux(y_percussive_smooth, fs)
    # col_onset = superflux(collective, fs_c)
    # overlay new recoring and collective
    align_rec = overlay(collective_dir, rec_dir, seed_onset, y_onset)
    # play(align_rec)
    # delete original file first
    delete_file(collective_dir)
    # update the collective voice
    align_rec.export(collective_dir, format="wav")

# tool: deletefile
def delete_file(file_dir):
    if os.path.exists(file_dir):
        os.remove(file_dir)
    else:
        print("The file does not exist")

# 
def seed_onset(seed_dir):
    # load audio data
    y, fs = librosa.load(seed_dir)
    # 1. separation
    y_harmonic, y_percussive = hspp_sep(y, fs)

    # 2. Smoothing
    y_percussive_smooth = smooth(y_percussive, 5, window_length=1001, polyorder=1)
    # y_harmonic = hspp_sep(y, fs)
    # 2+3. smoothing + onsets
    y_onset = superflux(y_percussive_smooth, fs)
    return y_onset