import numpy as np
from scipy.fftpack import fft
from scipy.signal import hamming
import matplotlib.pyplot as plt


def get_spectrum(sig, fft_size=4096, avg=True):

    if not avg:
        fft_size = int(np.shape(sig)[0])

    if np.mod(np.shape(sig)[0], fft_size) != 0:
        n_padding = fft_size - np.mod(np.shape(sig)[0], fft_size)
        sig_pad = np.pad(sig, (0, n_padding), 'constant', constant_values=(0, 0))
    else:
        sig_pad = sig

    w = hamming(fft_size)
    sum_fft_result = np.zeros(int(fft_size/2 + 1))
    n_frame = int(np.ceil(len(sig_pad)/fft_size))

    for i_frame in range(n_frame):
        sig_frame = sig_pad[i_frame * fft_size:(i_frame + 1) * fft_size]
        sig_fft = fft(sig_frame * w)
        sum_fft_result += np.abs(sig_fft)[0:int(fft_size/2) + 1]

    avg_fft_result = sum_fft_result/n_frame/fft_size

    return avg_fft_result


def plot_spectrum(sig, fs, fft_size=4096, figsize=(10, 6), freqlim=None, amplim=None, unit=('log', 'dB'), avg=True, path_savefig=None):
    '''Plot the spectrum

    Args:
        sig: Monophonic audio sig
        fs: Sample rate in Hz
        fft_size: The size of fft
        path_savefig: The path to save figure. If it is not given, just show the spectrum directly.

        figsize: The figure size
        freqlim: The range of frequency to plot. Ex: To plot from 20 to 20000 Hz, freqlim is (20, 20000)
        amplim: The range of amplitude to plot. Ex: To plot from -50 to -30 dB, amplim is (-50, -30)
        unit: The frequency and amplitude axis scale types.
              Options for frequency axis: {"linear", "log"}. The default is "log".
              Options for amplitude axis: {"linear", "dB"}. The default is "dB".
        avg: If the spectrum values are averaged by frames or not. The default is True.

    '''

    # Get the unit setting for frequency and amplitude axes
    frequnit = unit[0]
    ampunit = unit[1]

    # If avg is False set the fft_size to the sig length.
    if not avg:
        fft_size = int(np.shape(sig)[0])

    # Calculate the spectrum
    fft_result = get_spectrum(sig, fft_size, avg=avg)

    # Change the unit of frequency and amplitude axis
    if ampunit is None or ampunit == 'linear':
        ylabel = 'Amplitude'
    elif ampunit == 'dB':
        fft_result = 20 * np.log10(fft_result)
        ylabel = 'Amplitude (dB)'

    # Plot spectrum
    f_axis = np.linspace(0.0, fs/2, fft_size//2 + 1)

    # Set the range of the axes
    if freqlim is not None:
        if freqlim[0] <= 0:
            freqlim = (1, freqlim[1])
            print('Modification: The lowest frequency to show sets to 1 Hz.')

    plot_line(f_axis, fft_result, figsize, xlabel='Frequency (Hz)', ylabel=ylabel, xunit=frequnit, xlim=freqlim, ylim=amplim, path_savefig=path_savefig)

    return path_savefig

def plot_line(x, y, figsize, xlabel, ylabel, xunit, xlim=None, ylim=None, path_savefig=None):

    # add matplot figure
    fig = plt.figure(figsize=figsize)
    ax = plt.subplot(111)

    # Change the unit of x axis
    plt.xscale(xunit)

    # Set label
    plt.xlabel(xlabel, fontsize=14, color='#EBEBEB')
    plt.ylabel(ylabel, fontsize=14, color='#EBEBEB')

    # Plot
    plt.plot(x, y, color='#1BAED8')
    
    # Set limit
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)

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

    if path_savefig is None:
        plt.show()
    else:
        plt.savefig(path_savefig, facecolor='#121619')

    return path_savefig
