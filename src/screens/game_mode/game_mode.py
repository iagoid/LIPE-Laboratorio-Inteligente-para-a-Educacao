#!/usr/bin/env python
# coding: utf-8

import pygame
import pygame_gui
from src.screens.players import players
from src.screens.loading import loading
from src.screens.game.condition_game import ConditionGame
from src.screens.game.sequence_game import SequenceGame
from src.constants.constants import DEVELOP_MODE

class GameMode:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("LIFE: Lab of Artificial Inteligence for Education")
        self.window_surface = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        
        self.background = pygame.image.load("images/background.jpg")
        self.window_surface.blit(self.background, (0, 0))
        self.manager = pygame_gui.UIManager(
            (self.window_surface.get_width(), self.window_surface.get_height()),
            "src/styles/style.json",
        )

        self.player_screen = players.PlayerScreen()

    def Show(self):
        btn_back = pygame_gui.elements.UIButton(
            pygame.Rect(5, 5, 150, 50),
            "VOLTAR",
            self.manager,
            anchors={"left": "left", "top": "top"},
        )
        
        btn_sequence = pygame_gui.elements.UIButton(
            pygame.Rect(0, -120, 500, 100),
            "SEQUÊNCIA",
            self.manager,
            anchors={"centerx": "centerx", "centery": "centery"},
        )

        btn_condition = pygame_gui.elements.UIButton(
            pygame.Rect(0, 0, 500, 100),
            "CONDIÇÃO",
            self.manager,
            anchors={"centerx": "centerx", "centery": "centery"},
        )

        btn_iteration = pygame_gui.elements.UIButton(
            pygame.Rect(0, 120, 500, 100),
            "ITERAÇÃO",
            self.manager,
            anchors={"centerx": "centerx", "centery": "centery"},
        )

        clock = pygame.time.Clock()
        is_running = True

        while is_running:
            time_delta = clock.tick(10) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == btn_back:
                        is_running = False
                        
                    elif event.ui_element == btn_sequence:
                        self.game = SequenceGame()
                        
                        if DEVELOP_MODE:
                            self.game.start(*pygame.display.get_window_size())
                        else:
                            self.loading = loading.Loading(self.window_surface, self.background)
                            self.loading.Show(self.game)

                    elif event.ui_element == btn_condition:
                        self.game = ConditionGame()
                            
                        if DEVELOP_MODE:
                            self.game.start(*pygame.display.get_window_size())
                        else:
                            self.loading = loading.Loading(self.window_surface, self.background)
                            self.loading.Show(self.game)
                        
                    elif event.ui_element == btn_iteration:
                        # self.game = IterationGame()
                        # if DEVELOP_MODE:
                        #     self.game.start(*pygame.display.get_window_size())
                        #     pass
                        # else:
                        #     self.loading = loading.Loading(self.window_surface, self.background)
                        #     self.loading.Show(self.game)
                        pass
                        
                self.manager.process_events(event)

            self.manager.set_window_resolution(
                (self.window_surface.get_width(), self.window_surface.get_height())
            )
            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)

            pygame.display.update()

        pygame.event.clear()