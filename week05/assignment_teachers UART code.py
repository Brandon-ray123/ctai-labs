
from RPi import GPIO
import time

GPIO.setmode(GPIO.BCM)

ledPin = 17
GPIO.setup(ledPin, GPIO.OUT)

def send_byte(byte, LSBFirst=True):
    print(LSBFirst)

    for i in range(8):

        nshift = i

        if LSBFirst == False:
            nshift = 7 - i

        bitvalue = (byte & (1 << nshift))

        if bitvalue > 0:
            bitvalue = 1

        GPIO.output(ledPin, bitvalue)

        time.sleep(0.2)


def send_string(text):

    for character in text:

        ascii_value = ord(character)

        print(character, bin(ascii_value))

        send_byte(ascii_value)


send_string("hello world")


GPIO.cleanup()