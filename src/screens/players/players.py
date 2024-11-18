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
from src.draw.draw import write_message
from src.speaker import speaker
from src.utils.utils import string_from_numbers, number_in_words_2_numeric
import time
import os
import uuid
from pathlib import Path
from src.speaker.text_reader import SpeakText
from src.speaker.speaker import SpeakerMic
from database.students.students import select_max_id, add_student
from src.utils.dir import delete_files_in_directory
from src.datatypes.player import Player

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

screen_name = "Identificador de Movimentos"


class PlayerScreen:
    def __init__(self) -> None:
        self.is_new_player = False
        self.player: Player
        self.lock = Lock()
        self.my_event = Event()
        self.GetLastUserId()
        self.next_player = False
        self.qtd_img_playes = 0
        self.all_images_recorded = False

    def AskQuestion(self) -> None:
        speaker_mic = SpeakerMic()

        while not self.my_event.is_set():
            time.sleep(3)

            with self.lock:
                self.all_images_recorded = False
                self.next_player = False

            self.create_directory()
            self.schIsaveImgProfile = schedule.every(1).seconds.do(
                self.SaveProfilePicture
            )
            self.schSaveImg = schedule.every(1).seconds.do(self.SavePlayerImages)

            name = speaker_mic.SpeakRecongnize("Qual seu nome?")
            speaker.SpeakText(name)

            with self.lock:
                self.is_new_player = True

            age = 0
            order = "Qual sua idade?"

            if self.my_event.is_set():
                schedule.cancel_job(self.schSaveImg)
                return

            text_age = speaker_mic.SpeakRecongnize(order)

            age_list = string_from_numbers(text_age)
            converted_age = number_in_words_2_numeric(text_age)

            if age_list:
                age = age_list[0]
            elif converted_age:
                age = converted_age

            order = "Não entendi. Qual sua idade?"

            if self.my_event.is_set():
                schedule.cancel_job(self.schSaveImg)
                return

            if age > 0:
                speaker.SpeakText(age)

            schedule.cancel_job(self.schSaveImg)

            while not self.all_images_recorded:
                self.SavePlayerImages()
                time.sleep(0.5)

            with self.lock:
                self.player = Player(self.player_id, name, age)
                self.is_new_player = False
                self.SavePlayer()
                self.player = None

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
        add_student(self.player)

    def create_directory(self):
        self.directory_save = DIRECTORY_IMAGE_PLAYER + os.sep + str(self.player_id)
        Path(self.directory_save).mkdir(exist_ok=True)
        delete_files_in_directory(self.directory_save)

    def SaveProfilePicture(self):
        faces = face_detection_model(self.img)

        for x, y, w, h in faces:
            pY = int(y // 1.8)
            pX = int(x // 1.5)

            height = int(h * 1.8)
            width = int(w * 1.5)

            cv2.imwrite(
                self.directory_save + os.sep + "profile.jpg",
                self.img[pY : y + height, pX : x + width],
            )

            schedule.cancel_job(self.schIsaveImgProfile)
            break

    def SavePlayerImages(self):
        faces = face_detection_model(self.img)

        for x, y, w, h in faces:
            cv2.imwrite(
                self.directory_save + os.sep + str(uuid.uuid1()) + ".jpg",
                self.img,
            )

            self.qtd_img_playes += 1

        if self.qtd_img_playes >= 20:
            with self.lock:
                self.all_images_recorded = True

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
                    self.img = write_message(self.img, "PRÓXIMO JOGADOR")

            cv2.imshow(screen_name, self.img)  # exibe a imagem com os pontos na tela

            # verifica que teclas foram apertadas
            tecla = cv2.waitKey(33)  # espera em milisegundos da execução das imagens
            if tecla == 27:  # verifica se foi a tecla esc
                self.my_event.set()
                break

        thread_question.join()
        video_conf.stop()
        cv2.destroyAllWindows()
