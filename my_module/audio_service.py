import speech_recognition as SpRe
import sys

door_queue_for_audio = (sys.argv[1])
audio_resource_queue = (sys.argv[2])
recognition_queue = (sys.argv[3])

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