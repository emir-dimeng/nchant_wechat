'''

'''

from __future__ import print_function
import numpy as np

from scipy.signal import savgol_filter

def smooth(x, window_length=51, polyorder=3):
    s_x = savgol_filter(x, window_length, polyorder) # window size 51, polynomial order 3
    return s_x