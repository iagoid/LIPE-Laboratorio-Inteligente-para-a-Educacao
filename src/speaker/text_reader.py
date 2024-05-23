import pyttsx3
import os
from pygame import mixer
import time

def SpeakText(data:str):
    voice = 'pt-BR-AntonioNeural'
    output_file = "data.mp3"
    command = f'edge-tts --voice "{voice}" --text "{data}" --write-media "{output_file}"'
    os.system(command)
    
    mixer.init()
    mixer.music.load(output_file)
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(1)
    mixer.music.stop()
    mixer.quit()
