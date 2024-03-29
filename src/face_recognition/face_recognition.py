#!/usr/bin/env python
# coding: utf-8

import cv2
import mediapipe as mp
import face_recognition
import src.constants.colors as colors


def face_detection(img):
    fc_recognition = mp.solutions.face_detection # ativando a solução de reconhecimento de rosto
    recognizer = fc_recognition.FaceDetection() # criando o item que consegue ler uma img e reconhecer os rostos ali dentro

    faces_list = recognizer.process(img) # usa o reconhecedor para criar uma lista com os rostos reconhecidos
    mpDraw = mp.solutions.drawing_utils
    
    if faces_list.detections: # caso algum rosto tenha sido reconhecido
        for facial_landmarks in faces_list.detections: # para cada rosto que foi reconhecido
            mpDraw.draw_detection(img, facial_landmarks) # desenha o rosto na img
            
def face_mesh(img):
    fc_recognition = mp.solutions.face_mesh # ativando a solução de reconhecimento de rosto
    recognizer = fc_recognition.FaceMesh() # criando o item que consegue ler uma img e reconhecer os rostos ali dentro

    faces_list = recognizer.process(img) # usa o reconhecedor para criar uma lista com os rostos reconhecidos
    
    if faces_list.multi_face_landmarks: # caso algum rosto tenha sido reconhecido
        for facial_landmarks in faces_list.multi_face_landmarks: # para cada rosto que foi reconhecido
            for i in range (0, len(facial_landmarks.landmark)):
                pt = facial_landmarks.landmark[i]
                x = int(pt.x * img.shape[1])
                y = int(pt.y * img.shape[0])
                
                cv2.circle(img, (x, y), 3, colors.BLUE, -1)
                
                
def face_recognition(img):
    img_encoding = face_recognition.face_encodings(img)[0]
    
    img_to_recognize = cv2.imread("../../images/alan turing.png")
    rgb_img2 = cv2.cvtColor(img_to_recognize, cv2.COLOR_BGR2RGB)
    img_rec_encoding = face_recognition.face_encodings(rgb_img2)[0]
    
    result = face_recognition.compare_faces([img_encoding], img_rec_encoding)
    print("Result: ", result)
    