#!/usr/bin/env python
# coding: utf-8

from src.constants.game_modes import SEQUENCE
from src.constants.movements import *
from src.constants.colors import RED, BLUE, GREEN, YELLOW
from src.screens.game.game import Game
from src.interfaces.game_mode import IGameMode


class SequenceGame(IGameMode, Game):
    def __init__(self):
        Game.__init__(self)

        self.mode = SEQUENCE

    def reset_variables_mode(self):
        pass

    def start(self, width: int, height: int):
        self.Show(width, height, self)

    @property
    def mode(self) -> int:
        return self._mode
    
    @mode.setter
    def mode(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Mode deve ser um inteiro.")
        self._mode = value