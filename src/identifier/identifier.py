#!/usr/bin/env python
# coding: utf-8

import src.constants.movements as mov
import src.poses.poses as poses
import random
from cv2.typing import MatLike


# classe que identifica os movimentos do usuário
class Identifier(poses.Poses):
    def __init__(self):
        self.MOVEMENTS_METHODS = [
            self.hand_left,
            self.hand_right,
            self.jump_identifier,
            self.crouch_identifier,
        ]

        super().__init__()

    def __str__(self):
        pass

    def process_image(self, img: MatLike):
        # manda o mediapipe processar a imagem
        copy_image = img.copy()
        result_processing = self.pose.process(copy_image)
        # pego os pontos detectados na imagem
        self.points = result_processing.pose_landmarks

        if self.points:  # se foi identificado algum ponto...
            self.mpDraw.draw_landmarks(
                copy_image, self.points, self.mpPose.POSE_CONNECTIONS
            )

            # capturo os dados das posições desejadas para este contexto
            self.handRX = float(
                self.points.landmark[self.mpPose.PoseLandmark.RIGHT_INDEX].x
            )
            self.handRY = float(
                self.points.landmark[self.mpPose.PoseLandmark.RIGHT_INDEX].y
            )
            self.handLX = float(
                self.points.landmark[self.mpPose.PoseLandmark.LEFT_INDEX].x
            )
            self.handLY = float(
                self.points.landmark[self.mpPose.PoseLandmark.LEFT_INDEX].y
            )
            self.noseX = float(self.points.landmark[self.mpPose.PoseLandmark.NOSE].x)
            self.noseY = float(self.points.landmark[self.mpPose.PoseLandmark.NOSE].y)
            self.shoulderRY = float(
                self.points.landmark[self.mpPose.PoseLandmark.RIGHT_SHOULDER].y
            )
            self.shoulderLY = float(
                self.points.landmark[self.mpPose.PoseLandmark.LEFT_SHOULDER].y
            )

    def hand_left(self) -> bool:
        # distancia levando em consideração apenas a altura
        distMaos = abs(self.handRY - self.handLY)

        # se a distância das mãos e dos pés bater nas medidas, ele incrementa as contagens
        if distMaos > 0.5:
            if self.noseY >= self.handRY:
                return False
            if self.noseY >= self.handLY:
                return True

        return False

    def hand_right(self) -> bool:
        # distancia levando em consideração apenas a altura
        distMaos = abs(self.handRY - self.handLY)

        # se a distância das mãos e dos pés bater nas medidas, ele incrementa as contagens
        if distMaos > 0.5:
            if self.noseY >= self.handLY:
                return False
            if self.noseY >= self.handRY:
                return True

        return False

    def jump_identifier(self) -> bool:
        actual_mid_y = (self.shoulderRY + self.shoulderLY) / 2

        # aceita variações de menos de 30%
        lower_bound = self.standing_mid_y - (self.standing_mid_y * 0.30)

        if actual_mid_y < lower_bound:
            return True

        return False

    def crouch_identifier(self) -> bool:
        actual_mid_y = (self.shoulderRY + self.shoulderLY) / 2

        # aceita variações de mais de 30%
        upper_bound = self.standing_mid_y + (self.standing_mid_y * 0.3)

        if actual_mid_y > upper_bound:
            return True

        return False

    def sort_movements(self, height: float, qtd: int = 1):
        if self.shoulderRY == 0 or self.shoulderLY == 0:
            self.standing_mid_y = 0.8
        else:
            mid_shoulders = (self.shoulderRY + self.shoulderLY) // 2
            # verifica se a altura dos ombros está aceitavel
            if (mid_shoulders > height * 0.85) or (mid_shoulders < height * 0.65):
                self.standing_mid_y = 0.8
            else:
                self.standing_mid_y = mid_shoulders

        self.list_commands = []
        for i in range(qtd):
            self.list_commands.append(random.randint(1, len(mov.MOVEMENTS)))

        self.seq_command = 0
        self.command = self.list_commands[self.seq_command]

    def identify(self) -> bool:
        match self.command:
            case mov.LEFT_HAND:
                return self.hand_left()

            case mov.RIGHT_HAND:
                return self.hand_right()

            case mov.JUMP:
                return self.jump_identifier()

            case mov.CROUCH:
                return self.crouch_identifier()

    def identify_list_movements(self) -> bool | None:

        print(f"Movimento {self.command}")
        if self.MOVEMENTS_METHODS[self.command - 1]():
            return True

        for i, fn in enumerate(self.MOVEMENTS_METHODS):
            if fn():
                print(
                    f"Movimento Esperado: {mov.MOVEMENTS_ORDER[self.command]}. Retornado {mov.MOVEMENTS_ORDER[i+1]}"
                )
                return False

        return None

    def qtd_movements(self) -> int:
        return len(self.list_commands)

    def seq_command(self) -> int:
        return self.seq_command

    def command_at(self, pos: int) -> int:
        return self.list_commands[pos]

    def points(self):
        return self.points

    def next_movement(self):
        self.seq_command += 1
        self.command = self.list_commands[self.seq_command]
