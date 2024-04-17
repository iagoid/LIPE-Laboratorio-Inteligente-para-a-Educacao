#!/usr/bin/env python
# coding: utf-8

import speech_recognition as sr
import pyttsx3

def SpeakText(command:str):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def SpeakRecongnize(order:str):
    rec = sr.Recognizer()
    
    if order:
        SpeakText(order)
    
    while(True):
        try:
            with sr.Microphone() as mic:
                rec.adjust_for_ambient_noise(mic)
                audio = rec.listen(mic)
                recognized_text = rec.recognize_google(audio, language="pt-BR")
                recognized_text = recognized_text.lower()
                SpeakText(recognized_text)
                
                # pergunta se está correto
                return recognized_text

        except sr.RequestError as e:
            SpeakText("Não consegui entender." + order)

        except sr.UnknownValueError:
            SpeakText("Algo de errado ocorreu." + order)