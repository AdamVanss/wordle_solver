Here’s a cleaner, more polished README without emojis:

---

# Wordle Solver

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

---

If you want, I can also reorganize it into sections like installation, algorithm description, or add examples.
