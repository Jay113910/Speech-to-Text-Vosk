# Speech2Text_Vosk
A real time speech recognition using microphone based on [Vosk](https://alphacephei.com/vosk/) speech recognition open source toolkit.

## How to use
1. Install the necessary libaries. ([Vosk](https://alphacephei.com/vosk/install), [SpeechRecognition ](https://alphacephei.com/vosk/install), [PyAudio](https://pypi.org/project/PyAudio/)... )
2. Download the models from [Vosk models](https://alphacephei.com/vosk/models).
3. Arrange your project directory structure like this:
```
Project
│   vosk_microphone_speech2text
│
└───Models
│       vosk-model-small-en-us-0.15
|       vosk-model-en-us-0.22-lgraph
│       ...
|
└───Recording
```
4. Start the program (test on cmd)
![start image](imgs/start.png)
5. Press Ctrl starting record the sound 
![listening image](imgs/listening.png)
6. Recognize the sound
![recognition image](imgs/recognition.png)
7. Plot the time domain and frequency domain of the recorded sound
![plot_time_frequency image](imgs/plot_time_frequency.png)
