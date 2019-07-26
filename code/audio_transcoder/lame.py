import os


def wav_to_mp3(path_input, path_output, bitrate, fs=None, lowpass=None):
    if fs is None:
        result = os.system('lame -q0 -b' + str(bitrate) + ' "' + path_input + '" ' + '"' + path_output + '"')
    else:
        print('Resample to ', fs, 'kHz')
        prefix_command = 'lame -q0 -b' + str(bitrate) + ' --resample ' + str(fs) + ' --lowpass ' + str(lowpass)
        result = os.system(prefix_command + ' "' + path_input + '" ' + '"' + path_output + '"')
    return result


def wav_to_mp3_scale(path_input, path_output, bitrate, gain, fs=None, lowpass=None):
    if fs is None:
        prefix_command = 'lame -q0 -b' + str(bitrate) + ' --scale ' + str(gain)
        result = os.system(prefix_command + ' "' + path_input + '" ' + '"' + path_output + '"')
    else:
        print('Resample to ', fs, 'kHz')
        prefix_command = 'lame -q0 -b' + str(bitrate) + ' --scale ' + str(gain) + ' --resample ' + str(fs) + ' --lowpass ' + str(lowpass)
        print(prefix_command)
        result = os.system(prefix_command + ' "' + path_input + '" ' + '"' + path_output + '"')
    return result
