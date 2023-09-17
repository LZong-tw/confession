import time
from pygame import mixer  # Load the popular external library
from pydub import AudioSegment


def welcome(welcome_queue, block_queue, listen_queue):
    while True:
        if not welcome_queue.empty():
            content = welcome_queue.get()
            print("Welcome Queue: " + content)
            if (content == "welcome") and block_queue.empty():
                mixer.init(buffer=8192)
                mixer.music.load('assets/welcome_words/synthesis.wav')
                mixer.music.play()
                # while not mixer.music.get_busy():  # wait for music to finish playing
                #     time.sleep(1)
                audio = AudioSegment.from_file('assets/welcome_words/synthesis.wav')
                # Get the duration in milliseconds and convert it to seconds
                duration = len(audio)
                time.sleep((duration - 1000) / 1000)
                listen_queue.put("Start recognizing")
