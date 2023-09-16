import subprocess
import multiprocessing

# Create a multiprocessing queue for communication
door_queue_for_screen = multiprocessing.Queue()
door_queue_for_audio = multiprocessing.Queue()
print_data_queue = multiprocessing.Queue()
reply_queue = multiprocessing.Queue()
stop_queue = multiprocessing.Queue()
recognized_data_queue = multiprocessing.Queue()
screen_queue = multiprocessing.Queue()
listen_queue = multiprocessing.Queue()
stt_result_queue = multiprocessing.Queue()
recognition_queue = multiprocessing.Queue()
filename_queue = multiprocessing.Queue()
voice_count_queue = multiprocessing.Queue()
welcome_queue = multiprocessing.Queue()

# Launch Module 1 in a separate process
arduino_service = subprocess.Popen(['python', 'confession/arduino_service.py', 
    str(door_queue_for_screen),
    str(door_queue_for_audio),
])

# Launch Module 2 in a separate process
screen_manager = subprocess.Popen(['python', './confession/screen_manager.py', 
    str(door_queue_for_screen),
    str(screen_queue),
    str(welcome_queue),
])

welcome = subprocess.Popen(['python', 'confession/welcome.py', str(welcome_queue)])

responser = subprocess.Popen(['python', 'confession/responser.py', 
    str(screen_queue),
    str(reply_queue),
    str(stop_queue),
    str(print_data_queue),
    str(filename_queue),
    str(voice_count_queue),
])

thinker = subprocess.Popen(['python', 'confession/thinker.py', str(reply_queue), str(recognized_data_queue)])
supervisor = subprocess.Popen(['python', 'confession/supervisor.py', 
    str(stop_queue),
    str(recognized_data_queue)
])
recognizer = subprocess.Popen(['python', 'confession/recognizer.py', 
    str(listen_queue),
    str(stt_result_queue),
    str(recognized_data_queue),
    str(recognition_queue),
    str(filename_queue)
])
print_service = subprocess.Popen(['python', 'confession/print_service.py', 
    str(print_data_queue),
    str(voice_count_queue),
])
audio_service = subprocess.Popen(['python', 'confession/audio_service.py', 
    str(door_queue_for_audio),
    str(stt_result_queue),
    str(recognition_queue),
])

# Continue with the main script

# Optionally, retrieve data from the queue
# data_from_module1 = queue.get()
# data_from_module2 = queue.get()

# if __name__ == "__main__":
    #function1()
    #function2()