#!/usr/bin/env python
# coding: utf-8

import src.constants.movements as mov
import src.poses.poses as poses
from random import *

# classe que identifica os movimentos do usuário
class Identifier(poses.Poses):
    def __init__(self):
        super().__init__()

    def __str__(self):
        pass

    def process_image(self, img):
        # manda o mediapipe processar a imagem
        result_processing = self.pose.process(img)
        # pego os pontos detectados na imagem
        self.points = result_processing.pose_landmarks

        if self.points:  # se foi identificado algum ponto...
            self.mpDraw.draw_landmarks(img, self.points, self.mpPose.POSE_CONNECTIONS)
            h, w, c = img.shape  # pego as dimensões da tela

            # capturo os dados das posições desejadas para este contexto
            self.handRX = self.points.landmark[self.mpPose.PoseLandmark.RIGHT_INDEX].x
            self.handRY = self.points.landmark[self.mpPose.PoseLandmark.RIGHT_INDEX].y
            self.handLX = self.points.landmark[self.mpPose.PoseLandmark.LEFT_INDEX].x
            self.handLY = self.points.landmark[self.mpPose.PoseLandmark.LEFT_INDEX].y
            self.noseX = self.points.landmark[self.mpPose.PoseLandmark.NOSE].x
            self.noseY = self.points.landmark[self.mpPose.PoseLandmark.NOSE].y
            self.shoulderRY = self.points.landmark[
                self.mpPose.PoseLandmark.RIGHT_SHOULDER
            ].y
            self.shoulderLY = self.points.landmark[
                self.mpPose.PoseLandmark.LEFT_SHOULDER
            ].y

    def hand_left(self):
        # distancia levando em consideração apenas a altura
        distMaos = abs(self.handRY - self.handLY)

        # se a distância das mãos e dos pés bater nas medidas, ele incrementa as contagens
        if distMaos > 0.5 and not (
            self.noseY <= self.handRY and self.noseY <= self.handLY
        ):
            if self.noseY <= self.handLY:
                return True

        return False

    def hand_right(self):
        # distancia levando em consideração apenas a altura
        distMaos = abs(self.handRY - self.handLY)

        # se a distância das mãos e dos pés bater nas medidas, ele incrementa as contagens
        if distMaos > 0.5 and not (
            self.noseY <= self.handRY and self.noseY <= self.handLY
        ):
            if self.noseY <= self.handRY:
                return True

        return False

    def jump_identifier(self):
        actual_mid_y = (self.shoulderRY + self.shoulderLY) / 2
        standing_mid_y = (self.standing_shoulderRY + self.standing_shoulderLY) / 2

        # aceita apenas variações de 15% para mais ou menos
        lower_bound = standing_mid_y - (standing_mid_y * 0.15)
        if actual_mid_y < lower_bound:
            return True

        return False

    def crouch_identifier(self):
        actual_mid_y = (self.shoulderRY + self.shoulderLY) / 2
        standing_mid_y = (self.standing_shoulderRY + self.standing_shoulderLY) / 2

        # aceita apenas variações de 15% para mais ou menos
        upper_bound = standing_mid_y + (standing_mid_y * 0.15)

        if actual_mid_y > upper_bound:
            return True

        return False

    def sort_movement(self):
        self.command = randint(1, len(mov.MOVEMENTS))
        self.standing_shoulderRY = self.shoulderRY
        self.standing_shoulderLY = self.shoulderLY
        
        print(mov.MOVEMENTS_ORDER[self.command])
        # show_image(img, "images/" + mov.MOVEMENTS_IMAGES[command])
            
    def identify(self):
        match self.command:
            case mov.LEFT_HAND:
                return self.hand_left()

            case mov.RIGHT_HAND:
                return self.hand_right()

            case mov.JUMP:
                return self.jump_identifier()

            case mov.CROUCH:
                return self.crouch_identifier()
