#!/usr/bin/env python3
from subprocess import call, Popen, PIPE
from vosk import Model, KaldiRecognizer
import pyaudio, time

# Memory function
def getVoice():
    voices_app = open("settings.csv", "r")
    data = []
    data_line = voices_app.readline().split(',')
    data.append(data_line)
    voices_app.close()
    return data[0][0]

# Check if memory file exists
defaultVoice = "female2"
try:
    currentVoice = getVoice()
except:
    currentVoice = defaultVoice
    f = open("settings.csv", "w")
    f.write(defaultVoice)
    f.close()

# Load the Vosk model
model = Model("path_to_your_vosk_model_directory")

# Initialize the recognizer with the model
recognizer = KaldiRecognizer(model, 16000)

# Start the microphone and process audio input
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

# Initiate variables
gameRunning = False
startCommand = "start"
endGameCommand = "stop"
changeVoiceCommand = "voice"

# Define the command to run the process
command = ['python', 'loop.py']

# Startup sound
call("espeak -v " + currentVoice + " \"Welcome\"", shell=True)

# Run
transcript = []
while True:
    # Process audio chunks as they come in.
    data = stream.read(1000)
    if recognizer.AcceptWaveform(data):
        transcript = transcript + recognizer.Result()[14:-3].split()
    else:
        transcript = transcript + recognizer.PartialResult()[14:-3].split()
    # Here, you can parse the result and execute commands based on the recognized text
    for x in transcript:
        if x == startCommand and gameRunning == False:
            gameRunning = True
            proc = Popen(command, stdout=PIPE, stderr=PIPE)
            break
        elif x == endGameCommand and gameRunning == True:
            gameRunning = False
            try:
                proc.kill()
            except NameError:
                pass
            break
        elif x == changeVoiceCommand and gameRunning == False:
            if currentVoice == defaultVoice:
                currentVoice = "male2"
                call("espeak -v " + currentVoice + " \"male\"", shell=True)
            else:
                currentVoice = defaultVoice
                call("espeak -v " + currentVoice + " \"female\"", shell=True)
            fh = open("settings.csv", "w")
            fh.write(currentVoice)
            fh.close()
            break
        elif x == changeVoiceCommand and gameRunning == True:
            try:
                proc.kill()
                call("espeak -v " + currentVoice + " \"Cannot do that yet\"", shell=True)
                time.sleep(4)
                proc = Popen(command, stdout=PIPE, stderr=PIPE)
            except NameError:
                pass
            break
        else:
            pass
    for i in transcript:
        transcript.remove(i)
