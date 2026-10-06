import RPi.GPIO as gp
from time import sleep

up = 8
down = 10
v = 12

gp.setwarnings(False)

gp.setmode(gp.BOARD)
gp.setup(up, gp.OUT, initial = gp.LOW)
gp.setup(down, gp.OUT, initial = gp.LOW)
gp.setup(v, gp.OUT, initial = gp.LOW)

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

while True:
    # m_eye()
    # sleep(2)
    arrow_eye()
    sleep(0.15)
    v_eye()
    sleep(5)
    # arrow_eye()
    # sleep(0.15)