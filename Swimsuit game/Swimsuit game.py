"""
BEACH BUM BOB GOES TO THE BEACH (or other title)

SDEV 140 Spring 2019 - Final Project
Version 1.0

Authors:
Andy Olson Moyano
Parker Staph
Isaac Davis

Credits:
Tiles: created using tiled.com


"""
import arcade
import os

######################## CONSTANTS ####################
# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Beach Bum Bob Goes To The Beach"

# Sprite scaling
SPRITE_SCALING_PLAYER = 0.3
TILE_SCALING = 0.5
PRIZE_SCALING = 0.5

# Physics and movement
MOVEMENT_SPEED = 3
GRAVITY = 1
PLAYER_JUMP_SPEED = 15

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 150
BOTTOM_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 100

class MyGame(arcade.Window):

    def __init__(self):
        """
        Initializer
        """

        # Call the parent class initializer        
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, " ")

        #Variables that will hold sprite lists
        self.player_list = None
        self.wall_list = None
        self.prize_list = None
        self.background = None

        #Sprite of player
        self.player_sprite = None

        #No cursor
        self.set_mouse_visible(False)

        #Background
        arcade.set_background_color(arcade.color.AMAZON)
        self.background = arcade.load_texture("images/backgrounds/Beach background.png")

    def setup(self):
        #sets up game and initializes variables

        #Sprite Lists
        self.player_list = arcade.SpriteList()
        self.prize_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        #Setup player
        self.player_sprite = arcade.Sprite("images/player_1/Swimsuit Guy.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 60
        self.player_sprite.center_y = 150
        self.player_list.append(self.player_sprite)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1250, 64):
            wall = arcade.Sprite("images/tiles/tutorial/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[512, 96],
                           [256, 96],
                           [768, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite("images/tiles/tutorial/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)
        
    def on_draw(self):
        # Renders the screen
        arcade.start_render()
        
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Draw all the sprites
        self.player_list.draw()
        self.wall_list.draw()
        self.prize_list.draw()
        
    def update(self, delta_time):
        """ Movement and game logic """

        # Call update to move the sprite
        # If using a physics engine, call update on it instead of the sprite
        # list.        
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED         
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
