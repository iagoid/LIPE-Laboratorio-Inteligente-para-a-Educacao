#!/usr/bin/env python
# coding: utf-8

import cv2
import src.video_config.video_config as video_config
from pathlib import Path
from src.constants.constants import DIRECTORY_CSV_PLAYERS, DIRECTORY_IMAGE_PLAYER
from threading import Thread, Event
import schedule
from src.face_recognition.face_detect import (
    face_mesh,
    face_detection_model,
)
from random import *
from src.draw.draw import NextPlayer
from src.speaker import speaker
from src.utils.utils import string_from_numbers, number_in_words_2_numeric
from threading import Thread, Lock
import time
import os
import uuid
from pathlib import Path
import csv
import pandas as pd
import math
from src.speaker.text_reader import SpeakText
from src.speaker.speaker import SpeakerMic
import shutil

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")
FIELD_NAMES = ["id", "name", "age"]

screen_name = "Identificador de Movimentos"

class PlayerScreen:
    def __init__(self) -> None:
        self.is_new_player = False
        self.player_id = 1
        self.player = {}
        self.lock = Lock()
        self.my_event = Event()
        self.GetUserId()
        self.next_player = False

    def AskQuestion(self) -> None:
        speaker_mic = SpeakerMic()
        
        while not self.my_event.is_set():
            time.sleep(3)
            with self.lock:
                self.next_player = False
            
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
            counter_age_not_numeric = 1
            while counter_age_not_numeric <= 3:
                text_age = speaker_mic.SpeakRecongnize("Qual sua idade?")
                print(text_age)
                
                age_list = string_from_numbers(text_age)
                converted_age = number_in_words_2_numeric(text_age)
                
                if age_list:
                    age = age_list[0]
                    break
                elif converted_age:
                    age = converted_age
                    break

                counter_age_not_numeric += 1

            if not self.my_event.is_set():
                speaker.SpeakText(age)
                with self.lock:
                    self.player = {}
                    self.player["id"] = self.player_id
                    self.player["name"] = name
                    self.player["age"] = age
                    self.player_id += 1
                    self.is_new_player = False
                    self.SavePlayerCSV()
                    self.player = {}

            schedule.cancel_job(schSaveImg)
            
            with self.lock:
                self.next_player = True

            SpeakText("Próximo Jogador")

    def GetUserId(self):
        try:
            df = pd.read_csv(DIRECTORY_CSV_PLAYERS, header=0)
            max_size = df["id"].max()
            
            if math.isnan(max_size):
                max_size = 1

            self.player_id = max_size + 1
        except:
            self.player_id = 1
            with open(
                DIRECTORY_CSV_PLAYERS, "a", newline="", encoding="utf-8"
            ) as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(FIELD_NAMES)
                

    def SavePlayerCSV(self):
        with open(DIRECTORY_CSV_PLAYERS, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=FIELD_NAMES,
            )
            writer.writerow(self.player)

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
        video_conf = video_config.VideoConfig(screen_name, width=width, height=height)
        video = video_conf.video

        t1 = Thread(target=self.AskQuestion)
        t1.start()

        while True:
            check, src = video.read()  # lê o vídeo
            if not check:
                break

            self.img = cv2.flip(src, 1)  # impede o espelhamneto da tela

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

        video.release()
        cv2.destroyAllWindows()
