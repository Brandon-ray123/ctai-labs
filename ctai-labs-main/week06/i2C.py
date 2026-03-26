
import smbus
import time


class MPU6050:

    ## after try and revise the codes well ##

    def __init__(self, address):
        self.address = address
        self.bus = smbus.SMBus(1)

    def setup(self):
        self.bus.write_byte_data(self.address, 0x6B, 0)
        self.bus.write_byte_data(self.address, 0x1C, 0)
        self.bus.write_byte_data(self.address, 0x1B, 0)

    @staticmethod
    def two_complement(high, low):
        value = (high << 8) + low

        if value > 32767:
            value = value - 65536

        return value

    def read_acceleration(self):
        data = self.bus.read_i2c_block_data(self.address, 0x3B, 6)

        x = MPU6050.two_complement(data[0], data[1])
        y = MPU6050.two_complement(data[2], data[3])
        z = MPU6050.two_complement(data[4], data[5])

        x = x / 16384.0
        y = y / 16384.0
        z = z / 16384.0

        return x, y, z

    def read_gyroscope(self):
        data = self.bus.read_i2c_block_data(self.address, 0x43, 6)

        x = MPU6050.two_complement(data[0], data[1])
        y = MPU6050.two_complement(data[2], data[3])
        z = MPU6050.two_complement(data[4], data[5])

        x = x / 131.0
        y = y / 131.0
        z = z / 131.0

        return x, y, z


mpu = MPU6050(0x68)
mpu.setup()

while True:
    ax, ay, az = mpu.read_acceleration()
    gx, gy, gz = mpu.read_gyroscope()

    print("Acceleration:")
    print(ax, ay, az)

    print("Gyroscope:")
    print(gx, gy, gz)

    print()

    time.sleep(1)