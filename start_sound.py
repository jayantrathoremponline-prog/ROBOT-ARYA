from audioplayer import AudioPlayer
import time

player = AudioPlayer("/home/humanoid/Main/voices/startup.wav")

player.play(block=True)
player.stop()
player.close()