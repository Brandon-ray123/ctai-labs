from time import sleep
from RPi import GPIO
import RPi.GPIO as GPIO2

# --------------------------
# setup
# --------------------------
GPIO.setmode(GPIO.BCM)
GPIO2.setmode(GPIO2.BCM)

# stepper
stepper_pins = (19, 13, 6, 5)
button_left = 20
button_right = 21

GPIO.setup(stepper_pins, GPIO.OUT)
GPIO.setup(button_left, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_right, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

# dc motor
motorPin1 = 14
motorPin2 = 15
button_dc = 16

GPIO2.setup(motorPin1, GPIO2.OUT)
GPIO2.setup(motorPin2, GPIO2.OUT)
GPIO2.setup(button_dc, GPIO2.IN, pull_up_down=GPIO2.PUD_UP)

dc_pwm_1 = GPIO2.PWM(motorPin1, 1000)
dc_pwm_2 = GPIO2.PWM(motorPin2, 1000)

dc_pwm_1.start(0)
dc_pwm_2.start(0)

dc_state = 0

# servo
servoPin = 18
button_servo = 26

GPIO2.setup(servoPin, GPIO2.OUT)
GPIO2.setup(button_servo, GPIO2.IN, pull_up_down=GPIO2.PUD_UP)

servo = GPIO2.PWM(servoPin, 50)
servo.start(0)

servo_state = 0

# --------------------------
# main loop
# --------------------------
try:
    while True:

        # A = stepper left
        if GPIO.input(button_left) == 0:
            for step in steps:
                GPIO.output(stepper_pins, step)
                sleep(0.001)

        # B = stepper right
        elif GPIO.input(button_right) == 0:
            for step in reversed(steps):
                GPIO.output(stepper_pins, step)
                sleep(0.001)

        # no stepper button pressed
        else:
            GPIO.output(stepper_pins, (0,0,0,0))

        # C = DC motor toggle
        if GPIO2.input(button_dc) == 0:
            dc_state = dc_state + 1

            if dc_state > 2:
                dc_state = 0

            sleep(0.3)

        if dc_state == 0:
            dc_pwm_1.ChangeDutyCycle(0)
            dc_pwm_2.ChangeDutyCycle(0)

        elif dc_state == 1:
            dc_pwm_1.ChangeDutyCycle(50)
            dc_pwm_2.ChangeDutyCycle(0)

        elif dc_state == 2:
            dc_pwm_1.ChangeDutyCycle(0)
            dc_pwm_2.ChangeDutyCycle(50)

        # D = servo on / off
        if GPIO2.input(button_servo) == 0:
            if servo_state == 0:
                servo_state = 1
            else:
                servo_state = 0

            sleep(0.3)

        if servo_state == 1:
            servo.ChangeDutyCycle(7.5)
        else:
            servo.ChangeDutyCycle(0)

except KeyboardInterrupt:
    dc_pwm_1.stop()
    dc_pwm_2.stop()
    servo.stop()
    GPIO.cleanup()
    GPIO2.cleanup()