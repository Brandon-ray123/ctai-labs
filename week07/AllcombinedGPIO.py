
from RPi import GPIO
import RPi.GPIO as RGPIO
import time

# ----------------------------
# SETUP
# ----------------------------
GPIO.setmode(GPIO.BCM)
RGPIO.setmode(RGPIO.BCM)

# Stepper
stepper_pins = [19, 13, 6, 5]

# Buttons
BTN_LEFT = 20    # S6
BTN_RIGHT = 21   # S5
BTN_DC = 16      # S7
BTN_SERVO = 26   # S4

# DC motor
motorPin1 = 14
motorPin2 = 15

# Servo
SERVO_PIN = 18   # change if needed

# Setup stepper pins
for pin in stepper_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# Setup buttons
GPIO.setup(BTN_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
RGPIO.setup(BTN_DC, RGPIO.IN, pull_up_down=RGPIO.PUD_UP)
RGPIO.setup(BTN_SERVO, RGPIO.IN, pull_up_down=RGPIO.PUD_UP)

# Setup DC motor
RGPIO.setup(motorPin1, RGPIO.OUT)
RGPIO.setup(motorPin2, RGPIO.OUT)
pwm1 = RGPIO.PWM(motorPin1, 1000)
pwm2 = RGPIO.PWM(motorPin2, 1000)
pwm1.start(0)
pwm2.start(0)

# Setup servo
RGPIO.setup(SERVO_PIN, RGPIO.OUT)
servo = RGPIO.PWM(SERVO_PIN, 50)
servo.start(0)

# ----------------------------
# GLOBAL STATES
# ----------------------------
dc_state = 0          # 0=OFF, 1=LEFT, 2=RIGHT
servo_enabled = False

# Stepper sequence
step_sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

# ----------------------------
# HELPER FUNCTIONS
# ----------------------------
def step_once_left(delay=0.001):
    for step in step_sequence:
        for i in range(4):
            GPIO.output(stepper_pins[i], step[i])
        time.sleep(delay)

def step_once_right(delay=0.001):
    for step in reversed(step_sequence):
        for i in range(4):
            GPIO.output(stepper_pins[i], step[i])
        time.sleep(delay)

def stop_stepper():
    for pin in stepper_pins:
        GPIO.output(pin, 0)

def read_pot_percent():
    """
    Replace with your real potentiometer ADC read.
    Must return 0..100
    """
    return 50

def read_joystick_x():
    """
    Replace with your real ADC read for joystick X on channel 6.
    Must return 0..1023
    """
    return 512

def set_dc_motor(mode, speed):
    if mode == 0:
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)

    elif mode == 1:
        pwm1.ChangeDutyCycle(speed)
        pwm2.ChangeDutyCycle(0)

    elif mode == 2:
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(speed)

def joystick_to_angle(value):
    return int((value / 1023) * 180)

def angle_to_duty_cycle(angle):
    return 2.5 + (angle / 18.0)

# ----------------------------
# BUTTON CALLBACKS
# ----------------------------
def dc_toggle_callback(channel):
    global dc_state
    dc_state = (dc_state + 1) % 3
    print(f"DC state: {dc_state}")

def servo_toggle_callback(channel):
    global servo_enabled
    servo_enabled = not servo_enabled
    print(f"Servo enabled: {servo_enabled}")

RGPIO.add_event_detect(BTN_DC, RGPIO.FALLING, callback=dc_toggle_callback, bouncetime=300)
RGPIO.add_event_detect(BTN_SERVO, RGPIO.FALLING, callback=servo_toggle_callback, bouncetime=300)

# ----------------------------
# MAIN LOOP
# ----------------------------
try:
    while True:
        # A + B : stepper while holding button
        if GPIO.input(BTN_LEFT) == GPIO.LOW:
            step_once_left()

        elif GPIO.input(BTN_RIGHT) == GPIO.LOW:
            step_once_right()

        else:
            stop_stepper()

        # C : DC motor with speed from potentiometer
        speed = read_pot_percent()
        set_dc_motor(dc_state, speed)

        # D : Servo on/off + joystick X controls angle
        if servo_enabled:
            x_value = read_joystick_x()
            angle = joystick_to_angle(x_value)
            duty = angle_to_duty_cycle(angle)
            servo.ChangeDutyCycle(duty)
        else:
            servo.ChangeDutyCycle(0)

        time.sleep(0.02)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    stop_stepper()
    pwm1.stop()
    pwm2.stop()
    servo.stop()
    GPIO.cleanup()
    RGPIO.cleanup()