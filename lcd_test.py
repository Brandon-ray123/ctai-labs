
import lcd
import time

lcd.LCD_init()

while True:
    lcd.LCD_string("Hello", lcd.LCD_LINE_1)
    lcd.LCD_string("Brandon-Ray", lcd.LCD_LINE_2)
    time.sleep(2)

    lcd.LCD_string("CTAI", lcd.LCD_LINE_1)
    lcd.LCD_string("Week 5", lcd.LCD_LINE_2)
    time.sleep(2)

    