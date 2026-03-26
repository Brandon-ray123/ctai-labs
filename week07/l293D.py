
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

motorPin1 = 14
motorPin2 = 15

GPIO.setup(motorPin1, GPIO.OUT)
GPIO.setup(motorPin2, GPIO.OUT)

dc_pwm_1 = GPIO.PWM(motorPin1, 1000)
dc_pwm_2 = GPIO.PWM(motorPin2, 1000)

dc_pwm_1.start(0)
dc_pwm_2.start(0)

try:
    # turn left, 50% speed
    dc_pwm_1.ChangeDutyCycle(50)
    dc_pwm_2.ChangeDutyCycle(0)
    time.sleep(3)

    # turn right, 80% speed
    dc_pwm_1.ChangeDutyCycle(0)
    dc_pwm_2.ChangeDutyCycle(80)
    time.sleep(3)

    # turn left, 30% speed
    dc_pwm_1.ChangeDutyCycle(30)
    dc_pwm_2.ChangeDutyCycle(0)
    time.sleep(3)

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    dc_pwm_1.stop()
    dc_pwm_2.stop()
    GPIO.cleanup()