
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

motorPin1 = 14
motorPin2 = 15

# set pins to OUTPUT mode
GPIO.setup(motorPin1, GPIO.OUT)
GPIO.setup(motorPin2, GPIO.OUT)

# create PWM and set frequency to 1kHz
dc_pwm_1 = GPIO.PWM(motorPin1, 1000)
dc_pwm_1.start(0)

dc_pwm_2 = GPIO.PWM(motorPin2, 1000)
dc_pwm_2.start(0)

# turn left, 50% speed
#same here you can upgrade the percentage speed
dc_pwm_1.ChangeDutyCycle(50)
dc_pwm_2.ChangeDutyCycle(0)
time.sleep(3)

# turn right, 80% speed, still can upgrade the percentage speed
dc_pwm_1.ChangeDutyCycle(0)
dc_pwm_2.ChangeDutyCycle(80)
time.sleep(3)

# turn left, 30% speed when you run it, you can chnage the percentage run
dc_pwm_1.ChangeDutyCycle(30)
dc_pwm_2.ChangeDutyCycle(0)
time.sleep(3)

# stop everything
dc_pwm_1.stop()
dc_pwm_2.stop()

del dc_pwm_1 #here it did not run  because above we had dc_pwm_1.stop(). del dc_pwm_1
del dc_pwm_2 #so we had to add this code for it to run or it will five errors del dc_pwm_2 

GPIO.cleanup()