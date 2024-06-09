#!/usr/bin/env python
# coding: utf-8

import cv2
import time
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
    show_player_image,
)
from random import *
from database.students.students import select_students

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

screen_name = "Identificador de Movimentos"


# laço de repetição que fica rodando durante toda aplicação
class Game:
    def __init__(self):
        self.sort_movement = True
        self.is_showing_movements = False
        self.is_movement_identified = False
        self.searching_player = False
        self.player_found = False

        self.number_movements = 3
        self.mov_showing_seq = 0
        self.player_seq = 0

    def find_expected_player(self):

        if not self.searching_player:
            self.fut_player_search = self.executor.submit(
                self.my_face_recognizer.recognize_faces, self.img
            )
            self.searching_player = True

        elif self.fut_player_search.done():
            seached_player = self.fut_player_search.result()

            self.searching_player = False
            if seached_player == self.expected_player:
                print("Iniciando o Jogo")
                self.player_found = True
                self.executor.shutdown()

    def sort_sequence_movements(self):
        self.my_identifier.sort_movements(self.number_movements)
        self.sort_movement = False
        self.is_showing_movements = True
        self.timer_is_showing_movements = time.perf_counter()

    def show_movement(self):
        self.img = show_image_movements(
            self.img,
            self.my_identifier.command_at(self.mov_showing_seq),
            self.mov_showing_seq + 1,
        )

        delta = time.perf_counter() - self.timer_is_showing_movements

        if delta > 4:
            if self.mov_showing_seq < self.my_identifier.qtd_movements() - 1:
                self.timer_is_showing_movements = time.perf_counter()
                self.mov_showing_seq += 1
            else:
                self.is_showing_movements = False

    def show_identified_movement(self):
        message_mov = f"{self.my_identifier.seq_command + 1} - {mov.MOVEMENTS_MESSAGE[self.my_identifier.command]}"
        self.img = draw_message(self.img, message_mov)

        delta = time.perf_counter() - self.timer_next_mov
        if delta > 2:
            if self.my_identifier.seq_command < self.my_identifier.qtd_movements() - 1:
                self.my_identifier.next_movement()
                self.is_movement_identified = False
                self.timer_next_mov = time.perf_counter()
            else:
                # identificou toda a lista de movimentos, volta as variaveis para o valor inicial
                self.mov_showing_seq = 0
                self.number_movements += 1

                self.is_movement_identified = False
                self.sort_movement = True

                self.is_showing_movements = False

                if len(self.list_players) == 0:
                    print("Não foram identificados jogadores.")
                    self.expected_player = None
                else:
                    self.player_seq += 1
                    if self.player_seq <= len(self.list_players):
                        self.expected_player = self.list_players[self.player_seq][0]

    def show_next_player(self):
        img_player = show_player_image(self.img, self.expected_player)
        
        if img_player is None:
            return
        
        self.img = img_player
        
        delta = time.perf_counter() - self.timer_is_showing_movements
        if delta > 4:
            self.is_showing_next_player = False
            self.player_found = False

    def Show(self, width: int, height: int):
        # abre o fluxo de leitura
        # video_conf = VideoConfig(screen_name, "./images/videomaos.mp4") #lê de um vídeo
        video_conf = VideoConfig(screen_name, width=width, height=height)
        video_conf.start()

        self.timer_next_mov = time.perf_counter()
        self.timer_is_showing_movements = time.perf_counter()

        self.my_identifier = identifier.Identifier()
        self.my_face_recognizer = FaceRecognizer(
            encodings_location=DEFAULT_ENCODINGS_PATH
        )

        self.list_players = select_students()

        self.is_showing_next_player = True
        self.expected_player = self.list_players[self.player_seq][0]

        with ThreadPoolExecutor(max_workers=4) as self.executor:

            while True:
                if video_conf.stopped is True:
                    break
                else:
                    self.img = video_conf.read()

                    # imgRGB = cv2.cvtColor(
                    #     self.img, cv2.COLOR_BGR2RGB
                    # )  # converte a cor para RGB (posso também utilizar essa imagem no processamento)

                    # face_detection(img)
                    # face_mesh(img)
                    if self.is_showing_next_player:
                        self.show_next_player()

                    elif not self.player_found:
                        self.find_expected_player()

                    else:
                        self.my_identifier.process_image(self.img)
                        # draw_points(self.img, self.my_identifier.points)

                        if self.my_identifier.points:
                            if self.sort_movement:
                                self.sort_sequence_movements()

                            elif self.is_showing_movements:
                                self.show_movement()

                            elif not self.is_movement_identified:
                                # Verifico se existe a necessidade de realizar um novo sorteio
                                self.is_movement_identified = (
                                    self.my_identifier.identify()
                                )
                                if self.is_movement_identified:
                                    self.timer_next_mov = time.perf_counter()

                            elif self.is_movement_identified:
                                self.show_identified_movement()

                    cv2.imshow(
                        screen_name, self.img
                    )  # exibe a imagem com os pontos na tela

                # verifica que teclas foram apertadas
                tecla = cv2.waitKey(
                    33
                )  # espera em milisegundos da execução das imagens
                if tecla == 27:  # verifica se foi a tecla esc
                    break

        video_conf.stop()
        cv2.destroyAllWindows()
