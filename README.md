# AI Audio

# Files
`audio_files`: dump to store audio files
main.py: Python script. Requires several libraries
	- Deepspeech (duh)
	- wave
	- numpy
	- subprocess
	- shlex
 
`main_script.sh`: Bootstrap script that should be run to setup the environment and script to work. Requires virtualenv

# Usage
- `./main_script.sh`

# Additional Info
- Currently requires audio files with commands in WAV format. 
- To make it so the script uses the audio file, edit main.py to point to your `PATH_TO_WAV`
- Also requires Model and Scorer from the following:
```
wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm
wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer
```
ref: https://deepspeech.readthedocs.io/en/r0.9/USING.html#getting-the-pre-trained-model
- Modify the `PATH_TO_MODEL` and `PATH_TO_SCORER` in main.py once downloaded

