import soundfile as sf
from frequency_analysis import plot_spectrum

x, fs = sf.read('The_Messenger_L.wav')
plot_spectrum(x, fs, fft_size=4096, figsize=(10,6), freqlim=(20, 20000), amplim=(-115, -25), unit=('log', 'dB'), avg=True)
