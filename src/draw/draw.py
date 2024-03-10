#!/usr/bin/env python
# coding: utf-8

import cv2
import mediapipe as mp
import numpy as np
import time
import pyautogui
import tkinter as tk
import matplotlib.pyplot as plt

primary_font = cv2.FONT_HERSHEY_SIMPLEX
second_font = cv2.FONT_HERSHEY_PLAIN


def draw_rectangle(img, text, text_size, position):
    cv2.rectangle(img, (position[0]-50, position[1]-50), (position[0] +
                  text_size[0]+50, position[1]+text_size[1]+10), (0, 64, 255), -1)
    cv2.putText(img, text, (position[0], position[1]),
                primary_font, 1, (255, 255, 255), 2)

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
    cv2.putText(img, text, (textX, textY), second_font, 1, (255, 255, 255), 1)


def draw_message(img, message):
    cv2.rectangle(img, (1, 0), (260, 30), (0, 64, 255), -1)
    cv2.putText(img, message, (15, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

def draw_points(img, points):
    # um laço de repetição para percorrer todos os pontos e desenhar um círculo e o número do ponto
    for id, lm in enumerate(points.landmark):
        # print(f'ponto: {id}') #imprime os dados do ponto no terminal
        # print(lm);
        # calcula os pontos considerando as dimensões da tela
        cx, cy = int(lm.x * img.shape[1]), int(lm.y * img.shape[0])
        cv2.putText(img, str(int(id)), (cx+5, cy-5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.3, (255, 0, 0), 1)  # escreve o número do ponto
        cv2.circle(img, (cx, cy), 1, (255, 0, 0),
                   cv2.FILLED)  # desenha um círculo
        
def show_image(img, new_image):

    # reading image
    # new_img_read = cv2.imread(f"../../images/{new_image}")
    new_img_read = cv2.imread("C:\\crouch.png")

    # return cv2.subtract(img, new_img_read)