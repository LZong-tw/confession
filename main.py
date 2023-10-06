import confession
import audio_wave_form
import ctypes
from multiprocessing import Process, Queue
import subprocess
import time
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import sys
from datetime import datetime

class Logger(object):
    def __init__(self, filename="storage/logs/Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        # Generate the current timestamp
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.terminal.write(f"{current_timestamp} - {message}\n")
        self.log.write(f"{current_timestamp} - {message}\n")
        self.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()

    def __del__(self):
        self.log.close()

def set_volume(max_volume=True):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    if max_volume:
        volume.SetMasterVolumeLevelScalar(1, None)  # set volume to 100%
    else:
        volume.GetMasterVolumeLevelScalar()

def arduino_service(door_queue_for_screen, door_queue_for_audio, welcome_queue, block_queue, port="COM3"):
    confession.arduino_service(door_queue_for_screen,
                               door_queue_for_audio, welcome_queue, block_queue, port)


def screen_manager(door_queue_for_screen, screen_queue, welcome_queue, ambient_queue, audio_wave_from_queue):
    confession.screen_manager(door_queue_for_screen,
                              screen_queue, welcome_queue, ambient_queue, audio_wave_from_queue)


def welcome(welcome_queue, block_queue, listen_queue, ambient_queue):
    confession.welcome(welcome_queue, block_queue, listen_queue, ambient_queue)


def responser(screen_queue, reply_queue, stop_queue, print_data_queue,
              filename_queue, voice_count_queue, block_queue):
    confession.responser(screen_queue, reply_queue, stop_queue,
                         print_data_queue,
                         filename_queue, voice_count_queue, block_queue)


def thinker(reply_queue, recognized_data_queue, start_queue, stop_queue):
    confession.thinker(reply_queue, recognized_data_queue, start_queue, stop_queue)


def supervisor(stop_queue, reply_queue, start_queue):
    confession.supervisor(stop_queue, reply_queue, start_queue)


def recognition_bridge(listen_queue, stt_result_queue,
               recognized_data_queue, recognition_queue, filename_queue):
    confession.recognition_bridge(listen_queue, stt_result_queue,
                          recognized_data_queue, recognition_queue,
                          filename_queue)


def print_service(print_data_queue, stop_queue):
    confession.print_service(print_data_queue, stop_queue)


def recognition_service(door_queue_for_audio, stt_result_queue,
                  recognition_queue, ambient_queue, block_queue):
    confession.recognition_service(door_queue_for_audio,
                             stt_result_queue, recognition_queue, ambient_queue, block_queue)
    
def audio_wave_form_func(audio_wave_from_queue):
    audio_wave_form.audio_wave_form_body(audio_wave_from_queue)


if __name__ == '__main__':
    subprocess.Popen(['python', 'video_daemon.py'])
    time.sleep(3)
    subprocess.Popen(['python', 'audio_wave_form_daemon.py'])
    time.sleep(3)
    set_volume()
    today_string = datetime.today().strftime('%Y-%m-%d')
    sys.stdout = Logger("storage/logs/" + today_string + ".log")
    sys.stderr = sys.stdout
    print(f"This will be logged to storage/logs/{today_string}.log")

    door_queue_for_screen = Queue()
    door_queue_for_audio = Queue()
    print_data_queue = Queue()
    reply_queue = Queue()
    stop_queue = Queue()
    recognized_data_queue = Queue()
    screen_queue = Queue()
    listen_queue = Queue()
    stt_result_queue = Queue()
    recognition_queue = Queue()
    filename_queue = Queue()
    voice_count_queue = Queue()
    welcome_queue = Queue()
    start_queue = Queue()
    block_queue = Queue()
    ambient_queue = Queue()
    audio_wave_from_queue = Queue()

    arduino_service_process = Process(target=arduino_service, args=(
        door_queue_for_screen, door_queue_for_audio, welcome_queue, block_queue))
    screen_manager_process = Process(target=screen_manager, args=(
        door_queue_for_screen, screen_queue, welcome_queue, ambient_queue, audio_wave_from_queue,))
    welcome_process = Process(target=welcome, args=(welcome_queue, block_queue, listen_queue, ambient_queue,))
    responser_process = Process(target=responser, args=(
        screen_queue, reply_queue, stop_queue, print_data_queue,
        filename_queue, voice_count_queue, block_queue,))
    thinker_process = Process(target=thinker, args=(
        reply_queue, recognized_data_queue, start_queue, stop_queue,))
    supervisor_process = Process(target=supervisor, args=(
        stop_queue, reply_queue, start_queue,))
    recognition_bridge_process = Process(target=recognition_bridge, args=(
        listen_queue, stt_result_queue,
        recognized_data_queue, recognition_queue, filename_queue,))
    print_service_process = Process(target=print_service, args=(
        print_data_queue, stop_queue,))
    recognition_service_process = Process(target=recognition_service, args=(
        door_queue_for_audio, stt_result_queue,
        recognition_queue, ambient_queue, block_queue,))

    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)

    arduino_service_process.start()
    screen_manager_process.start()
    welcome_process.start()
    responser_process.start()
    thinker_process.start()
    supervisor_process.start()
    recognition_bridge_process.start()
    print_service_process.start()
    recognition_service_process.start()

    arduino_service_process.join()
    screen_manager_process.join()
    welcome_process.join()
    responser_process.join()
    thinker_process.join()
    supervisor_process.join()
    recognition_bridge_process.join()
    print_service_process.join()
    recognition_service_process.join()