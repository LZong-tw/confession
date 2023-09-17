import time
from pygame import mixer  # Load the popular external library


def welcome(welcome_queue, block_queue, listen_queue, ambient_queue):
    while True:
        if not welcome_queue.empty():           
            ambient_queue.put("START")  
            content = welcome_queue.get()
            print("Welcome Queue: " + content)           
            while not welcome_queue.empty():
                print("WELCOME QUEUE remains: " + welcome_queue.get())
            time.sleep(2)
            if (content == "welcome") and block_queue.empty():
                mixer.init(buffer=8192)
                mixer.music.load('assets/welcome_words/synthesis.wav')
                mixer.music.play()
                time.sleep(17)
                listen_queue.put("Start recognizing")
