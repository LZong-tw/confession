import speech_recognition as SpRe

def recognition_service(door_queue_for_audio, stt_result_queue, recognition_queue):
    microphone = SpRe.Microphone(device_index=1)
    recognition = SpRe.Recognizer()

    with microphone as source:
        while True:
            if not door_queue_for_audio.empty():
                content = door_queue_for_audio.get()
                print("Audio service get door_queue_for_audio: " + content)

                while not stt_result_queue.empty():
                    stt_result_queue.get()
                    recognition.adjust_for_ambient_noise(source, duration=2)

            while not recognition_queue.empty():
                content = recognition_queue.get()
                print(content)

                if content == "START RECOGNITION":
                    try:
                        print('start listening...')
                        audioData = recognition.listen(source, timeout=2,
                                                       phrase_time_limit=3)
                        print('end')
                        print('recognizing...')
                        content = recognition.recognize_google(audioData, language='zh-tw')
                    except Exception as e:
                        print(str(e))
                        content = '請再說一遍!!'
                stt_result_queue.put(content)

