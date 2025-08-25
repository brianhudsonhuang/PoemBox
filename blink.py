import serial
import time

ser = serial.Serial('COM7', 9600, timeout=1)
time.sleep(2)

for i in range(10):
    ser.write(b'1')   # send a byte
    time.sleep(0.5)        # wait 0.5 seconds
    ser.write(b'0')   # send a byte
    time.sleep(0.5)

ser.close()