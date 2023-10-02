import speech_recognition as SpRe
import logging
import os
from datetime import datetime

# Setting up logging
log_dir = 'storage/logs'
os.makedirs(log_dir, exist_ok=True)  # Create log directory if it doesn't exist
filename = datetime.now().strftime('%Y%m%d%H%M%S') + '.txt'
log_file = os.path.join(log_dir, filename)

logging.basicConfig(filename=log_file, level=logging.ERROR)

def recognition_service(door_queue_for_audio, stt_result_queue, recognition_queue, ambient_queue, block_queue):
    microphone = SpRe.Microphone(device_index=3)
    recognition = SpRe.Recognizer()

    with microphone as source:
        while True:
            if not ambient_queue.empty(): # and block_queue.empty():
                print("Ambient queue get: " + ambient_queue.get())
                recognition.adjust_for_ambient_noise(source, duration=2)
                print("Ambient completed.")

            if not recognition_queue.empty():
                content = recognition_queue.get()
                print(content)

                if content == "START RECOGNITION":
                    try:
                        print('start listening...')
                        audioData = recognition.listen(source, timeout=2,
                                                       phrase_time_limit=5)
                        print('end')
                        print('recognizing...')
                        content = recognition.recognize_google(audioData, language='zh-tw')
                    except Exception as e:
                        error_message = str(e)
                        print(error_message)
                        logging.error(error_message)
                        content = '我覺得沒有意義，請給我一段智慧之語'
                stt_result_queue.put(content)

