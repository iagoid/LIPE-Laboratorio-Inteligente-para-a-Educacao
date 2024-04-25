#!/usr/bin/env python
# coding: utf-8

import cv2
import tkinter as tk


class VideoConfig:
    def __str__(self):
        return f"width {self.screen_width}, height {self.screen_height}"

    def __init__(
        self, screen_name: str, width: int, height: int, video_source: int = 0
    ):
        # abre o fluxo de leitura
        self.video = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
        self.set_screen_size(width, height)
        self.video.set(cv2.CAP_PROP_FPS, 30)

        cv2.namedWindow(screen_name)

    def set_screen_size(self, screen_width: int, screen_height: int):
        self.screen_width = int(screen_width)
        self.screen_height = int(screen_height)

        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

    def video(self) -> cv2.VideoCapture:
        return self.video

    def height(self) -> int:
        return self.screen_height

    def width(self) -> int:
        return self.screen_width
