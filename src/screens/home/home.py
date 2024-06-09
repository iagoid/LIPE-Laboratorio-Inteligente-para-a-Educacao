#!/usr/bin/env python
# coding: utf-8

import pygame
import pygame_gui
from src.screens.players import players
from src.screens.game import game


class HomeScreen:
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
        self.game = game.Game()

    def Show(self):

        btn_play = pygame_gui.elements.UIButton(
            pygame.Rect(0, -120, 500, 100),
            "JOGAR",
            self.manager,
            anchors={"centerx": "centerx", "centery": "centery"},
        )

        btn_players = pygame_gui.elements.UIButton(
            pygame.Rect(0, 0, 500, 100),
            "JOGADORES",
            self.manager,
            anchors={"centerx": "centerx", "centery": "centery"},
        )

        btn_quit = pygame_gui.elements.UIButton(
            pygame.Rect(0, 120, 500, 100),
            "SAIR",
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
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        is_running = False

                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == btn_quit:
                        is_running = False

                    elif event.ui_element == btn_play:
                        pygame.display.set_mode(flags=pygame.HIDDEN)
                        self.game.Show(*pygame.display.get_window_size())
                        pygame.display.set_mode(flags=pygame.SHOWN)

                    elif event.ui_element == btn_players:
                        pygame.display.set_mode(flags=pygame.HIDDEN)
                        self.player_screen.Show(*pygame.display.get_window_size())
                        pygame.display.set_mode(flags=pygame.SHOWN)

                self.manager.process_events(event)

            self.manager.set_window_resolution(
                (self.window_surface.get_width(), self.window_surface.get_height())
            )
            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)

            pygame.display.update()

        pygame.quit()
