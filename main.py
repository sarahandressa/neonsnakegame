"""
Neon Snake Game
Developed for CSE 310 - Applied Programming.
This game demonstrates basic game development principles using the Python Arcade library.
It covers object-oriented programming, event handling, and game state management.

"""

import arcade
import random
from constants import *

class SnakeSegment(arcade.Sprite):
    """
    Represents a single block/segment of the snake.
    Inherits from arcade.Sprite for easy rendering and position management.
    """
    def __init__(self, x, y, color):
        # Create a solid color rectangle as the sprite image
        super().__init__()
        self.texture = arcade.make_soft_square_texture(SQUARE_SIZE, color, outer_alpha=255)
        self.center_x = x
        self.center_y = y

class Food(arcade.Sprite):
    """
    Represents the food item the snake tries to eat.
    Generated procedurally to avoid dependency on external image files.
    """
    def __init__(self):
        # Create a procedural texture (red square) for the food
        super().__init__()
        self.texture = arcade.make_soft_square_texture(SQUARE_SIZE, FOOD_COLOR, outer_alpha=255)
        self.respawn()

    def respawn(self):
        """Moves the food to a random grid-aligned location."""
        # Calculate max columns and rows based on screen size and unit size
        max_x = (SCREEN_WIDTH // SQUARE_SIZE) - 1
        max_y = (SCREEN_HEIGHT // SQUARE_SIZE) - 1
        
        # Grid align the food so it's reachable by the snake
        self.center_x = random.randint(0, max_x) * SQUARE_SIZE + (SQUARE_SIZE // 2)
        self.center_y = random.randint(0, max_y) * SQUARE_SIZE + (SQUARE_SIZE // 2)

class NeonSnakeGame(arcade.Window):
    """
    Main application class for the Neon Snake Game.
    Manages the game loop, input, and drawing logic.
    """

    def __init__(self):
        # Set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(BACKGROUND_COLOR)

        # Game State Variables
        self.snake_list = None
        self.food_list = None
        self.food = None
        self.direction = None
        self.next_direction = None
        self.score = 0
        self.game_over = False

        # Speed control variables
        self.time_since_last_move = 0
        self.move_delay = 0.2  # Initial delay (seconds per move)

        # Text objects for better performance in Arcade 3.0+
        self.score_text = arcade.Text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, TEXT_COLOR, 16)
        self.game_over_text = arcade.Text("GAME OVER", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10,
                                         arcade.color.RED, 30, anchor_x="center")
        self.restart_text = arcade.Text("Press 'R' to Restart", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 25,
                                       arcade.color.WHITE, 15, anchor_x="center")
        self.save_load_text = arcade.Text("Press 'S' to Save | 'L' to Load", 10, 10, arcade.color.GRAY, 10)

        # Load Sounds
        # Load Sounds with fallback
        try:
            self.eat_sound = arcade.load_sound(":resources:sounds/coin1.wav")
            self.game_over_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        except Exception:
            self.eat_sound = None
            self.game_over_sound = None

    def setup(self):
        """Initializes the game state and objects."""
        self.score = 0
        self.game_over = False
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.time_since_last_move = 0
        self.move_delay = 0.2

        # Create the snake (starting with 3 segments)
        self.snake_list = arcade.SpriteList()
        start_x = (SCREEN_WIDTH // 2)
        start_y = (SCREEN_HEIGHT // 2)

        # Head of the snake
        head = SnakeSegment(start_x, start_y, SNAKE_HEAD_COLOR)
        self.snake_list.append(head)

        # Initial tail segments
        for i in range(1, 3):
            segment = SnakeSegment(start_x - (i * SQUARE_SIZE), start_y, SNAKE_BODY_COLOR)
            self.snake_list.append(segment)

        # Create food
        self.food_list = arcade.SpriteList()
        self.food = Food()
        self.food_list.append(self.food)

    def on_draw(self):
        """Renders the screen."""
        self.clear()

        # Draw food
        self.food_list.draw()

        # Draw snake
        self.snake_list.draw()

        # Draw HUD (Heads Up Display)
        self.score_text.text = f"Score: {self.score}"
        self.score_text.draw()

        # Draw Game Over message
        if self.game_over:
            # Arcade 3.0+ uses explicit corner-based drawing
            # Calculate Left and Bottom for a 300x100 centered box
            left = (SCREEN_WIDTH // 2) - 150
            bottom = (SCREEN_HEIGHT // 2) - 50
            arcade.draw_lbwh_rectangle_filled(left, bottom, 300, 100, arcade.color.DARK_GRAY)
            self.game_over_text.draw()
            self.restart_text.draw()

        # Instructions for Save/Load
        self.save_load_text.draw()

    def on_key_press(self, key, modifiers):
        """
        Handles keyboard input.
        Prevents the snake from reversing 180 degrees directly.
        """
        if self.game_over:
            if key == arcade.key.R:
                self.setup()
            return

        if key == arcade.key.UP and self.direction != DOWN:
            self.next_direction = UP
        elif key == arcade.key.DOWN and self.direction != UP:
            self.next_direction = DOWN
        elif key == arcade.key.LEFT and self.direction != RIGHT:
            self.next_direction = LEFT
        elif key == arcade.key.RIGHT and self.direction != LEFT:
            self.next_direction = RIGHT
        elif key == arcade.key.S:
            self.save_game()
        elif key == arcade.key.L:
            self.load_game()

    def on_update(self, delta_time):
        """
        Logic for movement and collision.
        Accumulates delta_time to control movement speed.
        """
        if self.game_over:
            return

        # Increment timer
        self.time_since_last_move += delta_time

        # Only move if enough time has passed
        if self.time_since_last_move < self.move_delay:
            return

        # Reset timer
        self.time_since_last_move = 0

        # Update actual movement direction
        self.direction = self.next_direction

        # Calculate new head position
        old_head = self.snake_list[0]
        new_x = old_head.center_x + (self.direction[0] * SQUARE_SIZE)
        new_y = old_head.center_y + (self.direction[1] * SQUARE_SIZE)

        # 1. Collision with Walls
        if (new_x < 0 or new_x > SCREEN_WIDTH or 
            new_y < 0 or new_y > SCREEN_HEIGHT):
            self.mark_game_over()
            return

        # 2. Collision with Self
        # Check if new position overlaps with any existing segment
        for segment in self.snake_list:
            if segment.center_x == new_x and segment.center_y == new_y:
                self.mark_game_over()
                return

        # Create new head segment
        new_head = SnakeSegment(new_x, new_y, SNAKE_HEAD_COLOR)
        
        # Change old head color to body color
        old_head.texture = arcade.make_soft_square_texture(SQUARE_SIZE, SNAKE_BODY_COLOR, outer_alpha=255)
        
        # Add new head to list
        self.snake_list.insert(0, new_head)

        # 3. Collision with Food
        if arcade.check_for_collision(new_head, self.food):
            self.score += 10
            if self.eat_sound:
                arcade.play_sound(self.eat_sound)
            self.food.respawn()

            # Increase speed as snake grows
            # Decrease delay by 0.005s per apple, down to a minimum of 0.05s
            self.move_delay = max(0.05, 0.2 - (len(self.snake_list) // 2) * 0.01)
            # We don't remove the tail segment, so the snake grows
        else:
            # Normal movement: remove the last segment (the tail)
            self.snake_list.pop()

    def mark_game_over(self):
        """Sets game over state and plays sound."""
        self.game_over = True
        if self.game_over_sound:
            arcade.play_sound(self.game_over_sound)

    def save_game(self):
        """Saves current game state to a JSON file."""
        import json
        state = {
            "score": self.score,
            "direction": self.direction,
            "food_pos": [self.food.center_x, self.food.center_y],
            "snake_segments": [[s.center_x, s.center_y] for s in self.snake_list]
        }
        with open("save_game.json", "w") as f:
            json.dump(state, f)
        print("Game Saved")

    def load_game(self):
        """Loads game state from a JSON file."""
        import json
        import os
        if not os.path.exists("save_game.json"):
            return
            
        with open("save_game.json", "r") as f:
            state = json.load(f)
            
        self.score = state["score"]
        self.direction = tuple(state["direction"])
        self.next_direction = self.direction
        self.food.center_x, self.food.center_y = state["food_pos"]
        
        self.snake_list = arcade.SpriteList()
        for i, pos in enumerate(state["snake_segments"]):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
            segment = SnakeSegment(pos[0], pos[1], color)
            self.snake_list.append(segment)
            
        self.game_over = False
        print("Game Loaded")

def main():
    """Main execution function."""
    game = NeonSnakeGame()
    game.setup()
    # Control the game speed by setting update frequency
    # We use a custom schedule to slow down snake updates
    arcade.run()

if __name__ == "__main__":
    main()