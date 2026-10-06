import os
import requests
import pyjokes
import sys
import glob
# import pygame
from audioplayer import AudioPlayer
from multiprocessing import *
from time import *

tkinter_path = "/home/humanoid/Main/Tkinter"
sys.path.append(tkinter_path)
import home_screen
import data_screen

url = 'http://0.0.0.0:59125/api/tts'

voice_path = "/home/humanoid/Main/voices/"

global play_process, tk_process, player_obj, timer_start
play_process = None
tk_process = None
player_obj = None
timer_start = None

def trigger_sound_detect():
    sleep(0.5)
    
    test_tuple = voice_tag()
    print(test_tuple)
    
    tk_process = test_tuple[1]
    play_process = test_tuple[2]
    player_obj = test_tuple[3]

    try:
        play_process = Process(target=playsound_process, args=(player_obj, tk_process, play_process.pid, True,))
        print("\n\n Trigger PID Pushed\n\n")
    except:
        play_process = Process(target=playsound_process, args=(player_obj, tk_process, None, True,))

    play_process.start()
    
    # playsound_process(player_obj = player_obj, tk_process = tk_process, play_pid = play_process, bool_chk = True)

def find_file(file_name, path = "/home/humanoid/Main/images/"):
    try:
        file_path = glob.glob(os.path.join(path, file_name+'*'))[0]
        file_extension = file_path.split('.')[-1]
        # print(file_extension)
        image_name = f"{file_name}.{file_extension}"
        # print(image_name)
        image_path = f"{path}/{image_name}"
        return image_path
    except:
        pass

def generate_voice(command_voice_data):
     # Male
    # voice = "en_US/cmu-arctic_low#ahw"
    # voice = "en_US/cmu-arctic_low#rms"
    # voice = "en_US/cmu-arctic_low#aew"
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
    voice = "en_US/ljspeech_low"
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

def playsound_process(player_obj = None, tk_process = None, play_pid = None, bool_chk = False):
    global play_process

    # player_obj = AudioPlayer(device_name)

    if bool_chk:
        wav_path = "/home/humanoid/Main/voices/trigger.wav"
        player_obj = AudioPlayer(wav_path)
        print("Line 101")
    
    try:
        os.kill(play_pid, 9)
        print("\n\nPlayer Killed from line 102\n\n")
        player_obj.stop()
        player_obj.close()
    except:
        pass
        
    player_obj.play(block=True)

    try:
        os.kill(tk_process.pid, 9)
        print("\n\nTkinter Killed from line 108\n\n")
    except:
        pass
    
def voice_tag(device = None, name = False):
    global tk_process, play_process, player_obj

    try:
        if tk_process.is_alive():
            os.kill(tk_process.pid, 9)
            print("\n\nTkinter Killed from line 122\n\n")
    except:
        pass

    if name:
        audio_data = generate_voice(device)
        try:
            os.mkdir(voice_path)
        except:
            pass
            # print("\n\nPath Already Exists\n\n")
        
        audio_data = generate_voice(device)
        device = device.split()[0]
        wav_file = voice_path + device + '.wav'

        with open(wav_file, "wb") as f:
            f.write(audio_data)

        player = AudioPlayer(wav_file)
        player.play(block=True)
        player.stop()
        player.close()

        os.remove(wav_file)

    elif device and not name:
        try:
            text_path = f"/home/humanoid/Main/lib/{device}.txt"
            text_file = open(text_path, "r")
            text_file = text_file.read()
            image_name = find_file(device)
        except:
            pass

        # if device == "joke":
        #     joke_command = pyjokes.get_joke()
        #     # print("\n\n" + str(joke_command) + "\n\n")
        #     audio_data = generate_voice(joke_command)
        #     joke_file = voice_path + 'joke.wav'

        #     with open(joke_file, "wb") as f:
        #         f.write(audio_data)
            
        #     tk_process = Process(target = data_screen.data_window, args = (joke_command,))
        #     tk_process.start()

        #     sleep(1)
            
        #     player = AudioPlayer(joke_file)
        #     player.play(block=True)
        #     player.stop()
        #     player.close()

        #     os.remove(joke_file)
            
        #     try:
        #         if tk_process.is_alive():
        #             os.kill(tk_process.pid, 9)
        #             print("\n\nTkiner Killed from line 173\n\n")
        #     except:
        #         pass

        # elif device == "mic":
        if device == "mic":
            tk_process = Process(target = data_screen.data_window, args = (text_path, image_name,))
            tk_process.start()
            global timer_start
            timer_start = perf_counter()
            
        else:
            tk_process = Process(target = data_screen.data_window, args = (text_path, image_name,))
            tk_process.start()

            print(text_file)

            wav_file = voice_path + device + ".wav"
            isExist = os.path.exists(wav_file)
            
            if isExist:
                # print("\n\nFile exists. Playing the file!!\n\n")
                
                sleep(1.5)

                player_obj = AudioPlayer(wav_file)
                
                try:
                    play_process = Process(target=playsound_process, args=(player_obj, tk_process, play_process.pid,))
                    print("\n\nPID Pushed\n\n")
                except:
                    play_process = Process(target=playsound_process, args=(player_obj, tk_process,))

                play_process.start()
                # playsound_process(player_obj, tk_process)
        
            elif not isExist:
                # print("\n\nFile does not exist, creating the file.\n\n")

                try:
                    os.mkdir(voice_path)
                except:
                    pass
                    # print("\n\nPath Already Exists\n\n")
                
                audio_data = generate_voice(text_file)

                with open(wav_file, "wb") as f:
                    f.write(audio_data)

                sleep(1.5)

                player_obj = AudioPlayer(wav_file)
                
                try:
                    play_process = Process(target=playsound_process, args=(player_obj, tk_process, play_process.pid,))
                    print("\n\nPID Pushed\n\n")
                except:
                    play_process = Process(target=playsound_process, args=(player_obj, tk_process,))
                
                play_process.start()
                # playsound_process(player_obj, tk_process)
            
            else:
                pass
    
    elif device is None and not name:
        return timer_start, tk_process, play_process, player_obj

    try:
        return timer_start, tk_process, play_process, player_obj
    except:
        pass

if __name__ == "__main__":
    # print('\n\nPLAY CHECK:', play_process, play_process.is_alive())
    voice_tag("robo_intro")
    sleep(5)
    voice_tag("robo_start")
    sleep(5)
    # voice_tag("Devansh", True)
    voice_tag("restart")