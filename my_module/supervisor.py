import time
import sys

stop_queue = (sys.argv[1])
recognized_data_queue = (sys.argv[2])

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