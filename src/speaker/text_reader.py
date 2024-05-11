import pyttsx3

def SpeakText(command:str):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
