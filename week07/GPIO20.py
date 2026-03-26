
from time import sleep
from RPi import GPIO

GPIO.setmode(GPIO.BCM)

# stepper motor pins
pins = (19, 13, 6, 5)

# buttons
btn_left = 20


# setup motor pins
GPIO.setup(pins, GPIO.OUT) # all pins at onces

# setup button pins
GPIO.setup(btn_left, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# all outputs low at start
GPIO.output(pins, (0, 0, 0, 0))

# full step sequence
steps = (
    (1, 0, 0, 0),  # step 1
    (1, 1, 0, 0),  # step 2
    (0, 1, 0, 0),  # step 3
    (0, 1, 1, 0),  # step 4
    (0, 0, 1, 0),  # step 5
    (0, 0, 1, 1),  # step 6
    (0, 0, 0, 1),  # step 7
    (1, 0, 0, 1)   # step 8
)

try:
    while True:
        if GPIO.input(btn_left) == 0:   # button pressed
            for step in steps:
                for i in range(4):
                    GPIO.output(pins[i], step[i])
                sleep(0.001)
        else:
            GPIO.output(pins, (0,0,0,0))

except KeyboardInterrupt:
    print("cleanup")
    GPIO.cleanup()