import subprocess

# Define the command to run the Vosk process
vosk_command = ['python', 'voskInput.py']

# Start the Vosk process
vosk_process = subprocess.Popen(vosk_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

# Print the Vosk output in real-time
while True:
    output = vosk_process.stdout.readline()
    if output == '' and vosk_process.poll() is not None:
        break
    if output:
        print(output.strip())
