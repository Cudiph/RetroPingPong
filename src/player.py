from importlib.resources import path
import arcade
import os
import settings

ASSET_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'asset') 


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.texture = arcade.load_texture(os.path.join(ASSET_PATH, 'images', 'racket.png'))
        self.scale = settings.PLAYER_SCALE


    def update(self):
        super().update()
        # self.center_x += self.change_x
        # self.center_y += self.change_y

        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0
        elif self.top > settings.SCREEN_HEIGHT - 1:
            self.top = settings.SCREEN_HEIGHT - 1
            self.change_y = 0

