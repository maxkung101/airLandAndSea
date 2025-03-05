#!/usr/bin/env python
from subprocess import call
from vosk import Model, KaldiRecognizer
import pyaudio, threading, time, random

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

# Model loading and setup (replace with your own model path)
model_path = "path/to/your/model"
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# Audio stream setup
samplerate = 16000
blocksize = 8192

# Start the microphone and process audio input
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=samplerate, input=True, frames_per_buffer=blocksize)
stream.start_stream()

# Initiate variables
gameRunning = False
startCommand = "start"
endGameCommand = "stop"
changeVoiceCommand = "voice"
transcript = []

# Startup sound
call("espeak -v " + currentVoice + " \"Welcome\"", shell=True)

# Function 1
def randomLine():
    while True:
        if gameRunning:
            outputs = ["air", "land", "sea"]
            x = random.randint(0, len(outputs)-1)
            call("espeak -v " + currentVoice + " \"" + outputs[x] + "\"", shell=True)
            time.sleep(4)
        else:
            pass

# Function 2
def transcribeCommand():
    global gameRunning, currentVoice, transcript
    while True:
        # Process audio chunks as they come in.
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            transcript = transcript + recognizer.Result()[14:-3].split()
        else:
            transcript = transcript + recognizer.PartialResult()[14:-3].split()
        # Here, you can parse the result and execute commands based on the recognized text
        for x in transcript:
            if x == startCommand and gameRunning == False:
                gameRunning = True
                break
            elif x == endGameCommand and gameRunning == True:
                gameRunning = False
                break
            elif x == changeVoiceCommand and gameRunning == False:
                for i in transcript:
                    transcript.remove(i)
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
                for i in transcript:
                    transcript.remove(i)
                gameRunning = False
                call("espeak -v " + currentVoice + " \"Cannot do that yet\"", shell=True)
                time.sleep(2)
                gameRunning = True
                break
            else:
                pass
        for i in transcript:
            transcript.remove(i)

#Run
if __name__ == "__main__":
    threads = []
    f1 = threading.Thread(target=randomLine)
    f2 = threading.Thread(target=transcribeCommand)
    threads.append(f1)
    f1.start()
    threads.append(f2)
    f2.start()

    for t in threads:
        t.join()

    stream.stop_stream()
    stream.close()
