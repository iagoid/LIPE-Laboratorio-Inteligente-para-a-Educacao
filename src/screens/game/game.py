#!/usr/bin/env python
# coding: utf-8

import cv2
import time
from src.video_config.video_config import VideoConfig
import src.identifier.identifier as identifier
import src.constants.movements as mov
from pathlib import Path

from src.face_recognition.face_detect import (
    face_detection,
    face_mesh,
)
from src.face_recognition.face_recognizer import FaceRecognizer
from src.draw.draw import (
    initial_message,
    draw_message,
    draw_points,
    show_image_movements,
)
from random import *

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

screen_name = "Identificador de Movimentos"


# laço de repetição que fica rodando durante toda aplicação
def GameScreen():
    # abre o fluxo de leitura
    # video_conf = VideoConfig(screen_name, "./images/videomaos.mp4") #lê de um vídeo
    video_conf = VideoConfig(screen_name, 550, 300)
    video_conf.start()

    t1 = time.perf_counter()
    sort_movement = True
    movement_identified = False

    my_identifier = identifier.Identifier()
    my_face_recognizer = FaceRecognizer(encodings_location=DEFAULT_ENCODINGS_PATH)

    while True:
        if video_conf.stopped is True:
            break
        else:
            img = video_conf.read()

        imgRGB = cv2.cvtColor(
            img, cv2.COLOR_BGR2RGB
        )  # converte a cor para RGB (posso também utilizar essa imagem no processamento)

        # face_detection(img)
        # face_mesh(img)

        face_names = my_face_recognizer.recognize_faces(img=img)
        print(face_names)
        
        my_identifier.process_image(img)

        if my_identifier.points:
            # Verifico se existe a necessidade de realizar um novo sorteio
            delta = time.perf_counter() - t1
            if delta > 5 or sort_movement:
                t1 = time.perf_counter()
                sort_movement = True

            # realiza o sorteio do movimento
            if sort_movement:
                my_identifier.sort_movement()
                show_image_movements(img, my_identifier.command)
                sort_movement = False
                movement_identified = False

            movement_identified = my_identifier.identify()

            if movement_identified:
                draw_message(img, mov.MOVEMENTS_MESSAGE[my_identifier.command])

            draw_points(img, my_identifier.points)
        else:
            initial_message(img)

        cv2.imshow(screen_name, img)  # exibe a imagem com os pontos na tela

        # verifica que teclas foram apertadas
        tecla = cv2.waitKey(33)  # espera em milisegundos da execução das imagens
        if tecla == 27:  # verifica se foi a tecla esc
            break

    video_conf.stop()
    cv2.destroyAllWindows()
