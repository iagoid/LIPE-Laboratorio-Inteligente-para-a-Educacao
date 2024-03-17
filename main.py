#!/usr/bin/env python
# coding: utf-8

import cv2
import mediapipe as mp
import numpy as np
import time
import pyautogui
import tkinter as tk
import src.video_config.video_config as video_config
import src.identifier.identifier as identifier
import src.face_recognition.simple_facerec as facerec

from src.face_recognition.face_recognition import face_detection, face_mesh, face_recognition
from src.draw.draw import initial_message, draw_message, draw_points, show_image
from random import *
from datetime import datetime
import src.constants.movements as mov

screen_width = tk.Tk().winfo_screenwidth()
screen_height = tk.Tk().winfo_screenheight()


screen_name = "Identificador de Movimentos"
# abre o fluxo de leitura
# video_conf = video_config.VideoConfig(screen_name, "./images/videomaos.mp4") #lê de um vídeo
video_conf = video_config.VideoConfig(screen_name)
video = video_conf.video

my_facerec = facerec.SimpleFacerec()
my_facerec.load_encoding_images()

# define algumas configurações do mediapipe
mpPose = mp.solutions.pose
pose = mpPose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

t1 = datetime.now()
sort_movement = True
movement_identified = False

command = 0

my_identifier = identifier.Identifier

# laço de repetição que fica rodando durante toda aplicação
while True:
    check, src = video.read()  # lê o vídeo
    if not check:
        break
    img = cv2.flip(src, 1)  # impede o espelhamneto da tela

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # converte a cor para RGB (posso também utilizar essa imagem no processamento)

    # face_detection(img)
    # face_mesh(img)
    
    face_locations, face_names = my_facerec.detect_known_faces(img)
    if len(face_names) > 0:
        print(face_names)
    
    # manda o mediapipe processar a imagem
    result_processing = pose.process(imgRGB)
    # pego os pontos detectados na imagem
    points = result_processing.pose_landmarks

    # if points:  # se foi identificado algum ponto...
    #     mpDraw.draw_landmarks(img, points, mpPose.POSE_CONNECTIONS)
    #     h, w, c = img.shape  # pego as dimensões da tela

    #     # capturo os dados das posições desejadas para este contexto
    #     handRX = points.landmark[mpPose.PoseLandmark.RIGHT_INDEX].x
    #     handRY = points.landmark[mpPose.PoseLandmark.RIGHT_INDEX].y
    #     handLX = points.landmark[mpPose.PoseLandmark.LEFT_INDEX].x
    #     handLY = points.landmark[mpPose.PoseLandmark.LEFT_INDEX].y
    #     noseX = points.landmark[mpPose.PoseLandmark.NOSE].x
    #     noseY = points.landmark[mpPose.PoseLandmark.NOSE].y
    #     shoulderRY = points.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].y
    #     shoulderLY = points.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].y

    #     # Verifico se existe a necessidade de realizar um novo sorteio
    #     delta = datetime.now() - t1
    #     if delta.seconds > 5 or sort_movement:
    #         t1 = datetime.now()
    #         sort_movement = True

    #     # realiza o sorteio do movimento
    #     if sort_movement:
    #         command = randint(1, len(mov.MOVEMENTS))
    #         print(command, mov.MOVEMENTS_IMAGES[command])

    #         sort_movement = False
    #         movement_identified = False
    #         standing_shoulderRY = shoulderRY
    #         standing_shoulderLY = shoulderLY
    #         print(standing_shoulderLY, standing_shoulderRY)
    #         # show_image(img, mov.MOVEMENTS_IMAGES[command-1])

    #     match command:
    #         case mov.LEFT_HAND:
    #             movement_identified = my_identifier.hand_left(handRY, handLY, noseY)

    #         case mov.RIGHT_HAND:
    #             movement_identified = my_identifier.hand_right(handRY, handLY, noseY)

    #         case mov.JUMP:
    #             movement_identified = my_identifier.jump_identifier(
    #                 standing_shoulderRY, standing_shoulderLY, shoulderRY, shoulderLY
    #             )

    #         case mov.CROUCH:
    #             movement_identified = my_identifier.crouch_identifier(
    #                 standing_shoulderRY, standing_shoulderLY, shoulderRY, shoulderLY
    #             )

    #     if movement_identified:
    #         draw_message(img, mov.MOVEMENTS_MESSAGE[command])

    #     draw_points(img, points)
    # else:
    #     initial_message(img)
        
    cv2.imshow(screen_name, img)  # exibe a imagem com os pontos na tela

    # verifica que teclas foram apertadas
    tecla = cv2.waitKey(33) #espera em milisegundos da execução das imagens
    if tecla == 27:  # verifica se foi a tecla esc
        break
    
video.release()
cv2.destroyAllWindows()
