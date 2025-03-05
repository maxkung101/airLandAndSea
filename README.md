# Air Land Sea Assistant
Software for raspberry pi to moderate air land and sea

## Setup and Installation
### Requirements
* Audio input
* Audio output

### Install your dependencies
Make sure you have espeak installed on your raspberry pi.
```
$ sudo apt install -y espeak
```
You will also need to download a vosk model: [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models).

### Download source code
Type in the following command in your raspberry pi terminal.
```
$ gh repo clone maxkung101/airLandAndSea
```

### Install python libraries
Use the following raspberry pi terminal commands.
```
$ cd airLandAndSea/
$ pip install -r requirements.txt
$ cd ../
```

## How to use
### Run software
To run, type in the following commands.
```
$ cd airLandAndSea/
$ python main.py
```

## About
### Credits
Programmed by Max Kung