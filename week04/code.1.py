
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led = 17
GPIO.setup(led, GPIO.OUT)
ledpwm = GPIO.PWM(led, 1000)
ledpwm.start(0)

try:
    while True:
        ledpwm.ChangeDutyCycle(10)
        time.sleep(0.5)
        ledpwm.ChangeDutyCycle(0)
        time.sleep(0.5)
        ledpwm.ChangeDutyCycle(100)
        time.sleep(0.5)
        ledpwm.ChangeDutyCycle(0)
        time.sleep(0.5)


except KeyboardInterrupt:
    ledpwm.stop()
    del ledpwm
    GPIO.cleanup()