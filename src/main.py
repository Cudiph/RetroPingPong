import arcade
import random
from ball import Ball
from player import Player
from settings import *


class RetroPingPong(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.csscolor.BLACK)
        arcade.enable_timings()
        
        self.player1_sprite = Player()
        self.player2_sprite = Player()
        self.player_sprites = arcade.SpriteList()
        self.ball_sprites = arcade.SpriteList()
        self.current_event = None

    def on_draw(self):
        self.clear()
        self.player_sprites.draw()
        self.draw_score()
        self.ball_sprites.draw()
        arcade.draw_text(f'fps: {arcade.get_fps() // 1}', 10, self.height - 20, arcade.color.WHITE, 16)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.close()

        # player 1 control
        if symbol == arcade.key.A or symbol == arcade.key.W:
            self.player1_sprite.change_y = PLAYER_SPEED
        elif symbol == arcade.key.S or symbol == arcade.key.D:
            self.player1_sprite.change_y = -PLAYER_SPEED

        # player 2 control
        if not USING_AI:
            if symbol == arcade.key.UP or symbol == arcade.key.LEFT:
                self.player2_sprite.change_y = PLAYER_SPEED
            elif symbol == arcade.key.DOWN or symbol == arcade.key.RIGHT:
                self.player2_sprite.change_y = -PLAYER_SPEED
        

        if symbol == arcade.key.F1:
            pass
            # print(self.player1_sprite.left)

    def on_key_release(self, symbol: int, modifiers: int):
        # player 1
        if symbol == arcade.key.A or symbol == arcade.key.W:
            self.player1_sprite.change_y = 0
        elif symbol == arcade.key.S or symbol == arcade.key.D:
            self.player1_sprite.change_y = 0

        # player 2
        if not USING_AI:
            if symbol == arcade.key.UP or symbol == arcade.key.LEFT:
                self.player2_sprite.change_y = 0
            elif symbol == arcade.key.DOWN or symbol == arcade.key.RIGHT:
                self.player2_sprite.change_y = 0


    def on_update(self, delta_time: float):
        self.player_sprites.update()
        self.ball_sprites.update()

        # collission detection
        collide_with_p1: list[Ball] = self.player1_sprite.collides_with_list(self.ball_sprites)
        collide_with_p2: list[Ball] = self.player2_sprite.collides_with_list(self.ball_sprites)
        if collide_with_p1:
            for ball in collide_with_p1:
                ball.change_x = -ball.change_x
        elif collide_with_p2:
            for ball in collide_with_p2:
                ball.change_x = -ball.change_x

        # score system
        for ball_sprite in self.ball_sprites:
            if ball_sprite.left < 0:
                self.score2 += 1
                ball_sprite.kill()
                self.spawn_ball()
            elif ball_sprite.right > self.width:
                self.score1 += 1
                ball_sprite.kill()
                self.spawn_ball()
        
        if USING_AI:
            self.handle_AI(self.player2_sprite, delta_time)

        if isinstance(self.current_event, arcade.PhysicsEnginePlatformer):
            self.current_event.update()

    def distance(self, sprite1: arcade.Sprite, sprite2: arcade.Sprite):
        return (abs(sprite1.center_x - sprite2.center_x) ** 2 + abs(sprite1.center_y - sprite2.center_y) ** 2) ** 0.5

    def handle_AI(self, player_sprite: arcade.Sprite, delta_time: float):
        nearest_ball = None
        in_right = player_sprite.position[0] > self.width / 2

        # search for nearest ball that come to the player
        for ball in self.ball_sprites:
            if nearest_ball == None:
                nearest_ball = ball

            NEAREST_BALL_DISTANCE = self.distance(player_sprite, nearest_ball)
            ball_distance = 100000
            if ball.change_x > 0 and in_right:
                ball_distance = self.distance(ball, player_sprite)
            elif ball.change_x < 0 and not in_right:
                ball_distance = self.distance(ball, player_sprite)

            if NEAREST_BALL_DISTANCE > ball_distance:
                nearest_ball = ball

        x_ball = nearest_ball.center_x
        y_ball = nearest_ball.center_y

        if player_sprite.center_y > y_ball:
            player_sprite.center_y -= PLAYER_SPEED
        elif player_sprite.center_y < y_ball:
            player_sprite.center_y += PLAYER_SPEED

    
    def setup(self):
        self.score1 = 0
        self.score2 = 0

        # player 1 on the left
        self.player1_sprite.center_y = self.height / 2
        self.player1_sprite.left = 80
        self.player_sprites.append(self.player1_sprite)

        # player 2 on the right
        self.player2_sprite.center_y = self.height / 2
        self.player2_sprite.left = self.width - 100
        self.player_sprites.append(self.player2_sprite)

        self.spawn_ball()
        arcade.schedule(self.rand_event, 5)

        

    def spawn_ball(self):
        ball_sprite = Ball()
        RANDOM_NUM = random.randint(0,1)

        xspeed = 0
        yspeed = 0
        center_x = 0
        center_y = 0

        if RANDOM_NUM:
            xspeed = random.randrange(8, 13)
            yspeed = random.choice([x for x in range(-15, -3)] + [x for x in range(3, 15)])
            center_x = self.player1_sprite.center_x + 5
            center_y = self.player1_sprite.center_y
        else:
            xspeed = random.randrange(-13, -8)
            yspeed = random.choice([x for x in range(-15, -3)] + [x for x in range(3, 15)])
            center_x = self.player2_sprite.center_x - 5
            center_y = self.player2_sprite.center_y

        ball_sprite.center_x = center_x
        ball_sprite.center_y = center_y
        # ball_sprite.change_x = xspeed
        # ball_sprite.change_y = yspeed
        ball_sprite.velocity = [xspeed, yspeed]
        
        self.ball_sprites.append(ball_sprite)
      

    def draw_score(self):
        arcade.draw_text(str(self.score1), self.width / 2 / 2, self.height / 2 * 1.5, arcade.color.WHITE, 40)
        arcade.draw_text(str(self.score2), self.width / 2 * 1.5, self.height / 2 * 1.5 , arcade.color.WHITE, 40)

    def rand_event(self, delta_time):
        self.current_event = None

        RANDOM_NUM = random.randrange(0, 1)

        # add gravity
        if RANDOM_NUM == 0:
            self.spawn_ball()
            pass
        elif RANDOM_NUM == 1:
            pass
            # self.current_event = arcade.PhysicsEnginePlatformer(self.ball_sprite, gravity_constant=0.1)



def main():
    app = RetroPingPong(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    app.setup()
    arcade.run()


if __name__ == "__main__":
    main()