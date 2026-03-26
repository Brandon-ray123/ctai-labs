
from time import sleep
from RPi import GPIO

GPIO.setmode(GPIO.BCM)

# GPIO pins connected to L293D inputs
pins = (19, 13, 6, 5)

# Setup all pins as output
GPIO.setup(pins, GPIO.OUT)

# Full step sequence (8 steps)
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
    # Turn one direction
    for n in range(512):
        for step in steps:
            for i in range(4):
                GPIO.output(pins[i], step[i])
            sleep(0.001)  # speed control

    # Turn opposite direction
    for n in range(512):
        for step in steps:
            for i in range(4):
                GPIO.output(pins[3 - i], step[i])  # reverse
            sleep(0.001)

except KeyboardInterrupt:
    print("cleanup")

finally:
    GPIO.cleanup()