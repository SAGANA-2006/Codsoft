# ❌⭕ TicTacToeAI — Unbeatable Console Tic-Tac-Toe

**CodSoft Artificial Intelligence Internship — Task 2**

A console-based Human vs AI Tic-Tac-Toe game where the AI plays a
mathematically perfect game using the **Minimax algorithm** (with
alpha-beta pruning). No external AI APIs, no libraries — pure Python.

The AI **cannot lose**. The best a human opponent can achieve is a draw.

---

## ✨ Features

| Feature | Description |
|---|---|
| Human vs AI | Play a full game against an unbeatable AI opponent |
| Minimax AI | AI moves are chosen by exhaustively searching the game tree |
| Symbol choice | Choose to play as `X` or `O` (X always opens the game) |
| Beautiful board | Clean, color-coded 3x3 grid printed to the terminal |
| Winner detection | Detects all 8 winning lines (rows, columns, diagonals) |
| Draw detection | Recognizes a full board with no winner as a draw |
| Restart option | Play as many rounds as you like in one session |
| Input validation | Rejects out-of-range, non-numeric, or occupied-cell moves |
| Scoreboard | Tracks wins, losses, and draws across the whole session |
| AI thinking message | A short "AI is thinking..." pause before each AI move |

---

## 📁 Project Structure

```
Task2_TicTacToeAI/
│
├── main.py            # Console UI, game loop, input handling, scoreboard
├── minimax.py          # Board logic + the Minimax algorithm (AI brain)
├── README.md            # Project documentation (this file)
├── requirements.txt      # Python dependencies (none required)
├── LICENSE                # MIT License
├── .gitignore              # Files/folders excluded from Git
├── screenshots/            # Demo screenshots for GitHub
└── output/                 # Sample output logs
```

`main.py` and `minimax.py` are deliberately separated: `minimax.py` is
pure game logic with zero `print()`/`input()` calls, which makes the AI
easy to unit test and reuse in a different interface (a GUI, for
example) without changes.

---

## 🚀 How to Run

1. **Install Python 3** (3.8 or higher recommended).
   ```bash
   python3 --version
   ```

2. **Clone or download** this project folder.

3. **Navigate into the project folder:**
   ```bash
   cd Task2_TicTacToeAI
   ```

4. **Run the game:**
   ```bash
   python3 main.py
   ```

5. Choose `X` or `O`, then enter a number from **1-9** to place your
   mark on the matching board position:

   ```
    1 │ 2 │ 3
   ───┼───┼───
    4 │ 5 │ 6
   ───┼───┼───
    7 │ 8 │ 9
   ```

No external libraries are required — the project only uses Python's
built-in `os`, `time`, `math`, and `typing` modules.

---

## 🧠 The Minimax Algorithm, Step by Step

Minimax is a decision-making algorithm for two-player, turn-based games
where one player's gain is the other's loss (a **zero-sum game**).
Tic-Tac-Toe is a perfect fit: it's small enough to search completely,
and every game must end in a win, a loss, or a draw.

**The core idea:** simulate every possible sequence of remaining moves,
score each final outcome, and then work backward to figure out which
move *right now* leads to the best guaranteed outcome — assuming the
opponent also plays as well as possible.

Step by step, for the AI's turn:

1. **Generate every legal move** from the current board (every empty
   cell).
2. **For each move**, temporarily place the AI's symbol and recurse:
   now it's the human's simulated turn.
3. **On the human's simulated turn**, generate every legal move for
   *them*, temporarily place the human's symbol, and recurse again —
   now it's the AI's turn again.
4. **Keep recursing** — AI turn, human turn, AI turn... — until a
   branch reaches a **terminal state**: someone has won, or the board
   is full (a draw).
5. **Score terminal states:**
   - AI wins → `+10 - depth` (a win found sooner scores higher than
     one found deeper in the tree)
   - Human wins → `depth - 10` (a loss found deeper — i.e., delayed as
     long as possible — is less bad than an immediate one)
   - Draw → `0`
6. **Propagate scores back up the tree:**
   - On AI turns, the AI is the **maximizer** — it picks the child
     branch with the *highest* score, because it controls this move.
   - On human turns, the AI assumes the human is a perfect
     **minimizer** — it picks the child branch with the *lowest*
     score, modeling the worst case (the smartest possible opponent).
7. **Back at the root** (the real board), the AI now has a score for
   every one of its possible first moves. It plays the move whose
   subtree produced the **highest** score.

Because every branch is explored, this move is provably optimal — not
just "good," but the best possible response to *any* human play,
including perfect play. That's why the AI can never be beaten.

**Alpha-beta pruning** (`alpha`/`beta` in `minimax()`) is a standard
optimization layered on top: once a branch is found that a player would
never actually allow (because they already have a better alternative
elsewhere), the search stops exploring that branch early. It produces
the *exact same result* as plain minimax — it just skips work that
can't possibly change the answer.

---

## 🧩 Function Overview

### `minimax.py` — the AI's brain

| Function | Purpose |
|---|---|
| `get_winner(board)` | Checks all 8 winning lines; returns `'X'`, `'O'`, or `None` |
| `is_full(board)` | Returns `True` if there are no empty cells left |
| `is_game_over(board)` | Returns `True` if the game has a winner or is full |
| `available_moves(board)` | Returns a list of empty cell indices (legal moves) |
| `minimax(board, depth, is_maximizing, ai_player, human_player, alpha, beta)` | Recursively scores a board state assuming perfect play from both sides; the heart of the algorithm described above |
| `best_move(board, ai_player, human_player)` | Tries every legal move, scores each with `minimax()`, and returns the index of the highest-scoring one — this is what `main.py` calls each AI turn |

### `main.py` — the console game

| Function | Purpose |
|---|---|
| `clear_screen()` | Clears the terminal between board updates |
| `print_banner()` | Displays the game's title banner |
| `colorize(symbol)` | Wraps `X`/`O` in ANSI color codes for readability |
| `print_board(board)` | Renders the 3x3 grid, showing position numbers on empty cells |
| `print_scoreboard(scores, ...)` | Displays the running win/loss/draw tally |
| `choose_symbol()` | Prompts the human to pick `X` or `O`, with input validation |
| `get_human_move(board)` | Prompts for a move; re-asks until it's a valid, empty, in-range cell |
| `ask_yes_no(prompt)` | Generic validated yes/no prompt, used for "Play again?" |
| `ai_move(board, ...)` | Shows the "AI is thinking..." message, then plays `best_move()`'s choice |
| `play_round(human_symbol, ai_symbol)` | Runs one full game from empty board to a win/draw result |
| `announce_result(result)` | Prints a friendly win/lose/draw message |
| `main()` | Orchestrates setup, the replay loop, and the final scoreboard |

---

## ⏱️ Time Complexity

Plain minimax explores the full game tree. With `b` legal moves at each
step and a maximum depth `d`, the worst case is **O(b^d)**.

For Tic-Tac-Toe specifically:
- At most 9 moves are possible on the first turn, 8 on the next, and so
  on, so the absolute upper bound is `9! = 362,880` leaf nodes for a
  search starting from an empty board.
- In practice the *real* number of reachable game states is far
  smaller (about 255,168 possible completed games, and many fewer
  distinct states are explored per call since minimax is called once
  per remaining empty cell, not from a completely empty board every
  time).
- **Alpha-beta pruning** cuts a large fraction of this tree in
  practice — in the best case it reduces the effective branching
  factor from `b` to roughly `√b`, giving closer to **O(b^(d/2))**.

Either way, 9 cells is small enough that even the unpruned worst case
runs instantly (well under a second) on any modern machine — which is
precisely why minimax is a practical, standard choice for Tic-Tac-Toe,
even though it would be too slow for a game like Chess or Go.

## 💾 Space Complexity

Space is dominated by the recursion depth, not the number of nodes,
because minimax explores the tree depth-first and only needs to keep
the current path on the call stack: **O(d)**, where `d ≤ 9`. The board
itself is mutated in place (moves are made, then undone) rather than
copied at each recursive call, so no extra board-sized memory is
allocated per node.

---

## 🔮 Future Improvements

- Add a **difficulty setting** (e.g., "Easy" AI that occasionally
  picks a random move instead of the optimal one).
- Support **larger boards** (4x4, 5x5) with a configurable win length,
  which would make pure minimax too slow and motivate adding
  **iterative deepening** or a move-ordering heuristic.
- Add a **GUI** using Tkinter, or a web interface using Flask/Streamlit.
- Let the human **choose who goes first**, independent of symbol.
- Cache repeated board states with **memoization** (a transposition
  table) to avoid re-scoring identical positions reached via different
  move orders.
- Add **unit tests** (`pytest`) for `minimax.py`'s win detection and
  move selection.
- Log each session's results to a file for later review.

---

## 📸 Suggested Screenshots for GitHub

Save these in the `screenshots/` folder and reference them in your
README or LinkedIn post:

1. The title banner and symbol-choice prompt at startup.
2. A mid-game board showing both `X` and `O` marks in color.
3. The "AI is thinking..." message right before an AI move.
4. A completed game showing the win message (human win, if you can
   force one, or an AI win).
5. A completed game ending in a draw.
6. The scoreboard after a few rounds, showing the running tally.

---

## 📝 License

This project is licensed under the MIT License — see [LICENSE](LICENSE)
for details.

---

## 🙌 Acknowledgements

Built as part of the **CodSoft Artificial Intelligence Internship**
(Task 2 — Tic-Tac-Toe AI with Minimax).

`#codsoft` `#internship` `#artificialintelligence` `#python` `#minimax`
