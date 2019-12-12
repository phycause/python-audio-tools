import soundfile as sf
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os


def update_line(num, line, list_x_val, y_min, y_max):
    i = list_x_val[num]
    line.set_data( [i, i], [y_min, y_max])
    return line, 

def animate_audio_spectrogram(path_audio, output_name=None, fps=15, duration=None, freqscale='linear'):

    # Retrieve the directory and the name of the audio file
    dir_audio = os.path.dirname(path_audio)
    filename = os.path.splitext(os.path.basename(path_audio))[0]

    # Define the output name if it is not given.
    if output_name is None:
        output_name = filename + '_show'

    # Read the audio signal
    sig, fs = sf.read(path_audio)

    # If the audio is multichannel, then just take the first channel.
    if len(sig.shape) > 1: 
        x = sig[:, 0]
    else:
        x = sig

    # Define the duration to the full range of the audio if it is not given.
    if duration is None:
        duration = (0, len(x) / fs)

    # Calculate the spectrogram with the range of audio signal
    x_min_sample = int(duration[0] * fs)
    x_max_sample = int(duration[1] * fs)

    x = x[x_min_sample:x_max_sample]
    f, t, Sxx = signal.spectrogram(x, fs, window=('hamming'), nfft=4096)

    # Deal with the zero problem
    temp_sxx = Sxx.copy()
    temp_sxx[temp_sxx == 0] = 10**100
    Sxx[Sxx == 0] = np.min(temp_sxx)

    # Plot the spectrogram
    x_min = 0 # in sec
    x_max = duration[1] - duration[0]
    y_min = 0
    y_max = int(fs/2)
    list_x_val = np.linspace(x_min, x_max, x_max * fps) # possible x values for the line

    print('Draw the spectrogram')
    fig = plt.figure(figsize=(16, 9))
    plt.pcolormesh(t, f, np.log(Sxx))

    l , _ = plt.plot(-6, -1, 6, 1, linewidth=2, color= 'red')

    if freqscale == 'log':
        y_min = 1
        plt.yscale("log")

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (sec)')
    plt.title('Dynamic show audio')
    plt.tight_layout()

    # Animate the red line and save the video
    print('Animate the moving line')
    line_anim = animation.FuncAnimation(fig, update_line, frames=len(list_x_val), interval=1, fargs=(l, list_x_val, y_min, y_max,))

    path_video_only = os.path.join(dir_audio, output_name + '_video.mp4')
    line_anim.save(path_video_only, fps=fps, dpi=300, extra_args=['-vcodec', 'libx264'])

    # Combine video with audio
    if os.system('ffmpeg -version'):
        raise 'FFMPEG is not installed correctly.'

    if len(sig.shape) > 1:
        x_stereo = sig[x_min_sample:x_max_sample]
    else:
        x_stereo = np.array([x, x]).T # If the audio is mono, then make a stereo version for combine with video.

    sf.write('temp_stereo.wav', x_stereo, fs)
    path_output_audio = 'temp_stereo.wav'
    path_output_video = os.path.join(dir_audio, output_name + '.mp4')
    os.system('ffmpeg -y -i "' + path_video_only + 
    '" -i "' + path_output_audio + '" -c:v copy -c:a aac -strict experimental "' + path_output_video + '"')

    # Clean the temporary files
    if os.path.exists('temp_stereo.wav'):
        os.remove('temp_stereo.wav')
    if os.path.exists(path_video_only):
        os.remove(path_video_only)
