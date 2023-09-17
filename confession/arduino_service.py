import time
import serial


def arduino_service(door_queue_for_screen, door_queue_for_audio, welcome_queue, block_queue, port="COM5"):
    # Define the serial port and baud
    ser = serial.Serial(port, 9600)
    is_open = False
    
    while True:
        # Read data from the Arduino
        data = ser.readline().decode().strip()
        # print("DATA FROM ARDUINO: " + data)
        # print("Door is open? " + str(is_open))
        if data == "OPEN":
            # print("Door opened")
            is_open = True
            if door_queue_for_audio.empty():
                door_queue_for_audio.put("OPEN")                
            if door_queue_for_screen.empty():
                door_queue_for_screen.put("OPEN")
            # time.sleep(10)
            # block_queue.put("BLOCK")
        elif (data == "CLOSE"):
            is_open = False
            # print("Door closed")
        else:
            # print("YOOO")
            # if door_queue_for_audio.empty() and data == "OPEN" and not is_open:
            #     is_open = True
            #     door_queue_for_audio.put("OPEN")
            # if door_queue_for_screen.empty() and data == "OPEN" and not is_open:
            #     is_open = True
            #     door_queue_for_screen.put("OPEN")
            # else:
            is_open = False

