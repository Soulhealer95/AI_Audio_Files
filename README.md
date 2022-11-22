# AI Audio
- Attempt on Speech Recognition Software for UNIX based systems 
- Currently uses Python library called DeepSpeech
- Application has been written to follow a standard API for speech recognition and processing
- Requires several libraries
	- Deepspeech (duh)
	- wave
	- numpy
	- subprocess
	- shlex
- requires sox to be installed on the system
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
- `./start_deep.sh`

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

