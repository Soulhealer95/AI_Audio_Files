# POSIX SPEECH RECOGNITION
- Attempt on Speech Recognition Software for UNIX based systems 
- Currently uses Python library called DeepSpeech
- Application has been written to follow a standard API for speech recognition and processing
- Requires several libraries
	- Deepspeech (duh)
	- wave
	- numpy
	- subprocess
	- shlex
- requires sox and arecord to be installed on the system
- Python3.8 has been tested on an `x86_64` VM.
- Tested with Ubuntu 20.04
 
# Files
- `audio_files`: dump to store audio files
- `text_processing.py`: Backend processing of text once speech has been converted
- `Abstraction.py`: Parent class which provides basic wav to audio buffer conversion and other general API functions
- `deep_abstraction.py`: Child class which conforms DeepSpeech library to the standard API for use by application 
- `start_deep.py`: Python script application you must use to pass paths depending on what library is needed
- `start_script.sh`: Bootstrap script that should be run to setup the environment and script to work. Requires virtualenv

# Usage
- `./start_script.sh [relative path to audio wav file]`
If no file is provided, it will try to listen for an audio for 5 seconds
- example:
```
~/projects/AI_Audio_Files$ ./start_script.sh audio_files/Go_Home.wav 
==========Welcome to the Bootstrap for this Speech Recognition Software===========
******* Commands understood *******
go home/ 'to <destination>'
hello world
More commands will be added soon.....

==================Initializing Environment===================
created virtual environment CPython3.8.10.final.0-64 in 107ms
  creator CPython3Posix(dest=/home/shisaxena/tmp/deepspeech-venv, clear=False, global=False)
  seeder FromAppData(download=False, pip=latest, setuptools=latest, wheel=latest, pkg_resources=latest, via=copy, app_data_dir=/home/shisaxena/.local/share/virtualenv/seed-app-data/v1.0.1.debian.1)
  activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator
=====Done!=======
Starting Program...

TensorFlow: v2.3.0-6-g23ad988
DeepSpeech: v0.9.3-0-gf2e9c85
2022-11-22 12:35:27.769249: I tensorflow/core/platform/cpu_feature_guard.cc:142] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN)to use the following CPU instructions in performance-critical operations:  AVX2 FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.



===== Executing Command for 'go home' ===== 



Running cd $HOME in a new shell; type 'exit' to leave: 
~$ 
```

# Additional Info
- Currently requires audio files with commands in WAV format. 
- To make it so the script uses the audio file, edit `start_deep.py` to point to your `PATH_TO_WAV`
- Also requires Model and Scorer from the following:
```
wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm
wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer
```
ref: https://deepspeech.readthedocs.io/en/r0.9/USING.html#getting-the-pre-trained-model
- Modify the `PATH_TO_MODEL` and `PATH_TO_SCORER` in main.py once downloaded

