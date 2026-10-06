# # import multiprocessing
# # import time

# # def slow_worker():
# #     print('Starting worker')
# #     time.sleep(1)
# #     print('Finished worker')

# # if __name__ == '__main__':
# #     p = multiprocessing.Process(target=slow_worker)
# #     print('BEFORE:', p, p.is_alive())

# #     p.start()
# #     print('DURING:', p, p.is_alive())

# #     p.terminate()
# #     print('TERMINATED:', p, p.is_alive())

# import pygame
# import multiprocessing
# import time

# def play_wav_file(device):
#     pygame.init()

#     sound = pygame.mixer.Sound(device)
#     sound.play()

#     while pygame.mixer.get_busy():
#         pass

# def run_process(device):
#     try:
#         if process.is_alive():
#             process.terminate()
#     except:
#         pass

#     process = multiprocessing.Process(target=play_wav_file, args = (device,))
#     process.start()

# if __name__ == '__main__':
#     run_process("/home/humanoid/Main/voices/breadboard.wav")
#     time.sleep(5)
#     run_process("/home/humanoid/Main/voices/breadboard.wav")

import pygame
from multiprocessing import *
from time import *

stop_event = Event()

def play_wav_file(device, stop_event):
    pygame.init()
    sound = pygame.mixer.Sound(device)
    sound.play()
    while pygame.mixer.get_busy() and not stop_event.is_set():
        pass

def run_process(device, stop_event):
    global process

    try:
        if process.is_alive():
            stop_event.set()
    except:
        pass

    try:
        if stop_event.is_set():
            process.terminate()
    except:
        pass
    
    process = Process(target=play_wav_file, args=(device, stop_event))
    process.start()
    stop_event.clear()

if __name__ == '__main__':
    run_process("/home/humanoid/Main/voices/breadboard.wav", stop_event)
    sleep(5)
    run_process("/home/humanoid/Main/voices/breadboard.wav", stop_event)
    sleep(5)
    run_process("/home/humanoid/Main/voices/cro.wav", stop_event)
    sleep(5)
    stop_event.set()