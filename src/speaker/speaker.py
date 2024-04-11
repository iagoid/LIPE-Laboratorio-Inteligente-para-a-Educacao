#!/usr/bin/env python
# coding: utf-8

import speech_recognition as sr
import pyttsx3

def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def SpeakRecongnize(order):
    rec = sr.Recognizer()
    
    if order:
        SpeakText(order)
    
    while(True):
        try:
            with sr.Microphone() as mic:
                rec.adjust_for_ambient_noise(mic, duration=0.2)
                audio = rec.listen(mic)
                MyText = rec.recognize_google(audio, language="pt-BR")
                MyText = MyText.lower()
                SpeakText(MyText)
                
                # pergunta se está correto
                return MyText

        except sr.RequestError as e:
            SpeakText("Não consegui entender")

        except sr.UnknownValueError:
            SpeakText("Algo de errado ocorreu")