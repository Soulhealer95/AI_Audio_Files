__author__ = "Shivam S"
__email__ = "saxens12@mcmaster.ca"
__license__ = """

 * Copyright (c) 2022
 *	Shivam S.  All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * THIS SOFTWARE IS PROVIDED BY saxens12@mcmaster.ca. ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL saxens12@mcmaster.ca BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
"""

import wave
import subprocess
import shlex
import numpy as np

# Class for basic Speech to Text
# Should allow for use with any library
# SuperClass for Frontend
# Class           Speech 
# Desc:
# Class that contains basic APIs for any libraries to use
# The expectation is that any library being used will override the methods provided in this superclass
# All clients can then be provided the methods in this API for documentation to connect
# Most of these methods should be skeletons
# function
# Args:
# @model     ptr    pointer to model created by library
# @sample    ptr    pointer to audio file (wav format)
# @rate      int    sample rate of audio
# @size      int    size of audio output (np.intX format)
class Speech:
    def __init__(self, model, sample, rate, size):
        self.sample_wav = sample
        self.model = model
        self.rate = rate
        self.size = size
        self.audio = ""
        self.text = ""

    def __init_model(self):
        #TODO
        # Set up model with whatever is needed
        return

    # From DeepSpeech sample code to use sox
    # Converts sample rate to 16 bit signed int numpy array
    # 16kHz default. would have to change this for other models perhaps
    def __convert_samplerate(self):
        sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate {} --encoding signed-integer --endian little --compression 0.0 --no-dither - '.format(self.sample_wav, self.rate)
        try:
            output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
        except OSError as e:
            raise OSError(e.errno, 'SoX not found, use {}hz files or install it: {}'.format(self.rate, e.strerror))

        return self.rate, np.frombuffer(output, self.size)

    # Use Wave to get the audio as array convert if needed
    def get_audio(self):
        # Get Audio Sample from self.sample
        audio_file = wave.open(self.sample_wav, 'rb')
        file_rate = audio_file.getframerate()
        # Convert to rate if needed
        if file_rate != self.rate:
            file_rate_new, self.audio = self.__convert_samplerate()
        else:
            self.audio = np.frombuffer(audio_file.readframes(audio_file.getnframes()), self.size)
        # Returned audio in self.audio
        audio_file.close()
        return

    def train_text(self, cue):
        #TODO
        # Get audio from self.sample
        # Run inference using lib functions
        # Print results of training
        # Return if needed
        return

    def speech_to_text(self):
        #TODO
        # Using library, convert audio to text
        # Return output string
        return self.text
