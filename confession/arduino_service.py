import keyboard
import serial
import serial.tools.list_ports

def find_arduino_port():
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'Arduino' in p.description  # this part might vary depending on your OS and the Arduino description
    ]
    if not arduino_ports:
        raise IOError("No Arduino found")
    if len(arduino_ports) > 1:
        print('Multiple Arduinos found - using the first one')    
    return arduino_ports[0]


def arduino_service(door_queue_for_screen, door_queue_for_audio, welcome_queue, block_queue, port="COM3"):
    ser = False
    port = find_arduino_port()
    # Define the serial port and baud
    if ser:
        try:
            ser = serial.Serial(port, 9600)
        except Exception as e:
            print("Arduino not connected")
    is_open = False
    
    while True:
        if ser:
            # Read data from the Arduino
            data = ser.readline().decode().strip()
        # if data == "OPEN" or keyboard.is_pressed('k'):
        if keyboard.is_pressed('k'):
            print("Door opened")
            is_open = True
            if door_queue_for_audio.empty():
                door_queue_for_audio.put("OPEN")                
            if door_queue_for_screen.empty():
                door_queue_for_screen.put("OPEN")
            # time.sleep(10)
            # block_queue.put("BLOCK")
        # elif (data == "CLOSE") or keyboard.is_pressed('l'):
        elif keyboard.is_pressed('l'):
            is_open = False
            # print("Door closed")

