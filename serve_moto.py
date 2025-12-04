
import RPi.GPIO as GPIO
import time

# Use BCM pin numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the servo signal
servopin = 18

# Set the servo pin as OUTPUT
GPIO.setup(servopin, GPIO.OUT)

# Create PWM object with 50Hz frequency (standard for servos)
servo_pwm = GPIO.PWM(servopin, 50)

# Start PWM with duty cycle for ~0 degrees
servo_pwm.start(5)

# Move servo to ~180 degrees
servo_pwm.ChangeDutyCycle(10)
time.sleep(3)

# Move servo back to ~0 degrees
servo_pwm.ChangeDutyCycle(5)
time.sleep(3)

# Move servo to a middle position (~90-120 degrees depending on servo)
servo_pwm.ChangeDutyCycle(8)
time.sleep(3)

# Move servo again to ~180 degrees
servo_pwm.ChangeDutyCycle(10)
time.sleep(3)

# Stop PWM and clean GPIO pins
servo_pwm.stop()
GPIO.cleanup()