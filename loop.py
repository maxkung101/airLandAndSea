#!/usr/bin/env python3
import time, random
from subprocess import call

# Memory function
def getVoice():
    voices_app = open("settings.csv", "r")
    data = []
    data_line = voices_app.readline().split(',')
    data.append(data_line)
    voices_app.close()
    return data[0][0]

# Set voice
try:
    theVoice = getVoice()
except:
    theVoice = "female2"

# Function
def randomLine():
    outputs = ["air", "land", "sea"]
    x = random.randint(0, len(outputs)-1)
    call("espeak -v " + theVoice + " \"" + outputs[x] + "\"", shell=True)

# Run
while True:
    randomLine()
    time.sleep(4)
