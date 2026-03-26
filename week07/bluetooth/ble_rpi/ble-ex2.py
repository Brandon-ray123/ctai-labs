
from ble import bluetooth_uart_server
import threading
import queue
import time

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
                tx_q.put("stepper left command received")

            elif incoming == "right":
                tx_q.put("stepper right command received")

            elif incoming == "dc-left":
                tx_q.put("dc motor left command received")

            elif incoming == "dc-right":
                tx_q.put("dc motor right command received")

            elif incoming == "dc-stop":
                tx_q.put("dc motor stop command received")

            elif incoming == "servo-on":
                tx_q.put("servo on command received")

            elif incoming == "servo-off":
                tx_q.put("servo off command received")

            else:
                tx_q.put("unknown command")

        time.sleep(1)

except KeyboardInterrupt:
    print("Ctrl-C received, shutting down...")
    bluetooth_uart_server.stop_ble_gatt_uart_loop()
    time.sleep(0.5)