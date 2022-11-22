
__author__ = "Shivam S"
__email__ = "saxens12@mcmaster.ca"
__license__ =
 """
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
 * ARE DISCLAIMED.  IN NO EVENT SHALL Berkeley Software Design, Inc. BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
"""
import subprocess

# Defines
HELLO_TEXT = "Hello human! How're you doing? :)"
SORRY_TEXT = "I'm sorry, I couldn't understand what to do with "
RETURN_ERROR = -1
RETURN_OK = 0
HELLO_OUT = 2
BASH_SCRIPT = "/tmp/test.sh"


# Actual Class for Backend
class Text_Processing:
    def __init__(self, text):
        self.speech = text
        self.command = ""

    # Private Methods
    def __extract_cmd(self):
        if self.speech.find("go") != RETURN_ERROR:
            return self.__go()
        elif self.speech.find("hello") != RETURN_ERROR:
            return HELLO_OUT
        elif self.speech.find("copy") != RETURN_ERROR:
            return self.__copy()
        else:
            return RETURN_ERROR

    def __execute_cmd(self):
        # Lets give ourselves some clear space shall we?"
        self.command = self.__extract_cmd()
        print(f"\n\n\n===== Executing Command for '{self.speech}' ===== \n\n\n")
        if self.command == RETURN_ERROR:
            print(SORRY_TEXT + "'" + self.speech + "'")
            return
        elif self.command == HELLO_OUT:
            print(HELLO_TEXT)
            return
        else:
            # Command must be usable
            # Now I've done this in a hacky way. I create a temp bash script with the command,
            # then run that and ensure that the child shell stays on to people can do what they want.
            # This is good for demo purposes however would have to be integrated into the shell itself. Which will be tricky.
            command_prep = "echo '#!/bin/bash\n"+ self.command  + "\n $SHELL' > " + BASH_SCRIPT + "; chmod  -x " + BASH_SCRIPT
            script_location = ". " + BASH_SCRIPT
            print(f"Running {self.command} in a new shell; type 'exit' to leave: ")

            # Ensure the bash script can be executed and is created properly then actually execute it
            subprocess.run(command_prep, shell=True)
            subprocess.run(script_location, shell=True)

    def __copy(self):
        #TODO
        return "echo This is not yet supported!"

    # Method implementation to go somewhere
    def __go(self):
        res = self.speech
        cmd_args = ""
        # Special Cases (Home, temp, downloads, pictures):
        if res.find("home") != RETURN_ERROR:
            cmd_args = "$HOME"
        elif res.find("temp") != RETURN_ERROR:
            cmd_args = "$TMP"
        elif res.find("downloads") != RETURN_ERROR:
            cmd_args = "$HOME/Downloads"
        elif res.find("pictures")!= RETURN_ERROR:
            cmd_args = "$HOME/Pictures"
        else:
            print("Couldn't recognize destination. Trying absolute path")
            if res.find("to") != RETURN_ERROR:
                cmd_args = res[res.find("to ")+3:]
            else:
                print("Malformed sentence. expecting Go to <destination>")
                return RETURN_ERROR
        return "cd " + cmd_args


    # Public Methods
    def execute(self):
        self.__execute_cmd()
        return
