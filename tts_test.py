import os
import requests
import pyjokes
import sys
import glob
import simpleaudio as sa
import pygame
from playsound import playsound
from multiprocessing import *
from time import *

tkinter_path = "Tkinter"
sys.path.append(tkinter_path)
import home_screen
import data_screen

url = 'http://0.0.0.0:59125/api/tts'

voice_path = 'voices/'

global play_process

def generate_voice(command_voice_data):
     # Male
    # voice = "en_US/cmu-arctic_low#ahw"
    # voice = "en_US/cmu-arctic_low#rms"
    voice = "en_US/cmu-arctic_low#aew"
    # voice = "en_US/cmu-arctic_low#bdl"
    # voice = "en_US/cmu-arctic_low#jmk"
    # voice = "en_US/cmu-arctic_low#fem"
    # voice = "en_US/cmu-arctic_low#gka"
    # voice = "en_US/hifi-tts_low#9017"
    # voice = "en_US/hifi-tts_low#6097"
    # voice = "en_US/vctk_low#p274"
    # voice = "en_US/vctk_low#p270"
    # voice = "en_US/vctk_low#p284"
    # voice = "en_US/vctk_low#p360"
    # voice = "en_US/vctk_low#p316"
    
    # Female
    # voice = "en_US/ljspeech_low"
    # voice = "en_US/cmu-arctic_low#slt"
    # voice = "en_US/cmu-arctic_low#clb"
    # voice = "en_US/cmu-arctic_low#ljm"
    # voice = "en_US/cmu-arctic_low#slp"
    # voice = "en_US/cmu-arctic_low#eey"
    # voice = "en_US/vctk_low#p283"
    # voice = "en_US/vctk_low#p314"
    # voice = "en_US/vctk_low#p323"
    # voice = "en_US/vctk_low#s5"
    # voice = "en_US/vctk_low#p293"
    # voice = "en_US/vctk_low#p248"
    # voice = "en_US/vctk_low#p362"

    r = requests.post(url, params={"voice": voice}, data=command_voice_data)
    
    if not r.ok:
        print(f"Mimic3 server error: {r.reason}")
    
    else:
        audio_data = r.content
        return audio_data

def trigger_sound_detect():
    try:
        if tk_process.is_alive():
            tk_process.terminate()
    except:
        pass

    global play_process
    try:
        if play_process.is_alive():
            play_process.terminate()
    except:
        pass

    sleep(0.5)
    playsound("voices/trigger.wav")

def playsound_process(device, tk_process):
    global play_process

    try:
        if play_process.is_alive():
            play_process.terminate()
    except:
        pass
    
    pygame.mixer.init()
    pygame.mixer.music.load(device)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass

    if not pygame.mixer.music.get_busy():
        print("Audio has completed playing")
        tk_process.terminate()

def find_file(path, file_name):
    try:
        file_path = glob.glob(os.path.join(path, file_name+'*'))[0]
        file_extension = file_path.split('.')[-1]
        print(file_extension)
        image_name = f"{file_name}.{file_extension}"
        print(image_name)
        image_path = f"images/{image_name}"
        return image_path
    except:
        pass

def voice_tag(device: str, name = False):
    global tk_process, play_process

    try:
        if play_process.is_alive():
            play_process.terminate()
        
    except:
        pass

    if device == "joke" and not name:
        joke_command = pyjokes.get_joke()
        print("\n\n" + str(joke_command) + "\n\n")
        audio_data = generate_voice(joke_command)
        joke_file = voice_path + 'joke.wav'

        with open(joke_file, "wb") as f:
            f.write(audio_data)
        
        tk_process = Process(target = data_screen.data_window, args = (joke_command,))
        tk_process.start()

        sleep(1)
        
        playsound(joke_file, True)
        os.remove(joke_file)
        tk_process.terminate()

    elif name:
        audio_data = generate_voice(device)
        try:
            os.mkdir(voice_path)
        except:
            print("\n\nPath Already Exists\n\n")
        
        audio_data = generate_voice(device)
        device = device.split()[0]
        wav_file = voice_path + device + '.wav'

        with open(wav_file, "wb") as f:
            f.write(audio_data)

        playsound(wav_file, True)
        os.remove(wav_file)

    elif device and not name:
        text_path = f"lib/{device}.txt"
        text_file = open(text_path, "r")
        text_file = text_file.read()
        image_name = find_file("images/", device,)
        
        tk_process = Process(target = data_screen.data_window, args = (text_path, image_name,))
        tk_process.start()

        print(text_file)

        wav_file = voice_path + device + ".wav"
        isExist = os.path.exists(wav_file)
        
        if isExist:
            print("\n\nFile exists. Playing the file!!\n\n")
            sleep(1.5)

            play_process = Process(target=playsound_process, args=(wav_file, tk_process,))
            play_process.start()
    
        elif not isExist:
            print("\n\nFile does not exist, creating the file.\n\n")

            try:
                os.mkdir(voice_path)
            except:
                print("\n\nPath Already Exists\n\n")
            
            audio_data = generate_voice(text_file)

            with open(wav_file, "wb") as f:
                f.write(audio_data)

            sleep(1.5)
            play_process = Process(target=playsound_process, args=(wav_file, tk_process,))
            play_process.start()
        
        else:
            pass

if __name__ == "__main__":
    trigger_sound_detect()
    sleep(2)
    voice_tag("fun_gen")
    sleep (2)
    voice_tag()
    sleep (7)
    voice_tag("microwave_test")
    sleep (2)
    voice_tag("water_filling")
    sleep(1.5)
    voice_tag("waste_management")