from ble import bluetooth_uart_server
import threading
import queue
import time
from RPi import GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

# -------------------
# stepper motor
# -------------------
stepper_pins = (19, 13, 6, 5)
GPIO.setup(stepper_pins, GPIO.OUT)

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

# -------------------
# DC motor
# -------------------
motorPin1 = 14
motorPin2 = 15

GPIO.setup(motorPin1, GPIO.OUT)
GPIO.setup(motorPin2, GPIO.OUT)

dc_pwm_1 = GPIO.PWM(motorPin1, 1000)
dc_pwm_2 = GPIO.PWM(motorPin2, 1000)

dc_pwm_1.start(0)
dc_pwm_2.start(0)

# -------------------
# servo motor
# -------------------
servoPin = 18
GPIO.setup(servoPin, GPIO.OUT)

servo = GPIO.PWM(servoPin, 50)
servo.start(0)

# -------------------
# bluetooth
# -------------------
rx_q = queue.Queue()
tx_q = queue.Queue()

threading.Thread(
    target=bluetooth_uart_server.ble_gatt_uart_loop,
    args=(rx_q, tx_q, "Brandon-RayPi"),
    daemon=True
).start()

try:
    while True:
        try:
            incoming = rx_q.get_nowait()
        except queue.Empty:
            incoming = None

        if incoming:
            incoming = incoming.strip().lower()
            print("Incoming: {}".format(incoming))

            if incoming == "hello":
                tx_q.put("hello back")

            elif incoming == "left":
                for step in steps:
                    GPIO.output(stepper_pins, step)
                    sleep(0.001)
                GPIO.output(stepper_pins, (0,0,0,0))
                tx_q.put("stepper left done")

            elif incoming == "right":
                for step in reversed(steps):
                    GPIO.output(stepper_pins, step)
                    sleep(0.001)
                GPIO.output(stepper_pins, (0,0,0,0))
                tx_q.put("stepper right done")

            elif incoming == "dc-left":
                dc_pwm_1.ChangeDutyCycle(50)
                dc_pwm_2.ChangeDutyCycle(0)
                tx_q.put("dc motor left")

            elif incoming == "dc-right":
                dc_pwm_1.ChangeDutyCycle(0)
                dc_pwm_2.ChangeDutyCycle(50)
                tx_q.put("dc motor right")

            elif incoming == "dc-stop":
                dc_pwm_1.ChangeDutyCycle(0)
                dc_pwm_2.ChangeDutyCycle(0)
                tx_q.put("dc motor stopped")

            elif incoming == "servo-on":
                servo.ChangeDutyCycle(7.5)
                tx_q.put("servo on")

            elif incoming == "servo-off":
                servo.ChangeDutyCycle(0)
                tx_q.put("servo off")

            else:
                tx_q.put("unknown command")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Ctrl-C received, shutting down...")
    bluetooth_uart_server.stop_ble_gatt_uart_loop()
    time.sleep(0.5)

finally:
    dc_pwm_1.stop()
    dc_pwm_2.stop()
    servo.stop()
    GPIO.cleanup()