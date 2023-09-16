import time
import sys


def supervisor(stop_queue, recognized_data_queue):
    while True:
        while recognized_data_queue.empty():
            # count x seconds
            count = 0
            while count < 3:
                time.sleep(1)
                count += 1
            if not recognized_data_queue.empty():
                break
            else:
                stop_queue.put("stop")
