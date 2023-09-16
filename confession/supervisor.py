import time
import sys


def supervisor(stop_queue, recognized_data_queue, start_queue):
    while True:
        while recognized_data_queue.empty() and not start_queue.empty():
            # count x seconds
            count = 0
            while count < 18:
                time.sleep(1)
                count += 1
            if not recognized_data_queue.empty():
                break
            else:
                stop_queue.put("stop")
                while not start_queue.empty():
                    start_queue.get()
