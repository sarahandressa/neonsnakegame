# Neon Snake - CSE 310 Applied Programming

## Project Overview - Module 1 

Neon Snake is a grid-based arcade game designed to demonstrate proficiency in Python programming and the Arcade framework. This software implements custom Sprite classes for game entities, manages real-time event processing for keyboard input, and utilizes complex game logic for collision detection and state management. The project was developed as the first module to CSE 310 course to showcase the ability to bridge fundamental programming concepts with graphic user interface development

## Features
- **Graphics & UI**: Uses the Arcade library to render a high-contrast neon aesthetic with smooth 60 FPS performance.
- **Dynamic Interaction**: Full keyboard support for snake navigation with logic to prevent illegal 180-degree turns.
- **Game Logic**: Real-time tracking of snake growth, score calculation, and collision boundaries (walls and self).
- **Sound Integration**: Implementation of audio triggers for critical game events like scoring and failure states.
- **Persistence**: A custom JSON-based Save/Load system that allows user to preserve their current game progress.

## Development Environment

The following tools and technologies were utilized to build and test this software:
- **Language**: Python 3.10 (64-bit)
- **Framework**: [Arcade Library](https://arcade.academy/)
- **Text Editor**: Visual Studio Code
- **Version Control**: Git & GitHub

### Installation Requirements
To run this game locally, you must have the `arcade` module installed in your Python environment:
```bash
pip install arcade
```

## Useful Websites

The following resources were consulted during the research and development of this module:
- [Arcade Official Documentation](https://api.arcade.academy/) - Primary reference for SpriteList and collision logic.
- [Wikipedia: Snake (Video Game)](https://en.wikipedia.org/wiki/Snake_(video_game_genre)) - Used for historical context and logic principles.
- [BYU-Idaho CSE 310 Course Materials](https://github.com/byui-cse/cse310-course) - Guidance on project structure and requirements.

## Future Work

To further expand this software in future sprints, I intend to implement:
- **High Score Database**: Integration with a local file or cloud database to store top player records globally.
- **Multiple Levels**: Progression logic that introduces obstacles or increases game speed as the score increases.
- **Advanced Animations**: Particle emitters for when the snake "crashes" to provide a more premium visual experience.

## Training Video

[The Final Project Walkthrough Video]()

---

## How to Play
1. Navigate to the project directory in your terminal.
2. Run the command: `python main.py`
3. Use the **Arrow Keys** to move the snake.
4. Press **'S'** to Save your current progress.
5. Press **'L'** to Load your last saved game.
6. Press **'R'** to Restart if the game ends.