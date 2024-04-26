#!/usr/bin/env python
# coding: utf-8

import cv2
import src.video_config.video_config as video_config
from pathlib import Path
import src.constants.constants as constants
from threading import Thread, Event

from src.face_recognition.face_detect import (
    face_detection,
    face_mesh,
    face_detection_model,
)
from src.face_recognition.face_recognizer import recognize_faces
from random import *
from src.speaker import speaker
from threading import Thread, Lock
from multiprocessing.pool import ThreadPool
import time
from cv2.typing import MatLike
import os
import uuid
from pathlib import Path

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

screen_name = "Identificador de Movimentos"


class PlayerScreen:
    def __init__(self) -> None:
        self.is_new_player = False
        self.player_id = 1
        self.player = {}
        self.players = []
        self.lock = Lock()
        self.my_event = Event() 

    def AskQuestion(self) -> None:
        while not self.my_event.is_set():
            time.sleep(3)
            
            # TODO: corrigir o evento, ele só para quando chega no proximo loop
            name = ""
            while len(name) == 0 and not self.my_event.is_set():    
                name = speaker.SpeakRecongnize("Qual seu nome?")
            speaker.SpeakText(name)
                
            with self.lock:
                self.is_new_player = True

            age = ""
            while (len(age) == 0 or not age.isnumeric()) and not self.my_event.is_set():    
                age = speaker.SpeakRecongnize("Qual sua idade?")
            speaker.SpeakText(age)
                
            with self.lock:
                self.player["id"] = self.player_id
                self.player["name"] = name
                self.player["age"] = age
                self.players.append(self.player)
                self.player_id += 1
                self.is_new_player = False
                
    def SavePlayerImages(self, img: MatLike):
        faces = face_detection_model(img)

        directory_save = constants.DIRECTORY_IMAGE_PLAYER + os.sep + str(self.player_id)
        Path(directory_save).mkdir(exist_ok=True)

        for x, y, w, h in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (10, 159, 255), 2)
            cv2.imwrite(
                directory_save + os.sep + str(uuid.uuid1()) + ".jpg",
                img[y : y + h, x : x + w]
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

            img = cv2.flip(src, 1)  # impede o espelhamneto da tela


            # Tira a foto do aluno
            # Caso reconhece um novo aluno mostra a foto na tela e pede o nome
            with self.lock:
                if self.is_new_player:
                    self.SavePlayerImages(img)

            face_mesh(img)

            cv2.imshow(screen_name, img)  # exibe a imagem com os pontos na tela
            print(self.players)

            # verifica que teclas foram apertadas
            tecla = cv2.waitKey(33)  # espera em milisegundos da execução das imagens
            if tecla == 27:  # verifica se foi a tecla esc
                self.my_event.set()
                break

        video.release()
        cv2.destroyAllWindows()
