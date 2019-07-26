import os
import subprocess


# If it converted successfully, it will return 0. In contrast, 1.

'''wav-related converter'''


def any_to_wav(path_input, path_output):
    result = os.system('ffmpeg -y -i "' + path_input + '"' + ' "' + path_output + '"')
    return result


def any_to_wav_scale(path_input, path_output, gain):
    prefix_command = 'ffmpeg -y -i "' + path_input + '"' + ' -filter:a "volume=' + str(gain) + '"'
    result = os.system(prefix_command + ' "' + path_output + '"')
    return result


def any_to_wav32(path_input, path_output):
    result = os.system('ffmpeg -y -i "' + path_input + '" -c:a pcm_f32le "' + path_output + '"')
    return result


def any_to_wav32_scale(path_input, path_output, gain):
    prefix_command = 'ffmpeg -y -i "' + path_input + '"' + ' -c:a pcm_f32le -filter:a "volume=' + str(gain) + '"'
    result = os.system(prefix_command + ' "' + path_output + '"')
    return result


''''mp3-related converter'''


def any_to_mp3(path_input, path_output, bitrate, fs=None):
    if fs is None:
        result = os.system('ffmpeg -y -i "' + path_input + '" -codec:a libmp3lame -b:a ' + str(bitrate) + 'k "' + path_output + '"')
    else:
        prefix_command = 'ffmpeg -y -i "' + path_input + '"' + ' -ar ' + str(fs)
        result = os.system(prefix_command + ' -codec:a libmp3lame -b:a ' + str(bitrate) + 'k "' + path_output + '"')
    return result


def any_to_mp3_scale(path_input, path_output, bitrate, gain, fs=None):
    if fs is None:
        prefix_command = 'ffmpeg -y -i "' + path_input + '" -filter:a "volume=' + str(gain) + '"'
        result = os.system(prefix_command + ' -codec:a libmp3lame -b:a ' + str(bitrate) + 'k "' + path_output + '"')
    else:
        prefix_command = 'ffmpeg -y -i "' + path_input + '" -filter:a "volume=' + str(gain) + '"' + ' -ar ' + str(fs)
        result = os.system(prefix_command + ' -codec:a libmp3lame -b:a ' + str(bitrate) + 'k "' + path_output + '"')
    return result


''''opus-related converter'''


def any_to_opus(path_input, path_output, bitrate):
    prefix_command = 'ffmpeg -y -i "' + path_input + '"'
    result = os.system(prefix_command + ' -acodec libopus -b:a ' + str(bitrate) + 'k "' + path_output + '"')
    return result


def any_to_opus_scale(path_input, path_output, bitrate, gain):
    prefix_command = 'ffmpeg -y -i "' + path_input + '" -filter:a "volume=' + str(gain) + '"'
    result = os.system(prefix_command + ' -acodec libopus -b:a ' + str(bitrate) + 'k "' + path_output + '"')
    return result


''''ogg-related converter'''


def any_to_ogg(path_input, path_output, bitrate, fs=None):
    if fs is None:
        prefix_command = 'ffmpeg -y -i "' + path_input
        result = os.system(prefix_command + '" -acodec libvorbis -b:a ' + str(bitrate) + 'k "' + path_output + '"')
    else:
        prefix_command = 'ffmpeg -y -i "' + path_input + '" -ar ' + str(fs)
        result = os.system(prefix_command + ' -acodec libvorbis -b:a ' + str(bitrate) + 'k "' + path_output + '"')
    return result


def any_to_ogg_scale(path_input, path_output, bitrate, gain, fs=None):
    if fs is None:
        prefix_command = 'ffmpeg -y -i "' + path_input + '" -filter:a "volume=' + str(gain) + '"'
        result = os.system(prefix_command + ' -acodec libvorbis -b:a ' + str(bitrate) + 'k "' + path_output + '"')
    else:
        prefix_command = 'ffmpeg -y -i "' + path_input + '" -filter:a "volume=' + str(gain) + '"' + ' -ar ' + str(fs)
        result = os.system(prefix_command + ' -acodec libvorbis -b:a ' + str(bitrate) + 'k "' + path_output + '"')
    return result


'''volume detection'''


def volume_info(path_source):
    command = ['ffmpeg', '-i', path_source, '-filter:a', 'volumedetect', '-f', 'null', '/dev/null']
    response = subprocess.check_output(command, stderr=subprocess.STDOUT)
    volume_info = {}
    for line in str(response).split('\\n'):
        if 'mean_volume:' in line:
            volume_info['mean_volume'] = float(line.replace('dB\\r', '').split(':')[1].replace(' ', ''))
        if 'max_volume:' in line:
            volume_info['max_volume'] = float(line.replace('dB\\r', '').split(':')[1].replace(' ', ''))

    return volume_info
