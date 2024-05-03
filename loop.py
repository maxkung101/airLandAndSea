#!/usr/bin/env python3
import time, random
from subprocess import call

# Function
def randomLine():
    outputs = ["air", "land", "sea"]
    x = random.randint(0, len(outputs)-1)
    call("espeak \"" + outputs[x] + "\"", shell=True)

# Run
while True:
    randomLine()
    time.sleep(4)
