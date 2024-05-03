#!/usr/bin/env python3
from subprocess import call, Popen, PIPE
from vosk import Model, KaldiRecognizer
import pyaudio

# Load the Vosk model
model = Model("vosk-model-small-en-us-0.15")

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

# Define the command to run the process
command = ['python', 'loop.py']

# Startup sound
call("espeak \"Hello\"", shell=True)

# Run
while True:
    # Process audio chunks as they come in
    data = stream.read(4096)
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        # Here, you can parse the result and execute commands based on the recognized text
        transcript = result[14:-3]
        if transcript == startCommand and gameRunning == False:
            gameRunning = True
            proc = Popen(command, stdout=PIPE, stderr=PIPE)
        elif transcript == endGameCommand and gameRunning == True:
            gameRunning = False
            try:
                proc.kill()
            except NameError:
                pass
        else:
            pass
    else:
        pass
