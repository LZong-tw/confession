import time
from pygame import mixer  # Load the popular external library

def playWelcomWords():    
    mixer.init(buffer = 8192)
    mixer.music.load('歡迎詞錄音/synthesis.wav')
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(1)