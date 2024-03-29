#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np
from PIL import Image
import matplotlib.image as mpimg
import src.constants.colors as colors

primary_font = cv2.FONT_HERSHEY_SIMPLEX
second_font = cv2.FONT_HERSHEY_PLAIN


def draw_rectangle(img, text, text_size, position):
    cv2.rectangle(img, (position[0]-50, position[1]-50), (position[0] +
                  text_size[0]+50, position[1]+text_size[1]+10), colors.ORANGE, -1)
    cv2.putText(img, text, (position[0], position[1]),
                primary_font, 1, colors.WHITE, 2)

def write_center_screen(img, text):
    img_height = img.shape[0]
    img_width = img.shape[1]
    
    text_size = cv2.getTextSize(text, primary_font, 1, 2)[0]
    textX = int((img_width - text_size[0]) / 2)
    textY = int((img_height + text_size[1]) / 2)
    draw_rectangle(img, text, text_size, (textX, textY))

def initial_message(img):
    img_height = img.shape[0]
    img_width = img.shape[1]

    # escreve titulo
    title = 'IDENTIFICADOR DE MAOS'
    title_size = cv2.getTextSize(title, primary_font, 1, 2)[0]
    titleX = int((img_width - title_size[0]) / 2)
    titleY = int((img_height + title_size[1]) / 2)
    draw_rectangle(img, title, title_size, (titleX, titleY))

    # Escreve orientações
    text = 'Aperte \'esc\' para sair'
    text_size = cv2.getTextSize(text, second_font, 1, 1)[0]
    textX = int((img_width - text_size[0]) / 2)
    textY = int((img_height - text_size[1] - 20))
    cv2.putText(img, text, (textX, textY), second_font, 1, colors.WHITE, 1)


def draw_message(img, message):
    cv2.rectangle(img, (1, 0), (260, 30), colors.ORANGE, -1)
    cv2.putText(img, message, (15, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, colors.WHITE, 2)

def draw_points(img, points):
    # um laço de repetição para percorrer todos os pontos e desenhar um círculo e o número do ponto
    for id, lm in enumerate(points.landmark):
        # print(f'ponto: {id}') #imprime os dados do ponto no terminal
        # print(lm);
        # calcula os pontos considerando as dimensões da tela
        cx, cy = int(lm.x * img.shape[1]), int(lm.y * img.shape[0])
        cv2.putText(img, str(int(id)), (cx+5, cy-5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.3, colors.RED, 1)  # escreve o número do ponto
        cv2.circle(img, (cx, cy), 3, colors.RED,
                   cv2.FILLED)  # desenha um círculo
        
        
        
def show_image(img, img_dir):
    img_overlay_rgba = np.array(Image.open(img_dir))

    # Perform blending
    alpha_mask = img_overlay_rgba[:, :, 3] / 255.0
    img_result = img[:, :, :3].copy()
    img_overlay = img_overlay_rgba[:, :, :3]
    
    x = 300
    y = 300
    
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    # Exit if nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    # Blend overlay within the determined ranges
    img_crop = img[y1:y2, x1:x2]
    img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]
    alpha = alpha_mask[y1o:y2o, x1o:x2o, np.newaxis]
    alpha_inv = 1.0 - alpha

    img_crop[:] = alpha * img_overlay_crop + alpha_inv * img_crop