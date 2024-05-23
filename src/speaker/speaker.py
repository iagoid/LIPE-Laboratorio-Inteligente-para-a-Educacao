#!/usr/bin/env python
# coding: utf-8

import speech_recognition as sr
from threading import Event
import json
from src.speaker.text_reader import SpeakText
import whisper


def SpeakRecongnize(order: str, event: Event) -> str:
    rec = sr.Recognizer()

    if order:
        SpeakText(order)

    while True:
        try:
            with sr.Microphone() as mic:
                rec.adjust_for_ambient_noise(mic, 0.2)
                audio = rec.listen(mic, phrase_time_limit=8)

                if event.is_set():
                    return ""

                recognized_text = rec.recognize_whisper(audio, language="pt")
                recognized_text = recognized_text.lower()
                return recognized_text

        except sr.RequestError:
            return "Não Identificado"

        except sr.UnknownValueError:
            SpeakText("Repita" + order)


# para reconhecimentos numéricos do vosk, é necessário gravar o aúdio
def SpeakRecongnizeVosk(order: str, event: Event) -> str:
    rec = sr.Recognizer()

    if order:
        SpeakText(order)

    while True:
        try:
            with sr.Microphone() as mic:
                rec.adjust_for_ambient_noise(mic, 0.2)
                audio = rec.listen(mic, phrase_time_limit=8)

                if event.is_set():
                    return ""

                recognized_text = json.loads(rec.recognize_vosk(audio))
                recognized_text = recognized_text["text"].lower()
                return recognized_text

        except sr.RequestError:
            return "Não Identificado"

        except sr.UnknownValueError:
            SpeakText("Repita" + order)


def SpeakRecongnizeWhisper(order: str, event: Event) -> str:
    rec = sr.Recognizer()

    if order:
        SpeakText(order)

    while True:
        try:
            with sr.Microphone() as mic:
                rec.adjust_for_ambient_noise(mic, 0.2)
                audio = rec.listen(mic, phrase_time_limit=8)

                if event.is_set():
                    return ""

            file_name = "audio_file.wav"
            with open(file_name, "wb") as file:
                file.write(audio.get_wav_data())

            audio = whisper.load_audio(file_name)
            audio = whisper.pad_or_trim(audio)

            model = whisper.load_model("tiny")
            result = model.transcribe(
                audio,
                fp16=False,
                language="pt",
                verbose=True,
                patience=2,
                beam_size=5,
            )
            
            return result["text"]

        except:
            print("Texto não reconhecido")
