#!/usr/bin/env python
# coding: utf-8

import cv2
from threading import Thread


class VideoConfig:
    def __str__(self):
        return f"width {self.screen_width}, height {self.screen_height}"

    def __init__(
        self, screen_name: str, width: int, height: int, video_source: int = 0
    ):
        # abre o fluxo de leitura
        self.video = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
        if self.video.isOpened() is False:
            print("[Exiting]: Erro ao acessar a WebCam.")
            exit(0)

        self.set_screen_size(width, height)
        self.video.set(cv2.CAP_PROP_FPS, 30)

        self.grabbed, self.frame = self.video.read()
        if self.grabbed is False:
            print("[Exiting] Não existem mais frames para leitura")
            exit(0)

        self.stopped = True

        self.t = Thread(target=self.update, args=())
        self.t.daemon = True  # daemon threads keep running in the background while the program is executing

        cv2.namedWindow(screen_name)

    def start(self):
        self.stopped = False
        self.t.start()

    def update(self):
        while True:
            if self.stopped is True:
                break
            self.grabbed, self.frame = self.video.read()
            if self.grabbed is False:
                print("[Exiting] Não existem mais frames para leitura")
                self.stopped = True
                break

        self.video.release()

    def set_screen_size(self, screen_width: int, screen_height: int):
        self.screen_width = int(screen_width)
        self.screen_height = int(screen_height)

        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

    def read(self):
        return cv2.flip(self.frame, 1)

    def stop(self):
        self.stopped = True

    def video(self) -> cv2.VideoCapture:
        return self.video

    def height(self) -> int:
        return self.screen_height

    def width(self) -> int:
        return self.screen_width
