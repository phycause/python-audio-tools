import soundfile as sf
import numpy as np
from frequency_analysis import plot_spectrum
from waveform_display import plot_waveform
from animate_display import animate_audio_spectrogram

# ============================= #
x, fs = sf.read('../data/The_Messenger.wav')

if len(np.shape(x)) > 1:
    x = x[:, 0]
    print('Now support only monophonic audio file. It shows the first channel.')

# Plot waveform
plot_waveform(x, fs, figsize=(10, 6), tlim=(0, 20), amplim=(-1, 1))

# Plot spectrum
plot_spectrum(x, fs, fft_size=4096, figsize=(10, 6), freqlim=(20, 20000), amplim=(-115, -25), unit=('log', 'dB'), avg=True)

# ============================= #
# Animation demonstration of audio spectrogram
fps=15
duration = (0, 8)
path_audio = '../data/The_Messenger_stereo.wav'
animate_audio_spectrogram(path_audio, 'Demo', fps=fps, duration=duration, freqscale='log')
