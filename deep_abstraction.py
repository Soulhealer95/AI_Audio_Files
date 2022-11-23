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
import Abstraction as ab

# Library imports
import deepspeech as ds
import numpy as np

# Override class functions and tailor to DeepSpeech lib
class deep_speech_abs(ab.Speech):
    def __init__(self, model, scorer, wav_path):
        # child class defines
        self.scorer = scorer
        self.model = ds.Model(model)
        if scorer != "":
            self.model.enableExternalScorer(scorer)
        self.rate = self.model.sampleRate()

        # get everything else from parent class
        super().__init__(self.model, wav_path, self.rate, np.int16)

    # Override some functions
    def speech_to_text(self):
        # get audio
        super().get_audio()

        # convert to text and reply
        return self.model.stt(self.audio)
