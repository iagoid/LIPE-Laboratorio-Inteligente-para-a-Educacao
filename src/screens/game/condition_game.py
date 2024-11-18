#!/usr/bin/env python
# coding: utf-8

from src.constants.game_modes import CONDITION
from src.constants.movements import *
from src.constants.colors import RED, BLUE, GREEN, YELLOW
from src.screens.game.game import Game
import random
from src.interfaces.game_mode import IGameMode


class ConditionGame(IGameMode, Game):
    def __init__(self):
        Game.__init__(self)

        self.mode = CONDITION

    def color_move_representation(self):
        colors = [RED, BLUE, GREEN, YELLOW]

        move_in_colors = {}

        for i in range(1, len(colors)):
            rand_color = random.choice(colors)
            move_in_colors[i] = rand_color
            colors.remove(rand_color)

    def reset_variables_mode(self):
        self.color_move_representation()

    def start(self, width: int, height: int):
        Game.Show(width, height, self)
        
    @property
    def mode(self) -> int:
        return self._mode
    
    @mode.setter
    def mode(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Mode deve ser um inteiro.")
        self._mode = value
