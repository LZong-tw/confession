import sys
import datetime

listen_queue = eval(sys.argv[1]).strip('"')
audio_resource_queue = eval(sys.argv[2]).strip('"')
recognized_data_queue = eval(sys.argv[3]).strip('"')
recognition_queue = eval(sys.argv[4]).strip('"')
filename_queue = eval(sys.argv[5]).strip('"')
while True:
    while not listen_queue.empty():
        listen_queue.get()
        # 語音轉文字
        try:
            recognition = recognition_queue.get()
            source = audio_resource_queue.get()
            print('start listening...')
            audioData = recognition.listen(source, timeout = 3)
            print('end')
            print('recognizing...')
            content = recognition.recognize_google(audioData, language='zh-tw')
        except Exception as e:
            print(str(e))
            content = '請再說一遍!!'
        print("辨識結果：" + content)
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d_%H%M%S")
        filename = f"../storage/{now}問答.txt"
        with open(filename, "w", encoding="utf-8") as out:
            out.write("問：" + content + "\n")
        filename_queue.put(now)
        print(f'Asking log saved to "{filename}"')
        recognized_data_queue.put(content)
