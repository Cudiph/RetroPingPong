from tkinter import CENTER
from turtle import distance
import arcade
import random
from settings import *


class StarList:
    def __init__(self) -> None:
        self.star_list = []
        pass

    def update(self, delta_time):
        for i in self.star_list:
            i.update(delta_time)

    def draw(self):
        for i in self.star_list:
            i.draw()

    def __getitem__(self, index):
        self.star_list[index]

    def append(self, object):
        self.star_list.append(object)


class Star:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.scale = 0.1

    def reset_pos(self):
        self.scale = 0.1
        CENTER_SCREEN = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
        self.x = random.uniform(SCREEN_WIDTH * 0.45, SCREEN_WIDTH * 0.55)
        self.y = random.uniform(SCREEN_HEIGHT * 0.45, SCREEN_HEIGHT * 0.55)

        x_range = max(self.x, CENTER_SCREEN[0]) - min(self.x, CENTER_SCREEN[0])
        y_range = max(self.y, CENTER_SCREEN[1]) - min(self.y, CENTER_SCREEN[1])

        normalized_x = x_range / max(x_range, y_range)
        normalized_y = y_range / max(x_range, y_range)

        if self.x < CENTER_SCREEN[0]:
            normalized_x = -normalized_x
        if self.y < CENTER_SCREEN[1]:
            normalized_y = -normalized_y

        self.change_x = normalized_x * random.uniform(1, 2)
        self.change_y = normalized_y * random.uniform(1, 2)

    def update(self, delta_time):
        self.x += self.change_x
        self.y += self.change_y

        self.scale += delta_time * 0.2

        if self.x > SCREEN_WIDTH or self.x < 0 or self.y > SCREEN_HEIGHT or self.y < 0:
            self.reset_pos()

    def draw(self):
        arcade.draw_circle_filled(
            self.x, self.y, self.scale, arcade.color.WHITE)
