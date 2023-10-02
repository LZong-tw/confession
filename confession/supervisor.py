import time


def supervisor(stop_queue, reply_queue, start_queue):
    while True:
        while reply_queue.empty() and not start_queue.empty():
            # count x seconds
            count = 0
            while count < 13:
                if not reply_queue.empty():
                    print("supervisor stopped by reply queue not empty")
                    while not start_queue.empty():
                        print("start queue cleared: " + 
                        start_queue.get())
                    break
                if not stop_queue.empty():
                    stop_queue.get()
                    print("supervisor stopped by stop queue")
                    break
                time.sleep(1)
                print("SUPERVISOR wait, " + str(count) + " sec")
                count += 1
            if stop_queue.empty() and reply_queue.empty():
                stop_queue.put("STOP SUPERVISOR")
                print("too long, halted")
                while not start_queue.empty():
                    print("start queue cleared 2: " + 
                    start_queue.get())
            else:
                print("supervisor " + stop_queue.get())
                while not start_queue.empty():
                    print("stop queue cleared: " +
                    stop_queue.get())
                break
