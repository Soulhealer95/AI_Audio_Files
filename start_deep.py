import deepspeech as ds
import wave
import numpy as np
import shlex
import os
import text_processing as tp
import subprocess

# Work from Project Dir
cur_dir = os.getcwd()

PATH_TO_MODEL=cur_dir + "/deepspeech-0.9.3-models.pbmm"
PATH_TO_SCORER=cur_dir + "/deepspeech-0.9.3-models.scorer"
PATH_TO_WAV=cur_dir + "/audio_files/Go_Home.wav"

# Ported from library source
def convert_samplerate(audio_path, desired_sample_rate):
    sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate {} --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(audio_path, desired_sample_rate)
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno, 'SoX not found, use {}hz files or install it: {}'.format(desired_sample_rate, e.strerror))

    return desired_sample_rate, np.frombuffer(output, np.int16)

# Initialize the Model
model_file = ds.Model(PATH_TO_MODEL)
model_file.enableExternalScorer(PATH_TO_SCORER)
required_sample_rate = model_file.sampleRate()

# Get Audio File
file = wave.open(PATH_TO_WAV, 'rb')
file_fr = file.getframerate()
if file_fr != required_sample_rate:
    fs_new, audio = convert_samplerate(PATH_TO_WAV, required_sample_rate)
else:
    audio = np.frombuffer(file.readframes(file.getnframes()), np.int16)
file.close()

# Get text from Audio
res = model_file.stt(audio)
print("You Said: " + res)

# Create new class and execute
post_pr = tp.Text_Processing(res)
post_pr.execute()
