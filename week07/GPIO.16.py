
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

motorPin1 = 14
motorPin2 = 15
button = 16

GPIO.setup(motorPin1, GPIO.OUT)
GPIO.setup(motorPin2, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

dc_pwm_1 = GPIO.PWM(motorPin1, 1000)
dc_pwm_2 = GPIO.PWM(motorPin2, 1000)

dc_pwm_1.start(0)
dc_pwm_2.start(0)

state = 0

try:
    while True:
        if GPIO.input(button) == 0:
            state = state + 1

            if state > 2:
                state = 0

            time.sleep(0.3)

        if state == 0:
            dc_pwm_1.ChangeDutyCycle(0)
            dc_pwm_2.ChangeDutyCycle(0)

        elif state == 1:
            dc_pwm_1.ChangeDutyCycle(50)
            dc_pwm_2.ChangeDutyCycle(0)

        elif state == 2:
            dc_pwm_1.ChangeDutyCycle(0)
            dc_pwm_2.ChangeDutyCycle(50)

except KeyboardInterrupt:
    dc_pwm_1.stop()
    dc_pwm_2.stop()
    GPIO.cleanup()