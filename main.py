#!/usr/bin/env python
# coding: utf-8

from src.screens.home import home
from src.constants.constants import DIRECTORY_IMAGE_PLAYER
from pathlib import Path

if __name__ == "__main__":
    Path(DIRECTORY_IMAGE_PLAYER).mkdir(exist_ok=True)
    
    game = home.Game()
    game.HomeScreen()