import numpy as np
import matplotlib.pyplot as plt


def plot_waveform(sig, fs, path_savefig=None, figsize=(10, 6), tlim=None, amplim=(-1, 1)):
    '''Plot the waveform

    Args:
        sig: Monophonic audio sig
        fs: Sample rate in Hz
        path_savefig: The path to save figure. If it is not given, just show the waveform directly.

        figsize: The figure size
        tlim: The range of time to plot. Ex: To plot from 0 to 5 seconds, freqlim is (0, 5)
        amplim: The range of amplitude to plot. Ex: To plot from -0.5 to 0.5, amplim is (-0.5, 0.5). The default is (-1, 1).

    '''

    # add matplot figure
    fig = plt.figure(figsize=figsize)
    ax = plt.subplot(111)

    t_axis = np.linspace(0.0, np.shape(sig)[0]/fs, np.shape(sig)[0])
    plt.plot(t_axis, sig, color='#1BAED8')

    plt.xlabel('Time (s)', fontsize=14, color='#EBEBEB')
    plt.ylabel('Amplitude', fontsize=14, color='#EBEBEB')

    if tlim is not None:
        if tlim[0] < 0:
            tlim = (0, tlim[1])
            print('Modification: The start time is modified to 0.')
        plt.xlim(tlim)
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

    if path_savefig is None:
        plt.show()
    else:
        plt.savefig(path_savefig, facecolor='#121619')

    return path_savefig
