#!/usr/bin/env python
# coding: utf-8

import pygame
import pygame_gui
from src.screens.game import game
from src.face_recognition.model_recognition import encode_known_faces
from src.globals.variables import Loading_Counter
from threading import Lock
import random
import multiprocessing

class Loading:
    def __init__(self, window_surface, background):
        self.window_surface = window_surface
        self.background = background
        self.manager = pygame_gui.UIManager(
            (self.window_surface.get_width(), self.window_surface.get_height()),
            "src/styles/style.json",
        )
        
        self.lock = Lock()
        self.game = game.Game()

    def Show(self):
        global Loading_Counter
        loading_phrases = [
            "Segure firme! Ação intensa a caminho!",
            "Carregando conhecimento... fique atento!",
            "Preparando desafios para sua mente!",
            "Não vale trapacear, hein!",
            "Pense rápido! Estamos quase prontos para começar!",
            "Um momento... estamos ajustando o aprendizado!",
            "Carregamendo movimentos...",
            "Buscando as respostas no Chat GPT",
            "Aquecendo seus músculos digitais...",
        ]
        
        prg_loading = pygame_gui.elements.UIProgressBar(
            pygame.Rect(0, 0, 800, 50),
            anchors={"centerx": "centerx", "centery": "centery"},  # posicionamento
            manager=self.manager,
        )
        
        label = pygame_gui.elements.UILabel(
            pygame.Rect(0, 50, 600, 100),
            random.choice(loading_phrases),
            self.manager,
            anchors={"centerx": "centerx", "centery": "centery"},
        )

        clock = pygame.time.Clock()
        manager = multiprocessing.Manager()
        shared_Loading_Counter = manager.Value('i', 0)  # 'i' is the typecode for integers
        lock = manager.Lock()
        
        proc = multiprocessing.Process(target=encode_known_faces, args=(shared_Loading_Counter, lock))
        proc.start()
        
        pygame.display.update()
        
        while proc.is_alive():
            time_delta = clock.tick(0.5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    proc.terminate()
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        proc.terminate()
                
                self.manager.process_events(event)

            self.manager.set_window_resolution(
                (self.window_surface.get_width(), self.window_surface.get_height())
            )
            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)
            label.set_text(random.choice(loading_phrases))
            
            with lock:
                prg_loading.set_current_progress(shared_Loading_Counter.value)
            pygame.display.update()
        
        with lock:
            if shared_Loading_Counter.value == 100:
                pygame.display.set_mode(flags=pygame.HIDDEN)
                self.game.Show(*pygame.display.get_window_size())
                pygame.display.set_mode(flags=pygame.SHOWN)
            else:
                proc.terminate()
            