import arcade
import os

SPRITE_SCALING_PLAYER = 0.3
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 3

class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, " ")

        #Lists
        self.player_list = None
        self.background = None

        #Sptite of player
        self.player_sprite = None

        #No cursor
        self.set_mouse_visible(False)

        #Background
        arcade.set_background_color(arcade.color.AMAZON)
        self.background = arcade.load_texture("Beach background.png")

    def setup(self):
        #sets up game and initialzes

        self.player_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite("Swimsuit Guy.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 60
        self.player_sprite.center_y = 150
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.player_list.draw()

    def update(self, delta_time):
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
