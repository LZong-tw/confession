import time


def supervisor(stop_queue, reply_queue, start_queue):
    while True:
        while reply_queue.empty() and not start_queue.empty():
            # count x seconds
            count = 0
            while count < 16:
                if not reply_queue.empty():
                    print("supervisor stopped")
                    while not start_queue.empty():
                        print("start queue cleared: " + 
                        start_queue.get())
                    break
                time.sleep(1)
                print("SUPERVISOR wait, " + str(count) + " sec")
                count += 1
            if reply_queue.empty():
                stop_queue.put("STOP SUPERVISOR")
                print("too long, halted")
                while not start_queue.empty():
                    print("start queue cleared 2: " + 
                    start_queue.get())
