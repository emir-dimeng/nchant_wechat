'''
Separate an audio signal into its harmonic and percussive components.
reference: 
    Harmonic/Percussive Separation Using Median Filtering (Fitzgerald, 2010)
    Dreidger, Mueller and Disch, 2014 <http://www.terasoft.com.tw/conf/ismir2014/proceedings/T110_127_Paper.pdf>
source:
    https://librosa.org/librosa_gallery/auto_examples/plot_hprss.html
'''
import numpy as np
# import matplotlib.pyplot as plt
import soundfile as sf

import librosa
import librosa.display

# Separate an audio signal into its harmonic and percussive components
def hspp_sep(recording, fs, margin=20):
    # recording = harmonic + percussive
    # This technique is commonly used in MIR to suppress transients when analyzing pitch content
    rec_harmonic, rec_percussive = librosa.effects.hpss(recording, margin)
    return rec_harmonic
