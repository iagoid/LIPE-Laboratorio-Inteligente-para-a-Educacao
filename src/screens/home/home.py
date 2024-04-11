#!/usr/bin/env python
# coding: utf-8

import pygame
import pygame_gui
from src.screens.players import players
from src.screens.game import game

def HomeScreen():
    pygame.init()

    pygame.display.set_caption("LIFE: Lab of Artificial Inteligence for Education")
    # window_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    window_surface = pygame.display.set_mode((800, 600), pygame.RESIZABLE )

    background = pygame.image.load("images/background.jpg")
    window_surface.blit(background, (0, 0))
    
    manager = pygame_gui.UIManager((window_surface.get_width(), window_surface.get_height()), "src/styles/style.json")

    btn_play = pygame_gui.elements.UIButton(
        pygame.Rect(0, -120, 500, 100),
        "JOGAR",
        manager,
        anchors={"centerx": "centerx", "centery": "centery"},
    )
    
    btn_players = pygame_gui.elements.UIButton(
        pygame.Rect(0, 0, 500, 100),
        "JOGADORES",
        manager,
        anchors={"centerx": "centerx", "centery": "centery"},
    )
    
    btn_quit = pygame_gui.elements.UIButton(
        pygame.Rect(0, 120, 500, 100),
        "SAIR",
        manager,
        anchors={"centerx": "centerx", "centery": "centery"},
    )


    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(10) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == btn_quit:
                    pygame.quit()
                    is_running = False
                elif event.ui_element == btn_play:
                    pygame.display.set_mode(flags=pygame.HIDDEN)
                    game.GameScreen()
                    pygame.display.set_mode(flags=pygame.SHOWN)
                    
                elif event.ui_element == btn_players:
                    pygame.display.set_mode(flags=pygame.HIDDEN)
                    players.PlayersScreen()
                    pygame.display.set_mode(flags=pygame.SHOWN)
                    
            manager.process_events(event)

        manager.set_window_resolution((window_surface.get_width(), window_surface.get_height()))
        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()