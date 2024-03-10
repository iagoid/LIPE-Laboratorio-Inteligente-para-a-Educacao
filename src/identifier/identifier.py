#!/usr/bin/env python
# coding: utf-8

import cv2
import tkinter as tk


class Identifier:
    def __init__(self):
        pass

    def __str__(self):
        return f"numerador {self.num} e denominador {self.den}"

    def hand_left(handRY, handLY, noseY):
        # distancia levando em consideração apenas a altura
        distMaos = abs(handRY - handLY)

        # se a distância das mãos e dos pés bater nas medidas, ele incrementa as contagens
        if distMaos > 0.5 and not (noseY <= handRY and noseY <= handLY):
            if noseY <= handLY:
                return True

        return False

    def hand_right(handRY, handLY, noseY):
        # distancia levando em consideração apenas a altura
        distMaos = abs(handRY - handLY)

        # se a distância das mãos e dos pés bater nas medidas, ele incrementa as contagens
        if distMaos > 0.5 and not (noseY <= handRY and noseY <= handLY):
            if noseY <= handRY:
                return True

        return False

    def jump_identifier(
        standing_shoulderRY, standing_shoulderLY, shoulderRY, shoulderLY
    ):
        actual_mid_y = (shoulderRY + shoulderLY) / 2
        standing_mid_y = (standing_shoulderRY + standing_shoulderLY) / 2

        # aceita apenas variações de 15% para mais ou menos
        lower_bound = standing_mid_y - (standing_mid_y * 0.15)
        if actual_mid_y < lower_bound:
            return True

        return False

    def crouch_identifier(
        standing_shoulderRY, standing_shoulderLY, shoulderRY, shoulderLY
    ):
        actual_mid_y = (shoulderRY + shoulderLY) / 2
        standing_mid_y = (standing_shoulderRY + standing_shoulderLY) / 2

        # aceita apenas variações de 15% para mais ou menos
        upper_bound = standing_mid_y + (standing_mid_y * 0.15)

        if actual_mid_y > upper_bound:
            return True

        return False
