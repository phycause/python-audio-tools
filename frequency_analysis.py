import numpy as np
from scipy.fftpack import fft
from scipy.signal import hamming
import matplotlib.pyplot as plt


def get_spectrum(signal, fft_size=4096, avg=True):

    if not avg:
        fft_size = int(np.shape(signal)[0])

    if np.mod(len(signal), fft_size) != 0:
        n_padding = fft_size - np.mod(len(signal), fft_size)
        signal_pad = np.pad(signal, (0, n_padding), 'constant', constant_values=(0, 0))
    else:
        signal_pad = signal

    w = hamming(fft_size)
    sum_fft_result = np.zeros(int(fft_size/2 + 1))
    n_frame = int(np.ceil(len(signal_pad)/fft_size))

    for i_frame in range(n_frame):
        signal_frame = signal_pad[i_frame * fft_size:(i_frame + 1) * fft_size]
        signal_fft = fft(signal_frame * w)
        sum_fft_result += np.abs(signal_fft)[0:int(fft_size/2) + 1]

    avg_fft_result = sum_fft_result/n_frame/fft_size

    return avg_fft_result


def plot_spectrum(signal, fs, path_savefig=None, fft_size=4096, figsize=(10,6), freqlim=None, amplim=None, unit=('log', 'dB'), avg=True):
    '''Plot the spectrum

    Args:
        signal: Monophonic audio signal
        fs: Sample rate in Hz
        fft_size: The size of fft
        path_savefig: The path to save figure. If it is not given, just show the spectrum directly.

        figsize: The figure size
        freqlim: The range of frequency to plot. Ex: To plot from 20 to 20000 Hz, freqlim is (20, 20000)
        amplim: The range of frequency to plot. Ex: To plot from -50 to -30 dB, amplim is (-50, -30)
        unit: The frequency and amplitude axis scale types.
              Options for frequency axis: {"linear", "log"}. The default is "log".
              Options for amplitude axis: {"linear", "dB"}. The default is "dB".
        avg: If the spectrum values are averaged by frames or not. The default is True.

    '''

    # Get the unit setting for frequency and amplitude axes
    frequnit = unit[0]
    ampunit = unit[1]

    # add matplot figure
    fig = plt.figure(figsize=figsize)
    ax = plt.subplot(111)

    # If avg is False set the fft_size to the signal length.
    if not avg:
        fft_size = int(np.shape(signal)[0])

    # Calculate the spectrum
    fft_result = get_spectrum(signal, fft_size, avg=avg)

    # Change the unit of frequency and amplitude axis
    if ampunit == None:
        plt.ylabel('Amplitude', fontsize=14, color='#EBEBEB')
    elif ampunit == 'dB':
        fft_result = 20 * np.log10(fft_result)
        plt.ylabel('Amplitude (dB)', fontsize=14, color='#EBEBEB')
    plt.xscale(frequnit)
    plt.xlabel('Frequency (Hz)', fontsize=14, color='#EBEBEB')

    # Plot spectrum
    f_axis = np.linspace(0.0, fs/2, fft_size//2 + 1)
    plt.plot(f_axis, fft_result, color='#1BAED8')

    # Set the range of the axes
    if freqlim is not None:
        if freqlim[0] <= 0:
            freqlim = (1, freqlim[1])
            print('Modification: The lowest frequency to show sets to 1 Hz.')
        plt.xlim(freqlim)
    if amplim is not None:
        plt.ylim(amplim)

    # Add major and minor grid
    plt.grid(b=True, which='major', color='#515A62', linestyle='-')
    plt.grid(b=True, which='minor', color='#2D3236', linestyle='-')
    plt.minorticks_on()

    # Set the color of background, ticks and spine
    ax.set_facecolor('#121619')
    fig.patch.set_facecolor('#121619')
    ax.tick_params(axis='x', colors='#EBEBEB')
    ax.tick_params(axis='y', colors='#EBEBEB')
    ax.spines['bottom'].set_color('#EBEBEB')
    ax.spines['top'].set_color('#EBEBEB') 
    ax.spines['right'].set_color('#EBEBEB')
    ax.spines['left'].set_color('#EBEBEB')
    
    plt.tight_layout()

    if path_savefig == None:
        plt.show()
    else:
        plt.savefig(path_savefig, facecolor='#121619')

    return path_savefig
