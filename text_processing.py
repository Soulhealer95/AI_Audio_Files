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
        self.command = self.__extract_cmd()
        if self.command == RETURN_ERROR:
            return SORRY_TEXT + self.speech
        elif self.command == HELLO_OUT:
            return HELLO_TEXT
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

            

