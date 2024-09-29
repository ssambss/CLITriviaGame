# Trivia Quiz Game

This project is a command-line trivia quiz game that uses the Open Trivia Database API. The game supports multiple players, allows category and difficulty selection, and tracks player scores based on their correct answers. The first player to reach a predetermined number of points wins the game.

## Features

- **Multiple players**: Play with 1 or more players.
- **Category selection**: Choose from various trivia categories or let the game select one randomly.
- **Difficulty levels**: Choose between "easy", "medium", "hard", or "random" difficulties.
- **Dynamic trivia questions**: Questions are fetched live from the [Open Trivia Database](https://opentdb.com/).
- **Points system**: Players earn points based on the difficulty of the question. 
  - 1 point for **easy** questions
  - 2 points for **medium** questions
  - 3 points for **hard** questions
- **Session token**: Ensures that no trivia question is repeated during a session.

## Requirements

- Python 3.10 or newer.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. **Install dependencies**:
   ```bash
   pip install requests

3. **Run the game**:
   ```bash
   python trivia_game.py

## How to Play

1. **Number of Players**: Enter how many players will participate.
2. **Category Selection**: Choose a trivia category, or select "Random" for mixed categories.
3. **Difficulty Selection**: Choose from "Easy", "Medium", "Hard", or "Random".
4. **Points to Win**: Set the number of points a player must reach to win.
5. **Answer Questions**:
   - Each player takes turns answering multiple-choice questions.
   - Points are awarded based on difficulty: 
     - 1 point for **Easy**
     - 2 points for **Medium**
     - 3 points for **Hard**
6. **Winning**: The first player to reach the target score wins.

## Example Game Flow

1. **Start the game**:
   - Players choose the number of participants, category, difficulty, and points to win.
   
2. **Take turns answering**:
   - Players answer trivia questions in turn. The game checks if the answer is correct and updates scores.

3. **Winning the game**:
   - The first player to reach the target points wins.

**Note**

- If all questions in a category and difficulty level are used, the game prompts the players to select a new category or difficulty.
