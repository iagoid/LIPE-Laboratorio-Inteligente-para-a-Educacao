#!/usr/bin/env python
# coding: utf-8

from src.screens.home import home
import src.constants.constants as  constants
from pathlib import Path

if __name__ == "__main__":
    Path(constants.DIRECTORY_IMAGE_PLAYER).mkdir(exist_ok=True)
    
    game = home.Game()
    game.HomeScreen()