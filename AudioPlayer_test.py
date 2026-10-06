# from time import sleep
# from audioplayer import AudioPlayer
# from multiprocessing import *

# def process_play(device_name):
#     player = AudioPlayer(device_name)
#     player.play(block=False)
#     sleep(2)
#     player.pause()
#     sleep(2)
#     player.resume()
#     sleep(2)
#     player.stop()
#     sleep(2)
#     player.play()
#     sleep(2)
#     player.close()

# if __name__=="__main__":
#     process1 = Process(target=process_play, args=("/home/humanoid/Main/voices/breadboard.wav",))
#     process1.start()
#     sleep(5)
#     process1.terminate()

from audioplayer import AudioPlayer
import time

# Create an instance of AudioPlayer
player = AudioPlayer("/home/humanoid/Main/voices/robo_intro.wav")

# Play the audio file
player.play()

# Check if the audio is still playing
while player.status()['state'] == 'playing':
    time.sleep(1)

# The audio has finished playing
print("Audio has finished playing")