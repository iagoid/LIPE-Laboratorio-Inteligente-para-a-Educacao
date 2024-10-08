#!/usr/bin/env python
# coding: utf-8

import cv2
import time
from src.video_config.video_config import VideoConfig
import src.identifier.identifier as identifier
import src.constants.movements as mov
import src.constants.colors as colors
from src.constants.timers import *
from src.constants.constants import *
from src.datatypes.confetti import Confetti
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
    draw_circles,
    draw_points,
    draw_message_center_screen,
    show_image_movements,
    show_player_image,
    apply_filter,
    write_message,
    show_correct_position,
    draw_confetti
)
import random
from database.students.students import select_students
from database.scores.scores import add_score
from typing import List


DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

screen_name = "Identificador de Movimentos"


# laço de repetição que fica rodando durante toda aplicação
class Game:
    def __init__(self):
        self.searching_player = False
        self.player_found = False
        self.is_showing_next_round = False

        self.number_movements = INITIAL_NUMBER_MOVEMENTS
        self.player_seq = 0

        self.confetti_particles: List[Confetti] = []
        
        self.reset_variables()

    def reset_variables(self):
        self.sort_movement = True
        self.is_showing_movements = False
        self.is_movement_wrong = False
        self.is_movement_identified = False
        self.is_draw_circles = False
        self.movement_correct = False

        self.mov_showing_seq = 0
        self.num_circles = 0
    
    def find_expected_player(self):

        if not self.searching_player:
            self.fut_player_search = self.executor.submit(
                self.my_face_recognizer.recognize_faces, self.real_image
            )
            self.searching_player = True

        elif self.fut_player_search.done():
            searched_player = self.fut_player_search.result()
            
            if not searched_player is None: 
                print(f"Player Consultado {searched_player}")
                self.searching_player = False
                if int(searched_player) == self.expected_player:
                    print("Iniciando o Jogo")
                    self.player_found = True

    def player_is_positioned(self):
        self.my_identifier.process_image(self.real_image)
        
        if self.my_identifier.is_correct_positioned():
            self.sort_movement = False
            self.is_showing_movements = True
            self.timer_is_showing_movements = time.perf_counter()
        else:
            self.img = show_correct_position(self.img)

    def show_movement(self):
        self.img = show_image_movements(
            self.img,
            self.my_identifier.command_at(self.mov_showing_seq),
            self.mov_showing_seq + 1,
        )
        
        self.is_draw_circles = True

        delta = time.perf_counter() - self.timer_is_showing_movements

        if delta > TIME_NEXT_MOVE:
            if self.mov_showing_seq < self.my_identifier.qtd_movements() - 1:
                self.timer_is_showing_movements = time.perf_counter()
                self.mov_showing_seq += 1
            else:
                self.is_showing_movements = False

    def show_identified_movement(self):
        if self.movement_correct:
            message_mov = f"{self.my_identifier.seq_command + 1} - {mov.MOVEMENTS_MESSAGE[self.my_identifier.command]}"
            self.img = draw_message(self.img, message_mov)
            
        if self.num_circles == self.my_identifier.seq_command:
            self.num_circles += 1
        
        delta = time.perf_counter() - self.timer_next_mov
        
        if delta > MIN_TIME_SHOW_MOVEMENT:
            if (delta > TIME_SHOW_MOVEMENT or not self.movement_correct):
                if self.my_identifier.has_next_movement():
                    self.my_identifier.next_movement()
                    self.is_movement_identified = False
                    self.is_movement_wrong = False
                    self.timer_next_mov = time.perf_counter()
                else:
                    self.call_next_round()

    def call_next_player(self, add_mov: bool = True):
        self.reset_variables()
        
        self.my_identifier.reset_seq_command()

        if len(self.list_players) == 0:
            print("Não foram identificados jogadores.")
            self.expected_player = None
        else:
            self.player_seq += 1
            if self.player_seq < len(self.list_players):
                self.expected_player = self.list_players[self.player_seq][0]
        
        self.is_showing_next_player = True
        self.timer_show_player = time.perf_counter()
        
    def call_next_round(self):
        self.mov_showing_seq = 0
        self.num_circles = 0
        self.my_identifier.reset_seq_command()

        self.number_movements += 1
        self.my_identifier.list_commands.append(random.randint(1, len(mov.MOVEMENTS)))

        self.is_movement_wrong = False
        self.is_movement_identified = False
        self.sort_movement = True

        self.is_showing_movements = False
        self.is_draw_circles = False
        self.movement_correct = False

        self.is_showing_next_round = True
        self.sort_confetti()
        self.timer_show_player = time.perf_counter()

    def sort_confetti(self):
        self.confetti_particles.clear()
        
        for _ in range(NUMBER_CONFETTI_PARTICLES): 
            x = random.randint(0, self.img.shape[1])
            y = random.randint(-200, self.img.shape[0] // 2)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            speed = random.randint(10, 25)
            
            confetti = Confetti(PosX=x, PosY=y, Color=color, Speed=speed)

            self.confetti_particles.append(confetti)
            
    def show_next_player(self):
        img_player = show_player_image(self.img, self.expected_player)

        if img_player is None:
            return

        self.img = img_player

        delta = time.perf_counter() - self.timer_show_player
        if delta > TIME_SHOW_PLAYER:
            self.is_showing_next_player = False
            self.player_found = False
            
    def show_message_new_round(self):
        self.img = write_message(self.img, "PASSOU DE FASE!")
        
        delta = time.perf_counter() - self.timer_show_player
        
        if delta > TIME_SHOW_PLAYER:
            self.is_showing_next_round = False
            self.player_found = False
        
    def Show(self, width: int, height: int):
        # abre o fluxo de leitura
        # video_conf = VideoConfig(screen_name, "./images/videomaos.mp4") #lê de um vídeo
        video_conf = VideoConfig(screen_name, width=width, height=height)
        video_conf.start()

        self.timer_show_player = time.perf_counter()

        self.my_identifier = identifier.Identifier()
        self.my_identifier.sort_movements(self.number_movements)
        
        self.my_face_recognizer = FaceRecognizer(
            encodings_location=DEFAULT_ENCODINGS_PATH
        )

        self.list_players = select_students()

        self.is_showing_next_player = True
        self.expected_player = int(self.list_players[self.player_seq][0])
        print("---> " + str(self.expected_player))

        with ThreadPoolExecutor(max_workers=4) as self.executor:

            while True:
                if video_conf.stopped is True:
                    break
                else:
                    self.img = video_conf.read()
                    self.real_image = video_conf.real_image()
                    
                    if self.is_draw_circles:
                        draw_circles(self.img, self.number_movements, self.num_circles, self.is_movement_wrong)

                    if len(self.confetti_particles) > 0:
                        self.img = draw_confetti(self.img, self.confetti_particles)
                        self.confetti_particles = [particle for particle in self.confetti_particles if particle.PosY < self.img.shape[0]]
                    
                    # imgRGB = cv2.cvtColor(
                    #     self.img, cv2.COLOR_BGR2RGB
                    # )  # converte a cor para RGB (posso também utilizar essa imagem no processamento)

                    # face_detection(img)
                    # face_mesh(img)
                    if self.is_showing_next_player:
                        self.show_next_player()
                        
                    elif self.is_showing_next_round:
                        self.show_message_new_round()

                    elif not self.player_found:
                        self.find_expected_player()

                    else:
                        self.my_identifier.process_image(self.real_image)
                        # draw_points(self.img, self.my_identifier.points)

                        if self.my_identifier.points:
                            if self.sort_movement:
                                self.player_is_positioned()

                            elif self.is_showing_movements:
                                self.show_movement()

                            elif not self.is_movement_identified and not self.is_movement_wrong:
                                # Verifico se existe a necessidade de realizar um novo sorteio
                                self.movement_correct = (
                                    self.my_identifier.identify_list_movements()
                                )

                                if self.movement_correct is None:
                                    pass
                                elif self.movement_correct:
                                    self.is_movement_wrong = False
                                    self.is_movement_identified = True
                                    self.timer_next_mov = time.perf_counter()
                                elif not self.movement_correct:
                                    self.timer_is_movement_wrong = time.perf_counter()
                                    self.is_movement_wrong = True

                            elif self.is_movement_wrong:
                                add_score((self.number_movements, self.expected_player))
                                delta = (
                                    time.perf_counter() - self.timer_is_movement_wrong
                                )
                                if delta < 4:
                                    self.img = apply_filter(self.img, colors.RED)
                                else:
                                    self.call_next_player(False)
                            elif self.is_movement_identified:
                                self.movement_correct = (
                                    self.my_identifier.identify_list_movements()
                                )
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
