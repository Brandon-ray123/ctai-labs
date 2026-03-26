
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

servoPin = 18
button = 26

GPIO.setup(servoPin, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

servo = GPIO.PWM(servoPin, 50)
servo.start(0)

state = 0

try:
    while True:
        if GPIO.input(button) == 0:
            if state == 0:
                state = 1
            else:
                state = 0

            time.sleep(0.3)

        if state == 1:
            servo.ChangeDutyCycle(7.5)   # middle position
        else:
            servo.ChangeDutyCycle(0)

except KeyboardInterrupt:
    servo.stop()
    GPIO.cleanup()