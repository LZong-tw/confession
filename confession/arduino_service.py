import time
import serial


def arduino_service(door_queue_for_screen, door_queue_for_audio, port="COM5"):
    # Define the serial port and baud
    ser = serial.Serial(port, 9600)

    while True:
        # Read data from the Arduino
        data = ser.readline().decode().strip()
        if data == "OPEN":
            door_queue_for_audio.put("OPEN")
            door_queue_for_screen.put("OPEN")
            time.sleep(15)
        elif data == "CLOSE" and (
                not (
                    door_queue_for_audio.empty() and
                    door_queue_for_screen.empty())
                ):
            door_queue_for_audio.get()
            door_queue_for_screen.get()
