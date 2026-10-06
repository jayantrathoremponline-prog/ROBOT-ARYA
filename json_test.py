import json
from time import *
import RPi.GPIO as gp
from mfrc522 import SimpleMFRC522

json_file = "/home/humanoid/Main/components.json"

gp.setwarnings(False)
reader = SimpleMFRC522()

def rfid_reader():
    print("Waitng for RFID card")
    id, text= reader.read()
    print(id)
    return id        

def find_device():
    with open(json_file, 'r') as file:
        try:
            devices = json.load(file)
            devices = devices["devices"]
            
            for x in devices:
                keys = x.keys()
                values = x.values()
                key_list = list(keys)
                value_list = list(values)

                card_id = rfid_reader()

                position = value_list.index(card_id)
                position = key_list[position]
                return position

        except:
            return "No Data"

# if __name__ == "__main__":
while True:
    device_name = find_device()
    print(device_name)
    sleep(0.5)
    
    if device_name == "end":
        print("Exiting the code")
        break
    