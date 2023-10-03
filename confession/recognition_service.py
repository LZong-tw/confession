import speech_recognition as SpRe
import logging
import os
from datetime import datetime
import pyaudio

# Setting up logging
log_dir = 'storage/logs'
os.makedirs(log_dir, exist_ok=True)  # Create log directory if it doesn't exist
filename = datetime.now().strftime('%Y%m%d%H%M%S') + '.txt'
log_file = os.path.join(log_dir, filename)

logging.basicConfig(filename=log_file, level=logging.ERROR)

def select_audio_device(name_substring):
    p = pyaudio.PyAudio()
    selected_device_index = None
    
    try:
        # Get count of audio devices
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        
        # Loop through all available devices
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                device_name = p.get_device_info_by_host_api_device_index(0, i).get('name')
                print(f"Input Device id {i} - {device_name}")
                
                # Check if device name contains the desired substring
                if name_substring.lower() in device_name.lower():
                    print(f"Selected device: {device_name}")
                    selected_device_index = i
                    break
    except:
        print("?????????")
    
    return selected_device_index


def recognition_service(door_queue_for_audio, stt_result_queue, recognition_queue, ambient_queue, block_queue):
    # Example usage
    selected_device_index = select_audio_device("éº¥å…‹é¢¨")
    if selected_device_index is not None:
        print(f"RECOGNITION SERVICE Device with index {selected_device_index} is selected.")
    else:
        print("RECOGNITION SERVICE No device with the desired name was found.")
    microphone = SpRe.Microphone(device_index=selected_device_index)
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

