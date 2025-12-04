
import smbus
import time

I2C_ADDR = 0x27

LCD_WIDTH = 16

LCD_CHR = 1
LCD_CMD = 0

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

LCD_BACKLIGHT = 0x08
ENABLE = 0b00000100

E_PULSE = 0.0005
E_DELAY = 0.0005

bus = smbus.SMBus(1)


def send_byte_with_e_toggle(bits):
    bus.write_byte(I2C_ADDR, bits | ENABLE)
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, bits & ~ENABLE)
    time.sleep(E_DELAY)


def send_byte(bits, mode):
    high_bits = mode | (bits & 0xF0) | LCD_BACKLIGHT
    low_bits = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    bus.write_byte(I2C_ADDR, high_bits)
    send_byte_with_e_toggle(high_bits)

    bus.write_byte(I2C_ADDR, low_bits)
    send_byte_with_e_toggle(low_bits)


def LCD_init():
    send_byte(0x33, LCD_CMD)
    send_byte(0x32, LCD_CMD)
    send_byte(0x06, LCD_CMD)
    send_byte(0x0C, LCD_CMD)
    send_byte(0x28, LCD_CMD)
    send_byte(0x01, LCD_CMD)
    time.sleep(E_DELAY)


def LCD_string(message, line):
    message = message.ljust(LCD_WIDTH, " ")

    send_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        send_byte(ord(message[i]), LCD_CHR)