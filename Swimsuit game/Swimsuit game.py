"""
BEACH BUM BOB BOUNCES BONDI BEACH (or other title)

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
SCREEN_TITLE = "Beach Bum Bob Bounces Bondi Beach"

# Sprite scaling
SPRITE_SCALING_PLAYER = 0.3
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# Physics and movement
MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 15

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 150
BOTTOM_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 100

# These numbers represent "states" that the game can be in.
INSTRUCTIONS_PAGE_0 = 0
INSTRUCTIONS_PAGE_1 = 1
GAME_RUNNING = 2
GAME_OVER = 3

class MyGame(arcade.Window):

    def __init__(self):
        """
        Initializer
        """

        # Call the parent class initializer        
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Start 'state' will be showing the first page of instructions.
        self.current_state = INSTRUCTIONS_PAGE_0
        
        #Variables that will hold sprite lists
        self.player_list = None
        self.wall_list = None
        self.coin_list = None

        #Sprite of player
        self.player_sprite = None

        #No cursor
        self.set_mouse_visible(False)

        # Our physics engine
        self.physics_engine = None
        
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("sounds/coin1.wav")
        self.jump_sound = arcade.load_sound("sounds/jump1.wav")
        
        # Keep track of the score
        self.score = 0
       
        #Background color beyond back ground image
        arcade.set_background_color(arcade.color.SAND)

        # Background image will be stored in this variable
        self.background = None

        # INSTRUCTION PAGES: Put each instruction page in an image. Make sure the image
        # matches the dimensions of the window, or it will stretch and look
        # ugly. You can also do something similar if you want a page between
        # each level.
        self.instructions = []
        texture = arcade.load_texture("images/backgrounds/craftpix/PNG/game_background_2/instructions_0.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("images/backgrounds/craftpix/PNG/game_background_2/instructions_1.png")
        self.instructions.append(texture)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Load the background image. Do this in the setup so we don't keep reloading it all the time.
        self.background = arcade.load_texture("images/backgrounds/craftpix/PNG/game_background_2/game_background_2.png")
        
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        #Sprite Lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        #Setup player
        self.player_sprite = arcade.Sprite("images/player_1/Swimsuit Guy.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 60
        self.player_sprite.center_y = 150
        self.player_list.append(self.player_sprite)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(-1250, 12500, 64):
            wall = arcade.Sprite("images/tiles/tutorial/sandMid.png", TILE_SCALING)
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

        # Use a loop to place some coins for our character to pick up
        for x in range(384, 2500, 256):
            coin = arcade.Sprite("images/items/tutorial/coinGold.png", COIN_SCALING)
            coin.center_x = x
            coin.center_y = 96
            self.coin_list.append(coin)        

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def draw_instructions_page(self, page_number):
        """
        Draw an instruction page. Load the page as an image.
        """
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, page_texture, 0)

    def draw_game_over(self):
        """
        Draw "Game over" across the screen.
        """
        output = "Game Over"
        arcade.draw_text(output, 250 + self.view_left, 400, arcade.color.WHITE, 54)

        output = "Click to restart"
        arcade.draw_text(output, 310 + self.view_left, 300, arcade.color.WHITE, 24)

    def draw_game(self):
        """
        Draw background, all the sprites, along with the score.
        """
        
        # Draw background
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Draw all the sprites
        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)        
    
    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw based on game state.
        if self.current_state == INSTRUCTIONS_PAGE_0:
            self.draw_instructions_page(0)

        elif self.current_state == INSTRUCTIONS_PAGE_1:
            self.draw_instructions_page(1)

        elif self.current_state == GAME_RUNNING:
            self.draw_game()

        else:
            self.draw_game()
            self.draw_game_over()
                    
    def update(self, delta_time):
        """ Movement and game logic """

        # Only move and do things if the game is running.
        if self.current_state == GAME_RUNNING:

            # Call update to move the sprite
            # If using a physics engine, call update on it instead of the sprite
            # list.        
            self.physics_engine.update()

            # See if we hit any coins
            coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                 self.coin_list)

            # Loop through each coin we hit (if any) and remove it
            for coin in coin_hit_list:
                # Remove the coin
                coin.remove_from_sprite_lists()
                # Play a sound
                arcade.play_sound(self.collect_coin_sound)
                # Add one to the score
                self.score += 1


            # If we've collected all the coins, then move to a "GAME_OVER"
            # state.
            if len(self.coin_list) == 0:
                self.current_state = GAME_OVER
                self.set_mouse_visible(True)
                
            # --- Manage Screen Scrolling ---

            # Track if we need to change the viewport
            changed = False

            # Scroll left
            left_boundry = self.view_left + LEFT_VIEWPORT_MARGIN
            if self.player_sprite.left < left_boundry:
                self.view_left -= left_boundry - self.player_sprite.left
                changed = True

            # Scroll right
            right_boundry = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
            if self.player_sprite.right > right_boundry:
                self.view_left += self.player_sprite.right - right_boundry
                changed = True

            # Scroll up
            top_boundry = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
            if self.player_sprite.top > top_boundry:
                self.view_bottom += self.player_sprite.top - top_boundry
                changed = True

            # Scroll down
            bottom_boundry = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
            if self.player_sprite.bottom < bottom_boundry:
                self.view_bottom -= bottom_boundry - self.player_sprite.bottom
                changed = True

            if changed:
                # Only scroll to integers. Otherwise we end up with pixels that
                # don't line up on the screen
                self.view_bottom = int(self.view_bottom)
                self.view_left = int(self.view_left)

                # Do the scrolling
                arcade.set_viewport(self.view_left,
                                    SCREEN_WIDTH + self.view_left,
                                    self.view_bottom,
                                    SCREEN_HEIGHT + self.view_bottom)

            # --- End Manage Scrolling ---
            
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # Change states as needed.
        if self.current_state == INSTRUCTIONS_PAGE_0:
            # Next page of instructions.
            self.current_state = INSTRUCTIONS_PAGE_1
        elif self.current_state == INSTRUCTIONS_PAGE_1:
            # Start the game
            self.setup()
            self.current_state = GAME_RUNNING
        
        # Only move the user if the game is running.
        if self.current_state == GAME_RUNNING:
            if key == arcade.key.UP:
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
                    arcade.play_sound(self.jump_sound)
            elif key == arcade.key.LEFT:
                self.player_sprite.change_x = -MOVEMENT_SPEED
            elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        
        # Only move the user if the game is running.
        if self.current_state == GAME_RUNNING:
            if key == arcade.key.LEFT or key == arcade.key.RIGHT:
                self.player_sprite.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Change states as needed.
        if self.current_state == GAME_OVER:
            # Restart the game.
            self.setup()
            self.current_state = GAME_RUNNING
            
def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
