import deepspeech as ds
import wave
import numpy as np
import subprocess
import shlex

PATH_TO_MODEL="/home/soul/AI_Audio_Files/deepspeech-0.9.3-models.pbmm"
PATH_TO_SCORER="/home/soul/AI_Audio_Files/deepspeech-0.9.3-models.scorer"
PATH_TO_WAV="/home/soul/AI_Audio_Files/audio_files/Go_Home.wav"
#PATH_TO_WAV="/home/soul/AI_Audio_Files/audio_files/Hello_World.wav"
BASH_SCRIPT="/tmp/test.sh"

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

command_to_run =""
cmd_args = ""
# Process input
if res.find("go") != -1:
    command_to_run= "cd "
    # Special Cases (Home, temp, downloads, pictures):
    if res.find("home") != -1:
        cmd_args = "$HOME"
    elif res.find("temp") != -1:
        cmd_args = "$TMP"
    elif res.find("downloads") != -1:
        cmd_args = "$HOME/Downloads"
    elif res.find("pictures")!= -1:
        cmd_args = "$HOME/Pictures"
    else:
        print("Couldn't recognize destimation. Trying absoluate path")
        if res.find("to") != -1:
            cmd_args = res[res.find("to ")+3:]
        else:
            print("Malformed sentence. expecting Go to <destination")
            exit(-1)
elif res.find("hello world") != -1:
    command_to_run = "echo "
    cmd_args = "Hello! I understood you!"
else:
    print(f"Couldn't Understand what to do with '{res}'")
    exit(-2)

# Found command!
command_to_run = command_to_run + cmd_args


# Now I've done this in a hacky way. I create a temp bash script with the command, then run that and ensure that the child shell stays on to people can do what they want. 
# This is good for demo purposes however would have to be integrated into the shell itself. Which will be tricky. 
command_prep = "echo '#!/bin/bash\n"+command_to_run  + "\n $SHELL' > " + BASH_SCRIPT + "; chmod  -x " + BASH_SCRIPT #+ "'" + command_to_run + cmd_args+ "'"
print(f"Running {command_to_run}; type 'exit' to leave: ")

# Ensure the bash script can be executed and is created properly then actually execute it
subprocess.run(command_prep, shell=True)
subprocess.run('. /tmp/test.sh', shell=True)
