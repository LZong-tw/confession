import confession
import subprocess
from multiprocessing import Process, Queue


def arduino_service(door_queue_for_screen, door_queue_for_audio, welcome_queue, block_queue, port="COM3"):
    confession.arduino_service(door_queue_for_screen,
                               door_queue_for_audio, welcome_queue, block_queue, port)


def screen_manager(door_queue_for_screen, screen_queue, welcome_queue):
    confession.screen_manager(door_queue_for_screen,
                              screen_queue, welcome_queue)


def welcome(welcome_queue, block_queue, listen_queue):
    confession.welcome(welcome_queue, block_queue, listen_queue)


def responser(screen_queue, reply_queue, stop_queue, print_data_queue,
              filename_queue, voice_count_queue):
    confession.responser(screen_queue, reply_queue, stop_queue,
                         print_data_queue,
                         filename_queue, voice_count_queue)


def thinker(reply_queue, recognized_data_queue, start_queue, stop_queue):
    confession.thinker(reply_queue, recognized_data_queue, start_queue, stop_queue)


def supervisor(stop_queue, recognized_data_queue, start_queue):
    confession.supervisor(stop_queue, recognized_data_queue, start_queue)


def recognition_bridge(listen_queue, stt_result_queue,
               recognized_data_queue, recognition_queue, filename_queue):
    confession.recognition_bridge(listen_queue, stt_result_queue,
                          recognized_data_queue, recognition_queue,
                          filename_queue)


def print_service(print_data_queue, voice_count_queue):
    confession.print_service(print_data_queue, voice_count_queue)


def recognition_service(door_queue_for_audio, stt_result_queue,
                  recognition_queue):
    confession.recognition_service(door_queue_for_audio,
                             stt_result_queue, recognition_queue)


if __name__ == '__main__':
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

    arduino_service_process = Process(target=arduino_service, args=(
        door_queue_for_screen, door_queue_for_audio, welcome_queue, block_queue))
    screen_manager_process = Process(target=screen_manager, args=(
        door_queue_for_screen, screen_queue, welcome_queue,))
    welcome_process = Process(target=welcome, args=(welcome_queue, block_queue, listen_queue))
    responser_process = Process(target=responser, args=(
        screen_queue, reply_queue, stop_queue, print_data_queue,
        filename_queue, voice_count_queue,))
    thinker_process = Process(target=thinker, args=(
        reply_queue, recognized_data_queue, start_queue, stop_queue,))
    supervisor_process = Process(target=supervisor, args=(
        stop_queue, recognized_data_queue, start_queue,))
    recognition_bridge_process = Process(target=recognition_bridge, args=(
        listen_queue, stt_result_queue,
        recognized_data_queue, recognition_queue, filename_queue,))
    print_service_process = Process(target=print_service, args=(
        print_data_queue, voice_count_queue,))
    recognition_service_process = Process(target=recognition_service, args=(
        door_queue_for_audio, stt_result_queue,
        recognition_queue,))

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
