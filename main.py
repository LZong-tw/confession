from my_module import *
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
audio_resource_queue = multiprocessing.Queue()
recognition_queue = multiprocessing.Queue()
filename_queue = multiprocessing.Queue()
voice_count_queue = multiprocessing.Queue()
welcome_queue = multiprocessing.Queue()

# Launch Module 1 in a separate process
arduino_service = subprocess.Popen(['python', 'arduino_service.py', [
    str(door_queue_for_screen),
    str(door_queue_for_audio),
]])

# Launch Module 2 in a separate process
screen_manager = subprocess.Popen(['python', 'screen_manager.py', [
    str(door_queue_for_screen),
    str(screen_queue),
    str(welcome_queue),
]])

welcome = subprocess.Popen(['python', 'welcome.py', str(welcome_queue)])

responser = subprocess.Popen(['python', 'responser.py', [
    str(screen_queue),
    str(reply_queue),
    str(stop_queue),
    str(print_data_queue),
    str(filename_queue),
    str(voice_count_queue),
]])

thinker = subprocess.Popen(['python', 'thinker.py', [str(reply_queue), str(recognized_data_queue)]])
supervisor = subprocess.Popen(['python', 'supervisor.py', [
    str(stop_queue),
    str(recognized_data_queue)
]])
recognizer = subprocess.Popen(['python', 'recognizer.py', [
    str(listen_queue),
    str(audio_resource_queue),
    str(recognized_data_queue),
    str(recognition_queue),
    str(filename_queue)
]])
print_service = subprocess.Popen(['python', 'print_service.py', [
    str(print_data_queue),
    str(voice_count_queue),
]])
audio_service = subprocess.Popen(['python', 'audio_service.py', [
    str(door_queue_for_audio),
    str(audio_resource_queue),
    str(recognition_queue),
]])

# Continue with the main script

# Optionally, retrieve data from the queue
# data_from_module1 = queue.get()
# data_from_module2 = queue.get()

# if __name__ == "__main__":
    #function1()
    #function2()