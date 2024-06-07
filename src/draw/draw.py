#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import matplotlib.image as mpimg
import src.constants.colors as colors
from cv2.typing import MatLike
import cvzone
import src.constants.movements as mov
from src.constants.fonts import PRIMARY_FONT, SECONDARY_FONT, FONT_SUPER_SQUAD_PATH

# TODO: Revisar todas os textos mostrados em tela para utilizar o PIL
def draw_rectangle(img: MatLike, text: str, text_size, position):
    cv2.rectangle(
        img,
        (position[0] - 50, position[1] - 50),
        (position[0] + text_size[0] + 50, position[1] + text_size[1] + 10),
        colors.ORANGE,
        -1,
    )
    cv2.putText(img, text, (position[0], position[1]), PRIMARY_FONT, 1, colors.WHITE, 2)


def write_center_screen(img: MatLike, text: str):
    img_height = img.shape[0]
    img_width = img.shape[1]

    text_size = cv2.getTextSize(text, PRIMARY_FONT, 1, 2)[0]
    textX = int((img_width - text_size[0]) / 2)
    textY = int((img_height + text_size[1]) / 2)
    draw_rectangle(img, text, text_size, (textX, textY))


def initial_message(img: MatLike):
    img_height = img.shape[0]
    img_width = img.shape[1]

    # escreve titulo
    title = "IDENTIFICADOR DE MAOS"
    title_size = cv2.getTextSize(title, PRIMARY_FONT, 1, 2)[0]
    titleX = int((img_width - title_size[0]) / 2)
    titleY = int((img_height + title_size[1]) / 2)
    draw_rectangle(img, title, title_size, (titleX, titleY))

    # Escreve orientações
    text = "Aperte 'esc' para sair"
    text_size = cv2.getTextSize(text, SECONDARY_FONT, 1, 1)[0]
    textX = int((img_width - text_size[0]) / 2)
    textY = int((img_height - text_size[1] - 20))
    cv2.putText(img, text, (textX, textY), SECONDARY_FONT, 1, colors.WHITE, 1)


def draw_message(img: MatLike, message: str):
    cv2.rectangle(img, (1, 0), (260, 30), colors.ORANGE, -1)
    
    pil_image = Image.fromarray(img)
    
    font = ImageFont.truetype(FONT_SUPER_SQUAD_PATH, size=15)
    draw = ImageDraw.Draw(pil_image)
    
    draw.text(
        (15, 5), message, font=font, stroke_width=1, stroke_fill=colors.BLACK
    )
    return np.asarray(pil_image)
    


def draw_points(img: MatLike, points):
    # um laço de repetição para percorrer todos os pontos e desenhar um círculo e o número do ponto
    for id, lm in enumerate(points.landmark):
        # print(f'ponto: {id}') #imprime os dados do ponto no terminal
        # print(lm);
        # calcula os pontos considerando as dimensões da tela
        cx, cy = int(lm.x * img.shape[1]), int(lm.y * img.shape[0])
        cv2.putText(
            img,
            str(int(id)),
            (cx + 5, cy - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.3,
            colors.RED,
            1,
        )  # escreve o número do ponto
        cv2.circle(img, (cx, cy), 3, colors.RED, cv2.FILLED)  # desenha um círculo


def show_image_movements(img: MatLike, command: int, seq:int = None):
    image_filter = apply_filter(img)
    
    img_movement = cv2.imread(
        "images/" + mov.MOVEMENTS_IMAGES[command], cv2.IMREAD_UNCHANGED
    )
    img_movement = cv2.resize(img_movement, (0, 0), None, 0.5, 0.5)

    h_background, w_ackground, _ = image_filter.shape
    h_img_mov, w_img_mov, _ = img_movement.shape

    pos_x = (w_ackground - w_img_mov) // 2
    pos_y = (h_background - h_img_mov) // 2
    cvzone.overlayPNG(image_filter, img_movement, [pos_x, pos_y])

    pil_image = Image.fromarray(image_filter)

    if seq:
        order = f"{seq} - {mov.MOVEMENTS_ORDER[command]}"
    else:
        order = mov.MOVEMENTS_ORDER[command]

    font = ImageFont.truetype(FONT_SUPER_SQUAD_PATH, size=25)
    draw = ImageDraw.Draw(pil_image)

    _, _, text_width, text_height = font.getbbox(text=order, stroke_width=1)

    textX = int((w_ackground - text_width) / 2)
    textY = int(pos_y + h_img_mov)
    draw.text(
        (textX, textY), order, font=font, stroke_width=1, stroke_fill=colors.BLACK
    )
    image = np.asarray(pil_image)

    return image


def apply_filter(img: MatLike) -> MatLike:
    blue_layer = np.full(img.shape, colors.RED_LIGHT, dtype=np.uint8)
    
    blended_img = cv2.addWeighted(img, 0.5, blue_layer, 0.5, 0)
    
    return blended_img


def draw_face_positioning(img: MatLike) -> MatLike:
    height, width, _ = img.shape
    center_coordinates = (width // 2, height // 2)
    axesLength = (width // 3 - 100, height // 3)
    angle = 90
    startAngle = 0
    endAngle = 360
    thickness = -1

    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.ellipse(
        mask, center_coordinates, axesLength, angle, startAngle, endAngle, 255, -1
    )
    return cv2.bitwise_and(img, img, mask=mask)


def NextPlayer(img: MatLike) -> MatLike:
    img_height, img_width, _ = img.shape
    text = "PRÓXIMO JOGADOR"

    pil_image = Image.fromarray(img)

    # Draw non-ascii text onto image
    font = ImageFont.truetype(FONT_SUPER_SQUAD_PATH, size=40)
    draw = ImageDraw.Draw(pil_image)

    _, _, text_width, text_height = font.getbbox(text=text, stroke_width=1)
    textX = int((img_width - text_width) / 2)
    textY = int((img_height - text_height - 50))
    draw.text((textX, textY), text, font=font, stroke_width=1, stroke_fill=colors.BLACK)

    image = np.asarray(pil_image)
    return image
