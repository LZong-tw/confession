import time
from pygame import mixer  # Load the popular external library


def welcome(welcome_queue):
    while True:
        while not welcome_queue.empty():
            welcome_queue.get()
            mixer.init(buffer=8192)
            mixer.music.load('../assets/welcome_words/synthesis.wav')
            mixer.music.play()
            while mixer.music.get_busy():  # wait for music to finish playing
                time.sleep(1)
