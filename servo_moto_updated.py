import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

SERVO_PIN = 18
GPIO.setup(SERVO_PIN, GPIO.OUT)

def angle_to_duty_cycle(angle):
    duty = 2.5 + (angle / 18)
    print(f"Target angle {angle} gives DC of {duty}")
    return duty

servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)

try:
    while True:
        for angle in [0, 180, 45]:
            servo.ChangeDutyCycle(angle_to_duty_cycle(angle))
            time.sleep(2)

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    servo.stop()
    GPIO.cleanup()


