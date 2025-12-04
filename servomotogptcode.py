
from RPi import GPIO
import time

GPIO.setmode(GPIO.BCM)

ledPin = 17
GPIO.setup(ledPin, GPIO.OUT)

def send_byte(byte):
    for i in range(8):
        nshift = 7 - i   # MSB first

        bitvalue = (byte & (1 << nshift))

        if bitvalue > 0:
            bitvalue = 1
        else:
            bitvalue = 0

        print(bitvalue)
        GPIO.output(ledPin, bitvalue)

        time.sleep(0.2)

def send_string(text):
    for character in text:
        ascii_value = ord(character)
        print(character, ascii_value)
        send_byte(ascii_value)
        time.sleep(1)   # 1 second between characters

send_string("hello")

GPIO.cleanup()