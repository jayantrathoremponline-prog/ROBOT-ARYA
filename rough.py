import os
from time import *
from multiprocessing import *
import pygame

global var 
var = 1
process = None

def play_sound(sound_path):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        continue

def play_process(sound_path):
    global var
    global process

    if process is not None:
        os.kill(process.pid, 9)

    process = Process(target=play_sound, args=(sound_path,))
    process.start()
    process_pid = process.pid
    print(f"\nProcess {var} PID: {process_pid}\n")
    var += 1

if __name__ == '__main__':
    sound_path1 = '/home/humanoid/Main/voices/breadboard.wav'
    sound_path2 = '/home/humanoid/Main/voices/cro.wav'

    play_process(sound_path1)

    sleep(5)  # delay in seconds before playing the second file

    play_process(sound_path2)