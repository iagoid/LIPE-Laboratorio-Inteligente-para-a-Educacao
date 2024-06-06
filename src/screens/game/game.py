#!/usr/bin/env python
# coding: utf-8

import cv2
import time
from threading import Thread, Lock 
from src.video_config.video_config import VideoConfig
import src.identifier.identifier as identifier
import src.constants.movements as mov
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

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
from multiprocessing.pool import ThreadPool

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

screen_name = "Identificador de Movimentos"


# laço de repetição que fica rodando durante toda aplicação
def GameScreen():
    # abre o fluxo de leitura
    # video_conf = VideoConfig(screen_name, "./images/videomaos.mp4") #lê de um vídeo
    video_conf = VideoConfig(screen_name, 550, 300)
    video_conf.start()

    timer_sort_movement = time.perf_counter()
    timer_show_movement = time.perf_counter()
    sort_movement = True
    show_movement = False
    movement_identified = False

    my_identifier = identifier.Identifier()
    my_face_recognizer = FaceRecognizer(encodings_location=DEFAULT_ENCODINGS_PATH)

    expected_player = "UNKNOWN" #TODO: Sortear um player
    
    searching_player = False
    player_found = False
    
    with ThreadPoolExecutor(max_workers=4) as executor:
    
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
            
            if not searching_player and not player_found:
                fut_player_search = executor.submit(my_face_recognizer.recognize_faces, img)
                searching_player = True
                
            elif fut_player_search.done() and not player_found:
                seached_player = fut_player_search.result()
                print(seached_player)
                searching_player = False
                if seached_player == expected_player:
                    print("Iniciando o Jogo")
                    player_found = True
                    executor.shutdown()

            elif player_found:
                my_identifier.process_image(img)
                
                delta = time.perf_counter() - timer_sort_movement
                if delta > 10 or sort_movement:
                    timer_sort_movement = time.perf_counter()
                    sort_movement = True
                
                # realiza o sorteio do movimento
                if my_identifier.points:
                    # realiza o sorteio do movimento
                    if sort_movement:
                        my_identifier.sort_movement()
                        show_movement = True
                        
                        delta = time.perf_counter() - timer_show_movement
                        if delta > 5:
                            timer_show_movement = time.perf_counter()
                
                    # Verifico se existe a necessidade de realizar um novo sorteio
                    movement_identified = my_identifier.identify()

                    if movement_identified:
                        draw_message(img, mov.MOVEMENTS_MESSAGE[my_identifier.command])

                    draw_points(img, my_identifier.points)
                else:
                    initial_message(img)
                    
                if show_movement:
                    delta = time.perf_counter() - timer_show_movement
                    if delta < 5:
                        show_image_movements(img, my_identifier.command)
                        movement_identified = False
                        sort_movement = False
                    else:
                        show_movement = False
                

            cv2.imshow(screen_name, img)  # exibe a imagem com os pontos na tela

            # verifica que teclas foram apertadas
            tecla = cv2.waitKey(33)  # espera em milisegundos da execução das imagens
            if tecla == 27:  # verifica se foi a tecla esc
                break

    video_conf.stop()
    cv2.destroyAllWindows()
