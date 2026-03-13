
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

ledPin = 17
GPIO.setup(ledPin, GPIO.OUT)

def send_byte(byte):
    for i in range(7, -1, -1):  # go from bit 7 to bit 0
        bit = (byte >> i) & 1
        print(bit)

        if bit == 1:
            GPIO.output(ledPin, GPIO.HIGH)
        else:
            GPIO.output(ledPin, GPIO.LOW)

        time.sleep(0.2)

message = "hello"

for char in message:
    send_byte(ord(char))
    time.sleep(1)

GPIO.cleanup()