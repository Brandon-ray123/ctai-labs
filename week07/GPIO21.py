
from time import sleep
from RPi import GPIO

GPIO.setmode(GPIO.BCM)

pins = (19, 13, 6, 5)
button = 21

GPIO.setup(pins, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

steps = (
    (1,0,0,0),
    (1,1,0,0),
    (0,1,0,0),
    (0,1,1,0),
    (0,0,1,0),
    (0,0,1,1),
    (0,0,0,1),
    (1,0,0,1)
)

try:
    while True:
        if GPIO.input(button) == 0:
            for step in reversed(steps):
                GPIO.output(pins, step)
                sleep(0.001)
        else:
            GPIO.output(pins, (0,0,0,0))

except KeyboardInterrupt:
    GPIO.cleanup()