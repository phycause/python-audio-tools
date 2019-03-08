import numpy as np
from scipy.fftpack import fft
from scipy.signal import hamming
import matplotlib.pyplot as plt

def spectrum(signal, fft_size=4096):
    w = hamming(fft_size)
    n_padding = fft_size - np.mod(len(signal), fft_size)
    signal_pad = np.pad(signal, (0, n_padding), 'constant', constant_values=(0, 0))
    sum_fft_result = np.zeros(int(fft_size/2 + 1))

    n_frame = int(np.ceil(len(signal_pad)/fft_size))
    for i_frame in range(n_frame):
        signal_frame = signal_pad[i_frame * fft_size:(i_frame + 1) * fft_size]
        signal_fft = fft(signal_frame * w)
        sum_fft_result += np.abs(signal_fft)[0:int(fft_size/2) + 1]

    avg_fft_result = sum_fft_result/n_frame/fft_size
    
    return avg_fft_result
    
def plot_spectrum(signal, fs, fft_size=4096, figsize=(10,6), xlim=None, ylim=None, unit=None):
    
    plt.figure(figsize=figsize)
    
    if unit == None:
        fft_result = spectrum(signal, fft_size)
        plt.ylabel('Amplitude')
    elif unit == 'dB':
        fft_result = spectrum(signal, fft_size)
        fft_result = 20 * np.log10(fft_result)
        plt.ylabel('Amplitude (dB)')
        
    f_axis = np.linspace(0.0, fs/2, fft_size//2 + 1)
    plt.plot(f_axis, fft_result)
    plt.xlabel('Frequency (Hz)')
    if xlim != None:
        plt.xlim(xlim)
    if ylim != None:
        plt.ylim(ylim)
    plt.show()