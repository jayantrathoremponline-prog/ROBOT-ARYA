import sys
import os
import speech_recognition as sr
import urllib.request
import json
import RPi.GPIO as gp
from time import *
from mfrc522 import SimpleMFRC522
from multiprocessing import *

tts_path = "/home/humanoid/Main/TTS"
sys.path.append(tts_path)
import tts

tkinter_path = "/home/humanoid/Main/Tkinter"
sys.path.append(tkinter_path)

import home_screen
import data_screen

url = "http://google.com"

json_file = "/home/humanoid/Main/components.json"

timer_start = None
tk_process = None
play_process = None

lf_pin = 37
up = 8
down = 10
v = 12
gp.setwarnings(False)
gp.setmode(gp.BOARD)

gp.setup(lf_pin, gp.OUT, initial = gp.LOW)
gp.setup(up, gp.OUT, initial = gp.LOW)
gp.setup(down, gp.OUT, initial = gp.LOW)
gp.setup(v, gp.OUT, initial = gp.LOW)

reader = SimpleMFRC522()

# Eyes control
def low_all():
    gp.setup(up, gp.OUT, initial = gp.LOW)
    gp.setup(down, gp.OUT, initial = gp.LOW)
    gp.setup(v, gp.OUT, initial = gp.LOW)

def m_eye():
    low_all()
    gp.output(down, True)
    gp.output(v, True)
    
def v_eye():
    low_all()
    gp.output(up, True)
    gp.output(v, True)

def arrow_eye():
    low_all()
    gp.output(up, True)
    gp.output(down, True)

def all_on():
    low_all()
    gp.output(up, True)
    gp.output(down, True)
    gp.output(v, True)

def voice_gen(device_name = None, name = False):
    v_eye()
    # print("\n\n" + device_name + " is running")
    global timer_start, tk_process, play_process
    tts_return_val = tts.voice_tag(device_name, name)
    # print(f"\n\nPure Value: {tts_return_val}\n\n")
    
    try:
        timer_start = tts_return_val[0]
    except:
        pass
    
    try:
        tk_process = tts_return_val[1]
    except:
        pass
    
    try:
        play_process = tts_return_val[2]
    except:
             pass
    
    # print(f"--------------------\n\n{timer_start} : {tk_process}: {play_process}\n\n--------------------")

    return tts_return_val

def timer_monitor():
    global timer_start, tk_process, play_process
    while True:
        current_time = perf_counter()
        time_difference = current_time - timer_start
        m_eye()
    
        if (time_difference >= 9):
            # print("Time's up!!!")
            # print (f"Elapsed Time: {time_difference:0.4f}")
            try:
                # print(f"--------------------\n\nTime Over: {timer_start} : {tk_process}: {play_process}\n\n--------------------")
                tk_process.terminate()
            except:
                pass
            break

def rfid_reader():
    # SDA <--> 24
    # SCL/SCK <--> 23
    # MISO <--> 21
    # MOSI <--> 19
    # RST <--> 22

    # try:
    # print("Waitng for RFID card")
    id, text= reader.read()
    # print(id)
    return id
    # finally:
    #     gp.cleanup()

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

def conn():
    try:
        urllib.request.urlopen(url, timeout = 5)
        return True
    except:
        return False

def mic():
    conn_status = conn()
    r = sr.Recognizer()
    r.pause_threshold = 0.6
 
    try:
        global triggered
        if triggered:
            timer_process = Process(target = timer_monitor)
            voice_gen("mic")
            timer_process.start()
            triggered = False
    
    except:
        pass
    
    # for index, name in enumerate(sr.Microphone.list_microphone_names()):
    #     print("mic with name \"{1}\" found for 'Microphone(device_index={0})'".format(index, name))
    
    # try:
    # with sr.Microphone(device_index = 3) as source:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        try:
            audio = r.listen(source, timeout = 8, phrase_time_limit = 8)
        except:
            pass

        if conn_status:
        # if conn():
            # print("\n\nSystem is Online.\n\n")

            try:
                mic_query = r.recognize_google(audio, language='en-IN')
                # print(f"\n\nYou said: {mic_query}\n\n")
                
                return mic_query

            except:
                pass
                # print("\n\nCould not understand your audio, please try again !\n\n")

        # elif not conn():
        elif not conn_status:
            # print("\n\nSystem is Offline.\n\n").
            voice_gen("no_connection")

        else:
            voice_gen("unstable_connection")
            
    # except:
    #     print("Microphone error")
    #     pass

def trigger_word_detection():
    # print('''\n\nSay: "hello", "robot", "arya", "namaste" : to trigger\n\n''')
    trig_query = mic()
    
    try:
        trig_query = trig_query.lower()
    except:
        pass
    
    global trigger_word_list
    trigger_word_list = ["arya", "robot"]

    if trig_query in trigger_word_list:
        m_eye()
        global triggered
        triggered = True
        trig_query = action_flow()
        # print(f"\n\nYou said: {trig_query} \n\n")
        return trig_query
    
    else:
        pass
        # print("\n\nNot Triggered\n\n")
        # print(f"You said: {trig_query}\n\n")
    
def action_flow():
    tts.trigger_sound_detect()
    # print("\n\nSay Your Command.\n\n")

    action_query = mic()
    # print(f"\n\nYour Command: {action_query}\n\n")

    try:
        if any(word in action_query.lower() for word in ["hi","welcome", "sir"]):
            voice_gen("computer_lab")

        elif any(word in action_query.lower() for word in ["irrigation", "automatic irrigation system"]):
            voice_gen("auto_irrigation")

        elif any(word in action_query.lower() for word in ["microwave"]):
            voice_gen("microwave")

        elif any(word in action_query.lower() for word in ["cathode ray oscilloscope", "cathode ray", "cathode"]):
            voice_gen("cro")

        elif any(word in action_query.lower() for word in ["smart", "monitor"]):
            voice_gen("smart_appliances")
            
        elif any(word in action_query.lower() for word in ["evm machine", "advance voting"]):
            voice_gen("advanced_evm")
           
        elif any(word in action_query.lower() for word in ["projector", "advanced projector"]):
            voice_gen("smart_projector") 
            
        elif any(word in action_query.lower() for word in["uv", "room sanitizer"]):
            voice_gen("uv_rays")
                     
        elif any(word in action_query.lower() for word in ["how are you", "how's you", "how r u"]):
            voice_gen("health")
        
        
        elif any(word in action_query.lower() for word in ["pick and place", "pick", "and place", "can place", "pic and place"]):
            voice_gen("pick_place")

        elif any(word in action_query.lower() for word in ["solar and wind hybrid energy system", "solar and wind"]):
            voice_gen("solar_wind")
        
        elif any(word in action_query.lower() for word in ["automatic waste segregator and monitoring system", "waste segregator", "waste segregator and monitoring"]):
            voice_gen("waste_management")
        
        elif any(word in action_query.lower() for word in ["automatic water filling machine", "water filling"]):
            voice_gen("water_filling")
            
        elif any(word in action_query.lower() for word in ["antenna", "anntenna"]):
            voice_gen("antenna")
            
        elif any(word in action_query.lower() for word in ["student","attendance"]):
            voice_gen("attendance_system")

        # elif any(word in action_query.lower() for word in ["joke", "jokes", "joking"]):
        #     voice_gen("joke")
        
        elif any(word in action_query.lower() for word in ["introduce yourself", "show me the instructions"]):
            voice_gen("robo_intro")

        elif any(word in action_query.lower() for word in ["restart"]):
            voice_gen("restart")
            sleep(5)
            os.system("sudo reboot now")

        elif any(word in action_query.lower() for word in ["shutdown", "power off", "power of", "switch off", "turn off", "swtich of", "turn of"]):
            voice_gen("shutdown")
            sleep(5)
            os.system("sudo shutdown now")

        elif any(word in action_query.lower() for word in ["the lab"]):
            voice_gen("lab_intro")
            all_on()
            sleep(3)
            gp.output(lf_pin, gp.HIGH)
        
            while True:
                device_name = find_device()
                
                if device_name != "end" and device_name != "home":
                    voice_gen(device_name)
                    
                    if play_process.is_alive():
                        gp.output(lf_pin,gp.LOW)
                        # print("Paused")
                        play_process.join()
                        gp.output(lf_pin, gp.HIGH)                   
                        # print("Resumed")

                elif device_name == "home":
                    gp.output(lf_pin,gp.LOW)
                    # print("Home detected.")
                    break

        elif any(word in action_query.lower() for word in trigger_word_list):
            action_flow()

        else:
            voice_gen("no_data")

    except:
        pass

if __name__ == "__main__":
    arrow_eye()
    tk_process_home = Process(target = home_screen.main)
    tk_process_home.start()
    
    sleep(1.5)
    voice_gen("robo_start")
    sleep(3)
    
    while True:
        if play_process.is_alive():
            v_eye()
        else:
            arrow_eye()

        trigger_word_detection()