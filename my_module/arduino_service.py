import time
import serial
import sys


# Define the serial port and baud rate
ser = serial.Serial('COM5', 9600)
# Change '/dev/ttyUSB0' to the correct port on your system

door_queue_for_screen = eval(sys.argv[1])
door_queue_for_audio = eval(sys.argv[2])

while True:
    # Read data from the Arduino
    data = ser.readline().decode().strip()
    if data == "OPEN":
        door_queue_for_audio.put("OPEN")
        door_queue_for_screen.put("OPEN")
        time.sleep(15)
    else:
        door_queue_for_audio.get()
        door_queue_for_screen.get()