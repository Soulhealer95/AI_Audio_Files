__author__= "Shivam S"
__email__= "saxens12@mcmaster.ca"
__license__="""
 
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
# Use DeepSpeech
import deep_abstraction as deep
# Use General Text Processing Class
import text_processing as tp

# Other system libs
import os,sys


# Work from Project Dir
cur_dir = os.getcwd()

# DeepSpeech Specific Things
PATH_TO_MODEL=cur_dir + "/deepspeech-0.9.3-models.pbmm"
PATH_TO_SCORER=cur_dir + "/deepspeech-0.9.3-models.scorer"

# Get this from commandline
if len(sys.argv) != 1:
    PATH_TO_WAV= cur_dir + "/" + sys.argv[1]

# Initialize the Model and get the text from voice
deep_model = deep.deep_speech_abs(PATH_TO_MODEL,PATH_TO_SCORER, PATH_TO_WAV)
result = deep_model.speech_to_text()

# Create new class and execute command
post_pr = tp.Text_Processing(result)
post_pr.execute()
