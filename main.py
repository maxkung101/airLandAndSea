#!/usr/bin/env python3
import random
import speech_recognition as sr
from subprocess import call

gameRunning = False
startCommand = "start"
endGameCommand = "stop"

def randomLine():
    outputs = ["air", "land", "sea"]
    x = random.randint(0, len(outputs)-1)
    call("espeak \"" + outputs[x] + "\"", shell=True)

call("espeak \"Hello\"", shell=True)

while True:
    if gameRunning:
        randomLine()
    else:
        pass
    transcript = ""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #adjust for ambient noise
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=4)
    	try:
            transcript = r.recognize_google(audio)
            if transcript == startCommand:
                gameRunning = True
            elif transcript == endGameCommand:
                gameRunning = False
            else:
                pass
    	except:
            pass
