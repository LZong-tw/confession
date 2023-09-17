import datetime


def recognition_bridge(listen_queue, stt_result_queue, recognized_data_queue,
               recognition_queue, filename_queue):
    while True:
        while not listen_queue.empty():
            print("Listen Queue: " + listen_queue.get())
            # 語音轉文字
            recognition_queue.put("START RECOGNITION")               
        while not stt_result_queue.empty():
            content = stt_result_queue.get()
            print("辨識結果：" + content)
            now = datetime.datetime.now()
            now = now.strftime("%Y-%m-%d_%H%M%S")
            filename = f"storage/{now}問答.txt"
            with open(filename, "w", encoding="utf-8") as out:
                out.write("問：" + content + "\n")
            filename_queue.put(now)
            print(f'Asking log saved to "{filename}"')
            recognized_data_queue.put(content)
