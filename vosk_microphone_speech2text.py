# this .py file must at the same directory of model folder
# part of code from https://tech-en.netlify.app/articles/en529590/index.html

import os
import vosk
import wave
import time
import json
import keyboard
import numpy as np
import speech_recognition as sr
import matplotlib.pyplot as plt


def Speech2Text(filename, model):
    print("\nRecognizing...\n")    
    
    wf = wave.open(filename, "rb")
    # check wheather the file is wav format or not
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)

    vosk_recognizer = vosk.KaldiRecognizer(model, wf.getframerate())
    vosk_recognizer.SetWords(True)

    text_lst =[]
    p_text_lst = []
    p_str = []
    len_p_str = []
    while True:
        data = wf.readframes(wf.getframerate())
        if len(data) == 0:
            break
        if vosk_recognizer.AcceptWaveform(data):
            text_lst.append(vosk_recognizer.Result())
            #print(vosk_recognizer.Result())
        else:
            p_text_lst.append(vosk_recognizer.PartialResult())
            #print(vosk_recognizer.PartialResult())

    if len(text_lst) !=0:
        jd = json.loads(text_lst[0])
        txt_str = jd["text"]
        
    elif len(p_text_lst) !=0: 
        for i in range(0,len(p_text_lst)):
            temp_txt_dict = json.loads(p_text_lst[i])
            p_str.append(temp_txt_dict['partial'])
       
        len_p_str = [len(p_str[j]) for j in range(0,len(p_str))]
        max_val = max(len_p_str)
        indx = len_p_str.index(max_val)
        txt_str = p_str[indx]
            
    else:
        txt_str = ""
        
    if txt_str == "":
        return "Vosk recognition could not understand audio."
    else:
        return txt_str

def RecordAudio(wav_output_path):  
    # =============================================================================
    # Recording audio from microphone that based on speech_recognition libary
    # =============================================================================
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        # first 2 second for adjust the noise
        #recognizer.adjust_for_ambient_noise(source, 2)
        
        #  dynamic_energy_threshold = True represents approximately the fraction of the current energy 
        #  threshold that is retained after one second of dynamic threshold adjustment
        recognizer.dynamic_energy_threshold = True
        print("\nListening...", end = '')
        audio = recognizer.listen(source)
    
    # write recorded audio
    with open(wav_output_path, "wb") as file:
        file.write(audio.get_wav_data())
        
    print("Finished!")
    print("%s is saved."%(wav_output_path.split("\\")[-1]))


def plotTimeFreq(signal_wave):
    # =============================================================================
    #     plot time domain and frequence domain figures of recorded audio
    # =============================================================================
    sample_rate = signal_wave.getframerate()
    sig = np.frombuffer(signal_wave.readframes(sample_rate), dtype=np.int16)
        
    # time domain
    plt.figure(1)
    plot_a = plt.subplot(211)
    plot_a.plot(sig)
    plot_a.set_xlabel('sample rate * time')
    plot_a.set_ylabel('energy')
    
    # frequence domain
    plot_b = plt.subplot(212)
    plot_b.specgram(sig, NFFT=1024, Fs=sample_rate, noverlap=900)
    plot_b.set_xlabel('Time')
    plot_b.set_ylabel('Frequency')
    
    plt.show()    



if __name__ == "__main__":
    
    # =============================================================================
    # parameter:
    #   model_sel: model selection
    #   wav_output_dir = .wav file directory  
    # =============================================================================
    
    model_sel = 1
    wav_output_dir = "Recording"  
    
    # =============================================================================
    # model list:
    #   English
    #   1. vosk-model-small-en-us-0.15   (40M)
    #   2. vosk-model-en-us-0.22-lgraph  (128M)
    #   3. vosk-model-en-us-0.22         (1.8G)
    # =============================================================================


    #
    if not os.path.isdir(wav_output_dir):
        os.mkdir(wav_output_dir)    
    
    model_dict = {1: r"Models\vosk-model-small-en-us-0.15",
                  2: r"Models\vosk-model-en-us-0.22-lgraph",
                  3: r"Models\vosk-model-en-us-0.22"}

    model = vosk.Model(model_dict[model_sel])
    
    
    print("\n\n")
    print("Sound Devices:")
    [print("[%d] %s"%(index, device)) for index, device in enumerate(sr.Microphone.list_microphone_names())]
      
    print('\n')
    print('----------------------------------------')
    print("Press 'Ctrl' to start!\nPress 'Ctrl+C' to terminate.\n")
    
    #
    while (True):

        if keyboard.is_pressed('ctrl'):  # if key 'ctrl' is pressed 
            try:    
                # use system time as the name of the .wav file
                time_now = time.strftime("%Y%m%d_%H_%M_%S")
                wav_output_path = wav_output_dir + "\\" + time_now + ".wav"            
                
                # recording audio from microphone
                RecordAudio(wav_output_path)
                 
                #
                # speech2text
                my_text = Speech2Text(wav_output_path, model)
                print("Transcript:")
                print(my_text)
                
                print('\n')
                print('----------------------------------------')
                print("Press 'Ctrl' to start!\nPress 'Ctrl+C' to terminate.\n")
                
                #
                # plot audio signal in time and frequence domain
                signal_wave = wave.open(wav_output_path, 'r')
                plotTimeFreq(signal_wave)
    
                
            except KeyboardInterrupt:
                print('\nTerminate') 
                break
        
        






    
    
        
        
        
        