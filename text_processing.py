
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
import subprocess, os

# Defines
HELLO_TEXT = "Hello human! How're you doing? :)"
SORRY_TEXT = "I'm sorry, I couldn't understand what to do with "
RETURN_ERROR = -1
RETURN_OK = 0
HELLO_OUT = 2
BASH_SCRIPT = "/tmp/test.sh"


# Actual Class for Backend
# Class            Text_Processing
# Desc:
# Class that contains methods to perform an action once you have a text from user
# function
# Args:
# @text     str    String of text
class Text_Processing:
    def __init__(self, text):
        self.speech = text
        self.original = self.speech
        self.command = ""

    # Method  (Private) __extract_cmd 
    # Desc:
    # Converts text to a UNIX command for program to execute at the end
    # Args:
    # N/A
    # Returns:
    # @command  str  string output from one of the other methods or -1 on error
    def __extract_cmd(self):
        space_index = self.speech.find(" ")
        command = self.speech[:space_index]
        rest = self.speech[space_index+1:]
        print("checking " + command)

        # A better system I think. 
        # replaces the malformed variations into command that we understand manually
        # Open
        if command in ["open", "play", "edit"]:
            command =  "open"
        # Copy
        elif command in ["cope", "copy"]:
            command =  "copy"
        # Go 
        elif command in ["go"]:
            command = "go"
        # Move something
        elif command in ["move"]:
            command = "move" 
        # Greetings
        elif command in ["hi", "hello", "hey"]:
           return HELLO_OUT 
        # Couldn't find it!
        else:
            return RETURN_ERROR

        # All functions have been named after the command they execute
        # This means we can form the function from the command itself 
        # example go would be self.go()
        # only catch is that these methods now have to be public
        # As an aside: those functions get the value of speech from self.speech. 
        # so we'll edit self.speech to be our interpretation of the actual speech :)
        self.speech = command +" "+ rest
        output = getattr(self,command)
        return output()

    # Method  (Private) __execute_cmd 
    # Desc:
    # Actually execute a proper Linux command using a shell script
    # Command must be usable
    # Now I've done this in a hacky way. I create a temp bash script with the command,
    # then run that and ensure that the child shell stays on to people can do what they want.
    # This is good for demo purposes however would have to be integrated into the shell itself.
    # The best way to do that would be to make this program the pty and then it would be a man in the middle
    # and check all inputs and execute them
    # Args:
    # N/A
    # Returns:
    # @command  str  string output from one of the other methods
    def __execute_cmd(self):
        # get command and handle special cases appropriately
        self.command = self.__extract_cmd()
        print(f"\n===== Executing Command for '{self.original}' ===== \n")
        if self.command == RETURN_ERROR:
            print(SORRY_TEXT + "'" + self.speech + "'")
            return
        elif self.command == HELLO_OUT:
            print(HELLO_TEXT)
            return
        else:
            # Create bash script and then execute it from a fixed location
            command_prep = "echo '#!/bin/bash\n"+ self.command  + "\n $SHELL' > " + BASH_SCRIPT + "; chmod  -x " + BASH_SCRIPT
            script_location = ". " + BASH_SCRIPT
            print(f"Running {self.command} in a new shell; type 'exit' to leave: ")

            # Ensure the bash script can be executed and is created properly then actually execute it
            subprocess.run(command_prep, shell=True)
            subprocess.run(script_location, shell=True)

    # Method  (Private) __common_dest
    # Desc:
    # Given location, return a path of commonly known locations
    # Special Cases (Home, temp, downloads, pictures)
    # Args:
    # @loc      str  abbreviations to translate
    # Returns:
    # @cmd_args  str  string output of translated path
    def __common_dest(self, loc):
        cmd_args = ""
        if loc.find("home") != RETURN_ERROR:
            cmd_args = "$HOME"
        elif loc.find("temp") != RETURN_ERROR:
            cmd_args = "$TMP"
        elif loc.find("download") != RETURN_ERROR:
            cmd_args = "$HOME/Downloads"
        elif loc.find("pictures")!= RETURN_ERROR:
            cmd_args = "$HOME/Pictures"
        else:
            return RETURN_ERROR
        return cmd_args

    # Method  (Public) move 
    # Desc:
    # Creates a move or copy command 
    # expect format `move x to y`. so the first argument would be after the first space and just before the first and only 'to'
    # If path is recognized, use that or use the argment as absolute path
    # Args:
    # @copy_instead     bool  if true, change command to copy
    # Returns:
    # @cmd_args  str  string output of command to execute
    def move(self, copy_instead):
        cmd = "mv "
        to_index = self.speech.find(" to ")
        if to_index == RETURN_ERROR:
            print("Malformed sentence. expecting move <src> to <destination>")
            return RETURN_ERROR
        # Check format
        arg1 = self.speech[self.speech.find(" ")+1:to_index]
        arg2 = self.speech[to_index+4:]
        dest = self.__common_dest(arg2)
        if dest == RETURN_ERROR:
            print("Couldn't recognize destination. Trying as absolute path")
            dest = arg2
        if copy_instead == 1:
            cmd = "cp "
        return cmd + arg1 + " " + dest

    # Method  (Public) copy
    # Desc:
    # Wrapper for move command with copy enabled
    # Args:
    # N/A
    # Returns:
    # @cmd_args  str  string output of command to execute
    def copy(self):
        return self.move(1)


    # Method  (Public) open 
    # Desc:
    # Creates a command to open most extensions of files
    # expect a format `open <filename>` 
    # Args:
    # N/A
    # Returns:
    #  str  string output of command to execute
    def open(self):
        # Get a file name (without extension)
        arg = self.speech[self.speech.find("open ")+5:]
        curr_dir = os.getcwd()
        file_to_open = ""

        # Find a file with that name in current directory
        for root, dirs, files in os.walk(curr_dir):
            for name in files:
                # return the first file found with that arg name
                if name.find(arg) != RETURN_ERROR:
                    file_to_open = curr_dir + "/" + name
                    break
        if file_to_open == "":
            return RETURN_ERROR
        else:
            print("Trying to open " + file_to_open)
            return "xdg-open " + file_to_open

    # Method  (Public) go 
    # Desc:
    # Creates a command to visit a location
    # expect a format `go to <location>` 
    # Args:
    # N/A
    # Returns:
    #  str  string output of command to execute
    def go(self):
        res = self.speech
        cmd_args = self.__common_dest(res)
        if cmd_args != RETURN_ERROR:
            return "cd " + cmd_args
        else:
            print("Couldn't recognize destination. Trying absolute path")
            if res.find("to") != RETURN_ERROR:
                return "cd " + res[res.find("to ")+3:]
            else:
                print("Malformed sentence. expecting Go to <destination>")
                return RETURN_ERROR

    # Method  (Public) execute 
    # Desc:
    # Wrapper for the private execute_cmd method
    # Args:
    # N/A
    # Returns:
    # N/A
    def execute(self):
        self.__execute_cmd()
        return
