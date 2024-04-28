#!/usr/bin/env python3
import random, subprocess
from subprocess import call

# Initiate
gameRunning = False
startCommand = "start"
endGameCommand = "stop"

# Function
def randomLine():
    outputs = ["air", "land", "sea"]
    x = random.randint(0, len(outputs)-1)
    call("espeak \"" + outputs[x] + "\"", shell=True)

# Define the command to run the Vosk process
command = ['python', 'voiceCommand.py']

# Startup sound
call("espeak \"Hello\"", shell=True)

# Run
while True:
    if gameRunning:
        randomLine()
    else:
        pass
    transcript = ""
    try:
        # Run the command with a timeout of 4 seconds
        result = subprocess.run(command, capture_output=True, text=True, timeout=4)
        transcript = result.stdout
        if transcript == startCommand:
            gameRunning = True
        elif transcript == endGameCommand:
            gameRunning = False
        else:
            pass
    except subprocess.TimeoutExpired:
        pass
