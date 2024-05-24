#!/usr/bin/env python3
from subprocess import call, Popen, PIPE
from vosk import Model, KaldiRecognizer
import pyaudio

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

# Define the command to run the process
command = ['python', 'loop.py']

# Startup sound
call("espeak \"Hello\"", shell=True)
transcript = []

# Run
while True:
    # Process audio chunks as they come in
    data = stream.read(4096)
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
        else:
            pass
    for i in transcript:
        transcript.remove(i)
