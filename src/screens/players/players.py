#!/usr/bin/env python
# coding: utf-8

import cv2
from src.video_config.video_config import VideoConfig
from pathlib import Path
from src.constants.constants import DIRECTORY_IMAGE_PLAYER
from threading import Thread, Event, Lock
import schedule
from src.face_recognition.face_detect import (
    face_detection_model,
)
from random import *
from src.draw.draw import NextPlayer
from src.speaker import speaker
from src.utils.utils import string_from_numbers, number_in_words_2_numeric
import time
import os
import uuid
from pathlib import Path
from src.speaker.text_reader import SpeakText
from src.speaker.speaker import SpeakerMic
from database.students.students import select_max_id, add_student

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

screen_name = "Identificador de Movimentos"


class PlayerScreen:
    def __init__(self) -> None:
        self.is_new_player = False
        self.player = {}
        self.lock = Lock()
        self.my_event = Event()
        self.GetLastUserId()
        self.next_player = False

    def AskQuestion(self) -> None:
        speaker_mic = SpeakerMic()

        while not self.my_event.is_set():
            time.sleep(3)
            with self.lock:
                self.next_player = False

            self.schIsaveImgProfile = schedule.every(1).seconds.do(
                self.SaveProfilePicture
            )
            schSaveImg = schedule.every(1).seconds.do(self.SavePlayerImages)

            # TODO: corrigir o evento, ele só para quando chega no proximo loop
            name = "NÃO IMPLEMENTADO"
            # while len(name) == 0 and not self.my_event.is_set():
            #     name = speaker.SpeakRecongnize("Qual seu nome?", self.my_event)
            # speaker.SpeakText(name)
            # print(name)

            with self.lock:
                self.is_new_player = True

            age = 0
            order = "Qual sua idade?"
            for _ in range(3):  # realiza 3 tentativas
                if self.my_event.is_set():
                    schedule.cancel_job(schSaveImg)
                    return
                
                text_age = speaker_mic.SpeakRecongnize(order)
                print(text_age)

                age_list = string_from_numbers(text_age)
                converted_age = number_in_words_2_numeric(text_age)

                if age_list:
                    age = age_list[0]
                    break
                elif converted_age:
                    age = converted_age
                    break
                
                order = "Não entendi. Qual sua idade?"
            
            if self.my_event.is_set():
                schedule.cancel_job(schSaveImg)
                return
            
            speaker.SpeakText(age)
            with self.lock:
                self.player = {}
                self.player["id"] = self.player_id
                self.player["name"] = name
                self.player["age"] = age
                self.is_new_player = False
                self.SavePlayer()
                self.player = {}

            schedule.cancel_job(schSaveImg)

            self.GetLastUserId()

            with self.lock:
                self.next_player = True

            if self.my_event.is_set():
                return
            SpeakText("Próximo Jogador")

    def GetLastUserId(self):
        last_id = select_max_id()
        self.player_id = last_id + 1

    def SavePlayer(self):
        add_student(student=(self.player["age"],))

    def SaveProfilePicture(self):
        faces = face_detection_model(self.img)

        directory_save = DIRECTORY_IMAGE_PLAYER + os.sep + str(self.player_id)
        Path(directory_save).mkdir(exist_ok=True)

        for x, y, w, h in faces:
            pY = int(y // 1.8)
            pX = int(x // 1.5)

            height = int(h * 1.8)
            width = int(w * 1.5)

            cv2.imwrite(
                directory_save + os.sep + "profile.jpg",
                self.img[pY : y + height, pX : x + width],
            )

            schedule.cancel_job(self.schIsaveImgProfile)
            break

    def SavePlayerImages(self):
        faces = face_detection_model(self.img)

        directory_save = DIRECTORY_IMAGE_PLAYER + os.sep + str(self.player_id)
        Path(directory_save).mkdir(exist_ok=True)

        for x, y, w, h in faces:
            cv2.imwrite(
                directory_save + os.sep + str(uuid.uuid1()) + ".jpg",
                self.img[y : y + h, x : x + w],
            )

    def Show(self, width: int, height: int):
        video_conf = VideoConfig(screen_name, width=width, height=height)
        video_conf.start()
        
        thread_question = Thread(target=self.AskQuestion)
        thread_question.start()

        while True:
            if video_conf.stopped is True:
                break
            else:
                self.img = video_conf.read()

            # Tira a foto do aluno
            # Caso reconhece um novo aluno mostra a foto na tela e pede o nome
            with self.lock:
                if self.is_new_player:
                    schedule.run_pending()

            # face_mesh(self.img)
            with self.lock:
                if self.next_player:
                    self.img = NextPlayer(self.img)

            cv2.imshow(screen_name, self.img)  # exibe a imagem com os pontos na tela

            # verifica que teclas foram apertadas
            tecla = cv2.waitKey(33)  # espera em milisegundos da execução das imagens
            if tecla == 27:  # verifica se foi a tecla esc
                self.my_event.set()
                break
        
        thread_question.join()
        video_conf.stop()
        cv2.destroyAllWindows()
