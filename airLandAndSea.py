#!/usr/bin/env python3
import random
import speech_recognition as sr
from subprocess import call

outputs = ["air", "land", "sea"]

gameRunning = False
gamePaused = False
powerFunctioning = True

shutDownCommand = "shut down"
startCommand = "start"
pauseCommand = "pause"
resumeCommand = "resume"
endGameCommand = "stop"

def randomLine():
    x = random.randint(0, len(outputs)-1)
    call("espeak \"" + outputs[x] + "\"", shell=True)

def recognize_microphone():
    global gameRunning
    global gamePaused
    global powerFunctioning
    transcript = ""
    r = sr.Recognizer()

    if gameRunning:
        if gamePaused:
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)
        else:
            randomLine()
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source, timeout=4)
    else:
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

    try:
        transcript = r.recognize_google(audio)
        print("You said, \"" + transcript + ".\"")
    except:
        recognize_microphone()

    if len(transcript.split()) > 2:
        call("espeak \"Use one or two words only.\"", shell=True)
        recognize_microphone()
    else:
        if transcript == shutDownCommand:
            if gameRunning:
                call("espeak \"Cannot do that during the game\"", shell=True)
            else:
                powerFunctioning = False
                call("espeak \"Good bye\"", shell=True)
        elif transcript == startCommand:
            if gameRunning:
                call("espeak \"Game is already running\"", shell=True)
            else:
                gameRunning = True
                call("espeak \"Starting the game\"", shell=True)
        elif transcript == endGameCommand:
            if gameRunning:
                gameRunning = False
                call("espeak \"Game end\"", shell=True)
            else:
                call("espeak \"Cannot do that yet\"", shell=True)
        elif transcript == pauseCommand:
            if gameRunning:
                if gamePaused:
                    call("espeak \"Game is already paused\"", shell=True)
                else:
                    gamePaused = True
                    call("espeak \"Paused\"", shell=True)
            else:
                call("espeak \"Cannot do that yet\"", shell=True)
        elif transcript == resumeCommand:
            if gameRunning:
                if gamePaused:
                    gamePaused = False
                    call("espeak \"Resuming\"", shell=True)
                else:
                    call("espeak \"Cannot do that yet\"", shell=True)
            else:
                call("espeak \"Cannot do that yet\"", shell=True)
        else:
            if powerFunctioning:
                call("espeak \"Unknown command\"", shell=True)
            else:
                pass

        if powerFunctioning:
            recognize_microphone()
        else:
            pass

call("espeak \"Hello\"", shell=True)
recognize_microphone()
