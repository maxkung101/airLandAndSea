#!/usr/bin/env python3
import time, pygame, random, os
import speech_recognition as sr

sounds = pygame.mixer
sounds.init()

directory = "wav/"

shuffle = "shuffle/"
response = "response/"

alreadyPaused = "alreadyPaused.wav"
alreadyRunning = "alreadyRunning.wav"
cannotDoThatDuringGame = "cannotDoThatDuringGame.wav"
cannotDoThatYet = "cannotDoThatYet.wav"
endingGame = "endingGame.wav"
fastest = "fastest.wav"
invalid = "invalid.wav"
oneOrTwoWords = "oneOrTwoWords.wav"
paused = "paused.wav"
poweringOn = "poweringOn.wav"
resuming = "resuming.wav"
shutDown = "shutDown.wav"
slowest = "slowest.wav"
startingGame = "startingGame.wav"

sAlreadyPaused = sounds.Sound(directory + response + alreadyPaused)                    # Game is already paused
sAlreadyRunning = sounds.Sound(directory + response + alreadyRunning)                  # Game is already running
sCannotDoThatDuringGame = sounds.Sound(directory + response + cannotDoThatDuringGame)  # Cannot do that during game
sCannotDoThatYet = sounds.Sound(directory + response + cannotDoThatYet)                # Cannot do that yet
sEndingGame = sounds.Sound(directory + response + endingGame)                          # Ending the game
sInvalid = sounds.Sound(directory + response + invalid)                                # Command is not valid
sOneOrTwoWords = sounds.Sound(directory + response + oneOrTwoWords)                    # Use one or two words only
sPaused = sounds.Sound(directory + response + paused)                                  # Paused
sPowerOn = sounds.Sound(directory + response + poweringOn)                             # Powering on
sResuming = sounds.Sound(directory + response + resuming)                              # Resuming
sShutDown = sounds.Sound(directory + response + shutDown)                              # Shutting down
sStartingGame = sounds.Sound(directory + response + startingGame)                      # Starting game

female = []
femaleDirectory = os.fsencode(directory + shuffle)
for file in os.listdir(os.fsencode(femaleDirectory)):
     filename = os.fsdecode(file)
     if filename.endswith(".wav"):
         female.append(sounds.Sound(directory + shuffle + filename))
         continue
     else:
         continue

gameRunning = False
gamePaused = False
powerFunctioning = True

shutDownCommand = "shut down"
startCommand = "start"
pauseCommand = "pause"
resumeCommand = "resume"
endGameCommand = "stop"
fasterCommand = "faster"
slowerCommand = "slower"

def randomLine():
    x = random.randint(0, len(female)-1)
    female[x].play()
    time.sleep(female[x].get_length())

def playback(spokenLine):
    spokenLine.play()
    time.sleep(spokenLine.get_length())

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
        sOneOrTwoWords.play()
        time.sleep(sOneOrTwoWords.get_length())
        recognize_microphone()
    else:
        if transcript == shutDownCommand:
            if gameRunning:
                playback(sCannotDoThatDuringGame)
            else:
                powerFunctioning = False
                playback(sShutDown)
        elif transcript == startCommand:
            if gameRunning:
                playback(sAlreadyRunning)
            else:
                gameRunning = True
                playback(sStartingGame)
        elif transcript == endGameCommand:
            if gameRunning:
                gameRunning = False
                playback(sEndingGame)
            else:
                playback(sCannotDoThatYet)
        elif transcript == pauseCommand:
            if gameRunning:
                if gamePaused:
                    playback(sAlreadyPaused)
                else:
                    gamePaused = True
                    playback(sPaused)
            else:
                playback(sCannotDoThatYet)
        elif transcript == resumeCommand:
            if gameRunning:
                if gamePaused:
                    gamePaused = False
                    playback(sResuming)
                else:
                    playback(sCannotDoThatYet)
            else:
                playback(sCannotDoThatYet)
        else:
            if powerFunctioning:
                playback(sInvalid)
            else:
                pass

        if powerFunctioning:
            recognize_microphone()
        else:
            pass

playback(sPowerOn)
recognize_microphone()
