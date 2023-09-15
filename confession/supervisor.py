import time
import sys

stop_queue = eval(sys.argv[1]).strip('"')
recognized_data_queue = eval(sys.argv[2]).strip('"')

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