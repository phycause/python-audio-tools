from frequency_analysis import get_spectrum, plot_line
import soundfile as sf
import numpy as np
from scipy import signal

def high_cut(sig, fs, fc):

    w = fc / (fs / 2) # Normalize the frequency
    b, a = signal.butter(1, w, 'low')
    output = signal.filtfilt(b, a, sig)

    return output

def spectrum_comparison(sig_1, sig_2, fft_size=4096):

    spec_1 = get_spectrum(sig_1, fft_size=fft_size, avg=True)
    spec_2 = get_spectrum(sig_2, fft_size=fft_size, avg=True)
    spec_1_filtered = high_cut(np.log10(spec_1), fft_size, 50)
    spec_2_filtered = high_cut(np.log10(spec_2), fft_size, 50)
    spec_cp = 20 * (spec_2_filtered - spec_1_filtered)

    return spec_cp


def plot_spectrum_comparison(sig_1, sig_2, fs, fft_size=4096, figsize=(10, 6), freqlim=None, amplim=None, unit=('log', 'dB'), avg=True, path_savefig=None):

    # Get the unit setting for frequency and amplitude axes
    frequnit = unit[0]
    ampunit = unit[1]

    spec_cp = spectrum_comparison(sig_1, sig_2, fft_size=4096)

    # Change the unit of frequency and amplitude axis
    if ampunit is None or ampunit == 'linear':
        ylabel = 'Amplitude'
    elif ampunit == 'dB':
        spec_cp = 20 * np.log10(spec_cp)
        ylabel = 'Amplitude (dB)'

    f_axis = np.linspace(0.0, fs/2, fft_size//2 + 1)

    # Set the range of the axes
    if freqlim is not None:
        if freqlim[0] <= 0:
            freqlim = (1, freqlim[1])
            print('Modification: The lowest frequency to show sets to 1 Hz.')
    
    plot_line(f_axis, spec_cp , figsize, xlabel='Frequency (Hz)', ylabel=ylabel, xunit=frequnit, xlim=freqlim, ylim=amplim, path_savefig=path_savefig)

    return path_savefig


if __name__ == "__main__":

    sig_1, fs = sf.read('../data/The_Messenger_mp3.wav')
    sig_2, fs = sf.read('../data/The_Messenger.wav')

    plot_spectrum_comparison(sig_1, sig_2, fs, fft_size=4096, figsize=(10, 6), freqlim=(20, 20000), amplim=(None, None), unit=('log', 'linear'), avg=True, path_savefig='spectrum_diff.png')