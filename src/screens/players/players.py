#!/usr/bin/env python
# coding: utf-8

import cv2
import src.video_config.video_config as video_config
from pathlib import Path

from src.face_recognition.face_detect import (
    face_detection,
    face_mesh,
)
from src.face_recognition.face_recognizer import recognize_faces
from random import *
from src.speaker import speaker

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

screen_name = "Identificador de Movimentos"

def PlayersScreen():
    video_conf = video_config.VideoConfig(screen_name)
    video = video_conf.video


    while True:
        check, src = video.read()  # lê o vídeo
        if not check:
            break

        img = cv2.flip(src, 1)  # impede o espelhamneto da tela

        face_detection(img)
        face_mesh(img)
        
        # Tira a foto do aluno
        # Caso não reconhece mostra a foto na tela e pede o nome
        
        text_recognized = speaker.SpeakRecongnize("Qual seu nome?")
        print(text_recognized)
        
        text_recognized = speaker.SpeakRecongnize("Quando você nasceu")
        print(text_recognized)

        face_names = recognize_faces(img=img, encodings_location=DEFAULT_ENCODINGS_PATH)

        cv2.imshow(screen_name, img)  # exibe a imagem com os pontos na tela

        # verifica que teclas foram apertadas
        tecla = cv2.waitKey(33)  # espera em milisegundos da execução das imagens
        if tecla == 27:  # verifica se foi a tecla esc
            break

    video.release()
    cv2.destroyAllWindows()
