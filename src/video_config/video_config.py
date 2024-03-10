#!/usr/bin/env python
# coding: utf-8

import cv2
import tkinter as tk


class VideoConfig:
    def __str__(self):
        return f"width {self.screen_width}, height {self.screen_height}"

    def __init__(self, screen_name, video_source = 0):
        # abre o fluxo de leitura
        self.video = cv2.VideoCapture(video_source)
        cv2.namedWindow(screen_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(screen_name, cv2.WINDOW_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        screen_width = tk.Tk().winfo_screenwidth()
        screen_height = tk.Tk().winfo_screenheight()
        self.set_screen_size(screen_width, screen_height)

    def set_screen_size(self, screen_width, screen_height):
        self.screen_width = int(screen_width)
        self.screen_height = int(screen_height)

        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

    def video(self):
        return self.video

    def height(self):
        return self.screen_height

    def width(self):
        return self.screen_width
