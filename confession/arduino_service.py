import time
import serial


def arduino_service(door_queue_for_screen, door_queue_for_audio, welcome_queue, block_queue, port="COM5"):
    # Define the serial port and baud
    ser = serial.Serial(port, 9600)
    is_open = False

    while True:
        # Read data from the Arduino
        data = ser.readline().decode().strip()
        if data == "OPEN" and not is_open:
            print("Door opened")
            is_open = True
            if door_queue_for_audio.empty():
                door_queue_for_audio.put("OPEN")
            else:
                while not door_queue_for_audio.empty():
                    print("CLEAR DOOR OPEN QUEUE FOR AUDIO: " + door_queue_for_audio.get())
            if door_queue_for_screen.empty():
                door_queue_for_screen.put("OPEN")
                # if welcome_queue.empty():
                #     welcome_queue.put("welcome")
            else:
                while not door_queue_for_screen.empty():
                    print("CLEAR DOOR OPEN QUEUE FOR SCREEN: " + door_queue_for_screen.get())
            time.sleep(10)
            block_queue.put("BLOCK")
        elif (data == "CLOSE" and is_open) and (
                not (
                    door_queue_for_audio.empty() and
                    door_queue_for_screen.empty())
                ):
            print("Door closed")
            while not door_queue_for_audio.empty():
                print('arduino service: door_queue_for_audio not empty')
                door_queue_for_audio.get()
            while not door_queue_for_screen.empty():
                print('arduino service: door_queue_for_screen not empty')
                door_queue_for_screen.get()
        else:
            # print("Arduino exception: " + data)
            if door_queue_for_audio.empty() and data == "OPEN" and not is_open:
                door_queue_for_audio.put("OPEN")
            else:
                while not door_queue_for_audio.empty():
                    print("CLEAR DOOR OPEN QUEUE FOR AUDIO2: " + door_queue_for_audio.get())
            if door_queue_for_screen.empty() and data == "OPEN" and not is_open:
                door_queue_for_screen.put("OPEN")
                # if welcome_queue.empty():
                #     welcome_queue.put("welcome")
            else:
                while not door_queue_for_screen.empty():
                    print("CLEAR DOOR OPEN QUEUE FOR SCREEN2: " + door_queue_for_screen.get())
        time.sleep(1)

