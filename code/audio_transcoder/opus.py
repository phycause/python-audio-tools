import os


def wav_to_opus(path_input, path_output, bitrate):
    result = os.system('opusenc --bitrate=' + str(bitrate) + ' "' + path_input + '" ' + '"' + path_output + '"')
    return result
