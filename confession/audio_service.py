import speech_recognition as SpRe


def audio_service(door_queue_for_audio, audio_resource_queue, recognition_queue):
    while True:
        while not door_queue_for_audio.empty():
            door_queue_for_audio.get()
            if not audio_resource_queue.empty():
                audio_resource_queue.get()
            if not recognition_queue.empty():
                recognition_queue.get()
            recognition = SpRe.Recognizer()
            with SpRe.Microphone(device_index=1) as source:
                recognition.adjust_for_ambient_noise(source, duration=2)
                audio_resource_queue.put(source)
                recognition_queue.put(recognition)
