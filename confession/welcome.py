import time
from pygame import mixer  # Load the popular external library


def welcome(welcome_queue, block_queue, listen_queue):
    while True:
        if not welcome_queue.empty():
            content = welcome_queue.get()
            print("Welcome Queue: " + content)
            if (content == "welcome") and block_queue.empty():
                mixer.init(buffer=8192)
                mixer.music.load('assets/welcome_words/synthesis.wav')
                mixer.music.play()
                while mixer.music.get_busy():  # wait for music to finish playing
                    time.sleep(1)
                listen_queue.put("Start recognizing")
