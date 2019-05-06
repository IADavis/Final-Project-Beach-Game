"""
BEACH BUM BOB BOUNCES BONDI BEACH (or other title)

SDEV 140 Spring 2019 - Final Project
Version 0.1.14

Authors:
Andy Olson Moyano
Parker Staph
Isaac Davis

Credits:
Tiles: created using tiled.com
Sprites: created using www.piskelapp.com

"""
import arcade
import os

######################## CONSTANTS ####################
# Screen
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Beach Bum Bob Bounces Bondi Beach"

#Background graphics
NUMBER_BACKGOUNDS = 6
BACKGROUND_SCALE = 0.35
BACKGROUND_WIDTH = 1920 * BACKGROUND_SCALE
BACKGROUND_HEIGHT = 1080 * BACKGROUND_SCALE

# Sprite scaling
SPRITE_SCALING_PLAYER = 0.15
SPRITE_SCALING_PLAYER_NEW = 0.6
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)
SPRITE_SIZE = int(SPRITE_PIXEL_SIZE * SPRITE_SCALING)

# Physics and movement
MOVEMENT_SPEED = 5
GRAVITY = 0.55
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
GAME_WINNER = 4

# Player Start position
PLAYER_START_X = 192
PLAYER_START_Y = 94

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1
TEXTURE_STILL = 2

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
        self.enemy_list = None

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
        self.hurt_sound = arcade.load_sound("sounds/hurt1.wav")
        self.gameover1_sound = arcade.load_sound("sounds/gameover1.wav")
        self.upgrade1_sound = arcade.load_sound("sounds/upgrade1.wav")
        self.upgrade2_sound = arcade.load_sound("sounds/upgrade2.wav")
        
        # Keep track of the score
        self.score = None
       
        #Background color beyond back ground image
        arcade.set_background_color([137,255,255])

        # Background image will be stored in this variable
        self.background = 0

        # INSTRUCTION PAGES: Put each instruction page in an image. Make sure the image
        # matches the dimensions of the window, or it will stretch and look
        # ugly. You can also do something similar if you want a page between
        # each level.
        self.instructions = []
        texture = arcade.load_texture("images/backgrounds/craftpix/PNG/game_background_2/instructions_0.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("images/backgrounds/craftpix/PNG/game_background_2/instructions_1.png")
        self.instructions.append(texture)

        # Define starting level and maximum number of levels
        self.level = 1
        self.max_level = 3

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Load the background image. Do this in the setup so we don't keep reloading it all the time.
        self.background = arcade.load_texture("images/backgrounds/craftpix/PNG/game_background_2/game_background_2.png")
        
        # Keep track of the score
        self.score = 0

        # Define starting level and maximum number of levels
        self.level = 1
        self.max_level = 3
        
        # Sprite Lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()


        # Setup player
        self.player_sprite = arcade.Sprite("images/player_1/Swimsuit Guy.png", SPRITE_SCALING_PLAYER_NEW)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        # Load the level
        self.load_level(self.level)

      
    def load_level(self, level):
        # Read in the tiled map lebel
        my_map = arcade.read_tiled_map(f"level_{level}.tmx", TILE_SCALING)  

        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        
        # Name of the layer that has items for pick-up
        coins_layer_name = 'Coins'

        # Name of the layer that has enemies
        #(doesn;t really have enemies, just clears previous level's enemies from memory)
        enemies_layer_name = 'Enemies'
       
        # -- Walls
        # Grab the layer of items we can't move through
        map_array = my_map.layers_int_data[platforms_layer_name]

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = len(map_array[0]) * GRID_PIXEL_SIZE

        # -- Platforms
        self.wall_list = arcade.generate_sprites(my_map, platforms_layer_name, TILE_SCALING)

        # -- Coins
        self.coin_list = arcade.generate_sprites(my_map, coins_layer_name, TILE_SCALING)

        # -- Enemies
        # Clear previous level enemies
        self.enemy_list = arcade.generate_sprites(my_map, enemies_layer_name, TILE_SCALING)

        for i in self.enemy_list:
            #This sets every single enemy's movement to 2
            i.change_x = 2
            
        # --- Other stuff
        # Set the background color
        if my_map.backgroundcolor:
            arcade.set_background_color(my_map.backgroundcolor)       

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

    def draw_instructions_page(self, page_number):
        """
        Draw an instruction page. Load the page as an image.
        """
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, page_texture, 0)
    
    def draw_game(self):
        """
        Draw background, all the sprites, along with the score.
        """
        
        # Draw in backgrounds
        for i in range(-1, NUMBER_BACKGOUNDS, 1):
            arcade.draw_texture_rectangle(i * BACKGROUND_WIDTH + BACKGROUND_WIDTH // 2, 64 + BACKGROUND_HEIGHT // 2,
                                      BACKGROUND_WIDTH, BACKGROUND_HEIGHT, self.background)

        # Draw all the sprites
        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.enemy_list.draw()

        
        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.color.CADMIUM_RED, 18)        

        # Draw our level on the screen, scrolling it with the viewport
        level_text = f"Level: {self.level}"
        arcade.draw_text(level_text, 120 + self.view_left, 10 + self.view_bottom,
                         arcade.color.CADMIUM_RED, 18)
        
    def draw_game_over(self):
        """
        Draw "Game over" across the screen.
        """
        output = "Game Over"
        arcade.draw_text(output, 250 + self.view_left, 400 + self.view_bottom, arcade.color.CADMIUM_RED, 54)

        output = "Click to restart"
        arcade.draw_text(output, 310 + self.view_left, 300 + self.view_bottom, arcade.color.CADMIUM_RED, 24)

    def draw_game_winner(self):
        """
        Draw "Winner!" across the screen.
        """
        output = "Winner!!"
        arcade.draw_text(output, 285 + self.view_left, 400 + self.view_bottom, arcade.color.CADMIUM_RED, 54)

        output = "Click to restart"
        arcade.draw_text(output, 310 + self.view_left, 300 + self.view_bottom, arcade.color.CADMIUM_RED, 24)
        
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

        elif self.current_state == GAME_OVER:
            self.draw_game()
            self.draw_game_over()
        else:
            self.draw_game()
            self.draw_game_winner()

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

            self.PlayerTexture()

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
        if self.current_state == GAME_OVER or self.current_state == GAME_WINNER:
            # Restart the game.
            self.setup()
            self.current_state = GAME_RUNNING


    def PlayerTexture(self):
##        super().__init__()

        # Load a left facing texture and a right facing texture.
        # mirrored=True will mirror the image we load.
        texture = arcade.load_texture("images/player_1/StandingR.png", mirrored=True, scale=SPRITE_SCALING_PLAYER_NEW)
        self.player_sprite.textures.append(texture)
        texture = arcade.load_texture("images/player_1/StandingR.png", scale=SPRITE_SCALING_PLAYER_NEW)
        self.player_sprite.textures.append(texture)
        texture = arcade.load_texture("images/player_1/Swimsuit Guy.png", scale=SPRITE_SCALING_PLAYER_NEW)
        self.player_sprite.textures.append(texture)

        # Figure out if we should face left or right
        if self.player_sprite.change_x < 0:
             self.player_sprite.set_texture(1)
        elif self.player_sprite.change_x > 0:
             self.player_sprite.set_texture(2)
        else:
             self.player_sprite.set_texture(0)
            
    def update(self, delta_time):
        """ Movement and game logic """
        #print(str(self.player_sprite.center_x) + "," + str(self.player_sprite.center_y))
        
        # Only move and do things if the game is running.
        if self.current_state == GAME_RUNNING:
            # Call update to move the sprite
            # If using a physics engine, call update on it instead of the sprite
            # list.        
            self.physics_engine.update()

            # --- Manage Player ---
            # Track if we need to change the viewport
            changed_viewport = False
            self.PlayerTexture()
            # Did the player fall off the map?
            if self.player_sprite.center_y < -1:
                arcade.play_sound(self.gameover1_sound)
                self.current_state = GAME_OVER
                self.set_mouse_visible(True)            
            

            # --- Manage Coins ---
            
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

            # If we've collected all the coins, then go to next level
            if len(self.coin_list) == 0:
                if self.level < self.max_level:
                    self.level += 1
                    self.load_level(self.level)
                    self.player_sprite.change_x = 0
                    self.player_sprite.change_y = 0
                    self.player_sprite.center_x = PLAYER_START_X
                    self.player_sprite.center_y = PLAYER_START_Y
                    arcade.play_sound(self.upgrade1_sound)
                else:
                    arcade.play_sound(self.upgrade2_sound)
                    self.current_state = GAME_WINNER
                    self.set_mouse_visible(True)

            # --- Manage Enemies ---            
            # Move the enemies
            self.enemy_list.update()
            #Enemy AI
            for enemy in self.enemy_list:
                #Gravity
                self.wallCollide = arcade.check_for_collision_with_list(enemy,self.wall_list)
##                print(str(len(self.wallCollide)))#Remove this line after debug
                if len(self.wallCollide) < 1:
                    enemy.change_x *= -1
                    enemy.change_y = -GRAVITY*10
                else:
                    enemy.change_y = 0

                #Stand on floor
                if len(self.wallCollide) < 3 and len(self.wallCollide) >= 1:
                    for wall in self.wallCollide:
                        topBound = wall.top
                        myBottomBound = enemy.bottom
                        if topBound > myBottomBound:
                            enemy.bottom = topBound-1
                            
                #Change direction when hit wall
                if len(self.wallCollide) >= 3:
                    enemy.change_x *= -1
                    
            #Use this print to figure out where to put enemies by using the player's coords
            #print(str(self.player_sprite.center_x) + "," + str(self.player_sprite.center_y))

            # See if the player hit an enemy If so, game over.
            if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) > 0:
                arcade.play_sound(self.hurt_sound)
                arcade.play_sound(self.gameover1_sound)
                self.current_state = GAME_OVER
                self.set_mouse_visible(True)
       
            
            # --- Manage Screen Scrolling ---
            # Scroll left
            left_boundry = self.view_left + LEFT_VIEWPORT_MARGIN
            if self.player_sprite.left < left_boundry:
                self.view_left -= left_boundry - self.player_sprite.left
                changed_viewport = True

            # Scroll right
            right_boundry = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
            if self.player_sprite.right > right_boundry:
                self.view_left += self.player_sprite.right - right_boundry
                changed_viewport = True

            # Scroll up
            top_boundry = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
            if self.player_sprite.top > top_boundry:
                self.view_bottom += self.player_sprite.top - top_boundry
                changed_viewport = True

            # Scroll down
            bottom_boundry = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
            if self.player_sprite.bottom < bottom_boundry:
                self.view_bottom -= bottom_boundry - self.player_sprite.bottom
                changed_viewport = True

            if changed_viewport:
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
            
def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
