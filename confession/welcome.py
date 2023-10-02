import time
from pygame import mixer  # Load the popular external library


def welcome(welcome_queue, block_queue, listen_queue, ambient_queue):
    while True:
        if not welcome_queue.empty():
            content = welcome_queue.get()
            print("Welcome Queue: " + content)
            time.sleep(2)
            while not welcome_queue.empty():
                print("WELCOME QUEUE remains: " + welcome_queue.get())
            if (content == "welcome") and block_queue.empty():
                block_queue.put("BLOCK")
                mixer.init(buffer=8192)
                mixer.music.load('assets/welcome_words/synthesis.wav')
                mixer.music.play()
                time.sleep(17)
                listen_queue.put("Start recognizing")
