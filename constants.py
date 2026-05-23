"""
Global constants for the Neon Snake Game.
These values control the visual appearance and physics of the game.
"""
import arcade

# Window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Neon Snake - CSE 310 Student Project"

# Grid settings
# The screen is divided into cells. Each cell is SQUARE_SIZE x SQUARE_SIZE.
SQUARE_SIZE = 20

# Directions
UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Colors (Neon Aesthetic)
BACKGROUND_COLOR = arcade.color.BLACK
SNAKE_HEAD_COLOR = arcade.color.NEON_GREEN
SNAKE_BODY_COLOR = arcade.color.ELECTRIC_GREEN
FOOD_COLOR = arcade.color.NEON_CARROT # Bright orange/red
TEXT_COLOR = arcade.color.WHITE

# Game speed (frames between updates)
# Low values = faster game
UPDATES_PER_SECOND = 10
