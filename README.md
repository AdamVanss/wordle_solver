# Wordle Solver

<<<<<<< HEAD
A simple web-based tool to help solve Wordle puzzles.

## How to Use

1. Choose a starting word or enter your own
2. Enter the word in Wordle
3. Click each letter tile to match the colors Wordle gave you (Gray → Yellow → Green)
4. Click **Submit Pattern** to get the next best word
5. Repeat until solved

## Features

- Light/Dark mode toggle
- Minimax algorithm for optimal word suggestions
- Full wordle official possible word database
=======
A simple command-line tool that helps you solve Wordle efficiently by suggesting the best next guess based on previous feedback.

## Usage

Run the solver from the command line:

```
python wordle_solver.py
```

The script will propose a word. Enter that word into Wordle, then provide the feedback using the following numeric format:

* **0** — Gray (letter not in the word)
* **1** — Yellow (letter in the word, wrong position)
* **2** — Green (letter in the correct position)

Feedback must be a five-digit string corresponding to the five letters of the guess.

### Example

If Wordle returns:

* Gray
* Yellow
* Green
* Gray
* Green

You should input:

```
01202
```

The solver will then analyze this information and suggest your next optimal word.
>>>>>>> f58bbbdb5b1167312832427d4d80ccd3ebccdc06
