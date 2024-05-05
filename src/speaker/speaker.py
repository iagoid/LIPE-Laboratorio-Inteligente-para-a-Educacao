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
                
                rec.adjust_for_ambient_noise(mic, 0.2)
                audio = rec.listen(mic, phrase_time_limit=8)
                recognized_text = rec.recognize_google(audio, language="pt-BR")
                recognized_text = recognized_text.lower()
                return recognized_text

        except sr.RequestError as e:
            SpeakText("Repita" + order)

        except sr.UnknownValueError:
            SpeakText("Repita" + order)