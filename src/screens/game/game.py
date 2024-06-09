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
def GameScreen(width: int, height: int):
    # abre o fluxo de leitura
    # video_conf = VideoConfig(screen_name, "./images/videomaos.mp4") #lê de um vídeo
    video_conf = VideoConfig(screen_name, width=width, height=height)
    video_conf.start()

    timer_next_mov = time.perf_counter()
    timer_show_movement = time.perf_counter()
    sort_movement = True
    show_movement = False
    movement_identified = False

    my_identifier = identifier.Identifier()
    my_face_recognizer = FaceRecognizer(encodings_location=DEFAULT_ENCODINGS_PATH)

    expected_player = "UNKNOWN"  # TODO: Sortear um player

    searching_player = False
    player_found = False

    number_movements = 3
    mov_showing_seq = 0

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
                fut_player_search = executor.submit(
                    my_face_recognizer.recognize_faces, img
                )
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
                # draw_points(img, my_identifier.points)

                if my_identifier.points:
                    if sort_movement:
                        my_identifier.sort_movements(number_movements)
                        sort_movement = False
                        show_movement = True
                        timer_show_movement = time.perf_counter()

                    elif show_movement:
                        img = show_image_movements(
                            img,
                            my_identifier.command_at(mov_showing_seq),
                            mov_showing_seq + 1,
                        )

                        delta = time.perf_counter() - timer_show_movement

                        if delta > 4:
                            if mov_showing_seq < my_identifier.qtd_movements() - 1:
                                timer_show_movement = time.perf_counter()
                                mov_showing_seq += 1
                            else:
                                show_movement = False

                    elif not movement_identified:
                        # Verifico se existe a necessidade de realizar um novo sorteio
                        movement_identified = my_identifier.identify()
                        if movement_identified:
                            timer_next_mov = time.perf_counter()

                    elif movement_identified:
                        message_mov = f"{my_identifier.seq_command + 1} - {mov.MOVEMENTS_MESSAGE[my_identifier.command]}"
                        img = draw_message(img, message_mov)

                        delta = time.perf_counter() - timer_next_mov
                        if delta > 2:
                            if (
                                my_identifier.seq_command
                                < my_identifier.qtd_movements() - 1
                            ):
                                my_identifier.next_movement()
                                movement_identified = False
                                timer_next_mov = time.perf_counter()
                            else:
                                # identificou toda a lista de movimentos, volta as variaveis para o valor inicial
                                mov_showing_seq = 0
                                number_movements += 1

                                movement_identified = False
                                sort_movement = True

                                show_movement = False

            cv2.imshow(screen_name, img)  # exibe a imagem com os pontos na tela

            # verifica que teclas foram apertadas
            tecla = cv2.waitKey(33)  # espera em milisegundos da execução das imagens
            if tecla == 27:  # verifica se foi a tecla esc
                break

    video_conf.stop()
    cv2.destroyAllWindows()
