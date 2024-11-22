#!/usr/bin/env python
# coding: utf-8

from src.constants.game_modes import SEQUENCE
from src.constants.movements import *
from src.constants.colors import RED, BLUE, GREEN, YELLOW
from src.screens.game.game import Game
from src.interfaces.game_mode import IGameMode
from src.draw.draw import (
    show_image_movements,
)
import time
from src.constants.constants import *
from src.constants.timers import *


class SequenceGame(IGameMode, Game):
    def __init__(self):
        Game.__init__(self)

        self._mode = SEQUENCE
        self._list_movements = [LEFT_HAND, RIGHT_HAND, JUMP, CROUCH]

    def show_movement(self):
        self.img = show_image_movements(
            img=self.img,
            command=self.my_identifier.command_at(self.mov_showing_seq),
            seq=self.mov_showing_seq + 1,
        )

        self.is_draw_circles = True

        delta = time.perf_counter() - self.timer_is_showing_movements

        if delta > TIME_NEXT_MOVE:
            if self.mov_showing_seq < self.my_identifier.qtd_movements() - 1:
                self.timer_is_showing_movements = time.perf_counter()
                self.mov_showing_seq += 1
            else:
                self.is_showing_movements = False

    def reset_variables_mode(self):
        pass

    def start(self, width: int, height: int):
        self.Show(width, height, self)

    @property
    def mode(self) -> int:
        return self._mode
    
    @property
    def list_movements(self) -> list[int]:
        return self._list_movements
