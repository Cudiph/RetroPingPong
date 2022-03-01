import arcade
import os
import settings
from player import ASSET_PATH

class Ball(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.texture = arcade.load_texture(os.path.join(ASSET_PATH, 'images', 'ball.png'))
        self.scale = 0.3
        self.center_x = settings.SCREEN_WIDTH / 2
        self.center_y = settings.SCREEN_HEIGHT / 2

    def update(self):
        super().update()
        # self.center_x += self.change_x
        # self.center_y += self.change_y

        if self.top > settings.SCREEN_HEIGHT - 1:
            self.change_y = -self.change_y
        elif self.bottom < 0:
            self.change_y = -self.change_y