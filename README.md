# Rock Paper Scissors Game

A simple Rock Paper Scissors game built with Pygame. Play against the computer in this classic hand game!

## Features

- Interactive gameplay with keyboard controls
- Computer opponent with animated hand selection
- Score tracking
- Clean and intuitive interface
- Responsive controls (R, P, S keys)
- Smooth animations and transitions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rohith-vp/rock-paper-scissors-pygame.git
cd rock-paper-scissors-pygame
```

2. Create and activate a virtual environment (optional but recommended):
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/MacOS
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

1. Run the game:
```bash
python app/main.py
```

2. Game Controls:
- Press 'R' for Rock
- Press 'P' for Paper
- Press 'S' for Scissors
- Press any key to play again after each round
- Alt+F4 or click 'X' to quit the game

## Game Rules

- Rock crushes Scissors
- Scissors cuts Paper
- Paper covers Rock
- The score is tracked for both player and computer

## Project Structure

```
rock-paper-scissors-pygame/
├── app/
│   ├── main.py          # Game entry point
│   └── Game.py          # Main game logic
├── res/                 # Game resources
│   ├── rock.png
│   ├── paper.png
│   ├── scissors.png
│   └── icon.png
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Requirements

- Python 3.x
- Pygame 2.5.0 or higher

## License

This project is open source and available under the MIT License.