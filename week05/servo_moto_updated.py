
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

servoPin = 18
GPIO.setup(servoPin, GPIO.OUT)

def angle_to_DC(angle):
    res = (angle / 18) + 2.5
    print("Target angle {} gives DC of {}".format(angle, res))
    return res

servoPWM = GPIO.PWM(servoPin, 50)
servoPWM.start(angle_to_DC(0))

try:
    while True:
        servoPWM.ChangeDutyCycle(angle_to_DC(0))
        time.sleep(2)

        servoPWM.ChangeDutyCycle(angle_to_DC(180))
        time.sleep(2)

        servoPWM.ChangeDutyCycle(angle_to_DC(45))
        time.sleep(2)

except KeyboardInterrupt:
    pass

finally:
    servoPWM.stop()
    GPIO.cleanup()