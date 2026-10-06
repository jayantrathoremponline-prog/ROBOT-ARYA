import pygame
import multiprocessing
from time import sleep

def play_audio(file_path, process2):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass

    if not pygame.mixer.music.get_busy():
        print("Audio has completed playing")
        process2.terminate()

def print_data():
    i = 0
    while True:
        print(f"{i}: Other code is executing")
        sleep(1)
        i+=1

if __name__ == "__main__":
    process2 = multiprocessing.Process(target=print_data)
    process2.start()

    process1 = multiprocessing.Process(target=play_audio, args=("voices/auto_irrigation.wav", process2))
    process1.start()
