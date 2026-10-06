from time import *
import RPi.GPIO as gp
from mfrc522 import SimpleMFRC522

gp.setwarnings(False)

reader = SimpleMFRC522()

try:
    while True:
        print("Waitng for RFID card")
        id, text= reader.read()
        print(id)
        sleep(0.5)
    # print(id[0])
    # print(text)
            
finally:
    gp.cleanup()
