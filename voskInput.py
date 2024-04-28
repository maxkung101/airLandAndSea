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

# Process audio chunks as they come in
hearing = True
while hearing:
    data = stream.read(4096)
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        # Here, you can parse the result and execute commands based on the recognized text
        print(result[14:-3])
        hearing = False
    else:
        pass
