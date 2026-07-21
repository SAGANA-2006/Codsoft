"""
main.py

Console-based Human vs AI Tic-Tac-Toe.

The AI never loses: it uses the minimax algorithm (see minimax.py) to
search the entire remaining game tree on every turn, so it always plays
a mathematically optimal move. The worst a human can achieve is a draw.

Author: <Your Name>
Project: CodSoft AI Internship - Task 2
"""

import os
import time

from minimax import available_moves, best_move, get_winner, is_full

# ---------------------------------------------------------------------------
# DISPLAY CONSTANTS
# ---------------------------------------------------------------------------

CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

AI_THINK_DELAY_SECONDS = 0.6


# ---------------------------------------------------------------------------
# DISPLAY HELPERS
# ---------------------------------------------------------------------------

def clear_screen() -> None:
    """Clear the terminal so each new board is easy to read."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner() -> None:
    """Show the game's title banner."""
    print(f"{BOLD}{CYAN}")
    print("=" * 45)
    print("        TIC-TAC-TOE — HUMAN vs AI")
    print("        (AI powered by Minimax)")
    print("=" * 45)
    print(RESET)


def colorize(symbol: str) -> str:
    """Wrap a symbol in an ANSI color so X and O are easy to tell apart."""
    if symbol == "X":
        return f"{CYAN}{BOLD}X{RESET}"
    if symbol == "O":
        return f"{YELLOW}{BOLD}O{RESET}"
    return symbol


def print_board(board: list) -> None:
    """
    Print the board in a clean 3x3 grid.

    Empty cells show their position number (1-9) so the human always
    knows exactly what to type to make a move.
    """
    def cell(i: int) -> str:
        return colorize(board[i]) if board[i] != " " else str(i + 1)

    row_divider = "   ───┼───┼───"
    print()
    print(f"    {cell(0)}   │   {cell(1)}   │   {cell(2)}   ")
    print(row_divider)
    print(f"    {cell(3)}   │   {cell(4)}   │   {cell(5)}   ")
    print(row_divider)
    print(f"    {cell(6)}   │   {cell(7)}   │   {cell(8)}   ")
    print()


def print_scoreboard(scores: dict, human_symbol: str, ai_symbol: str) -> None:
    """Display the running win/loss/draw tally for the session."""
    print(f"{BOLD}--- Scoreboard ---{RESET}")
    print(f"  You ({colorize(human_symbol)}) : {scores['human']}")
    print(f"  AI  ({colorize(ai_symbol)}) : {scores['ai']}")
    print(f"  Draws        : {scores['draws']}")
    print("-" * 20)
    print()


# ---------------------------------------------------------------------------
# INPUT HELPERS (all with validation + re-prompting on bad input)
# ---------------------------------------------------------------------------

def choose_symbol() -> tuple:
    """
    Ask the human to choose X or O.

    Returns:
        A (human_symbol, ai_symbol) tuple. X always moves first, so if
        the human picks O, the AI takes the opening move.
    """
    while True:
        choice = input("Choose your symbol - X or O: ").strip().upper()
        if choice in ("X", "O"):
            ai_symbol = "O" if choice == "X" else "X"
            return choice, ai_symbol
        print(f"{RED}Invalid choice. Please type X or O.{RESET}")


def get_human_move(board: list) -> int:
    """
    Prompt the human for a move and validate it.

    Keeps asking until the input is an integer from 1-9 that
    corresponds to an empty cell, then returns it as a 0-based index.
    """
    while True:
        raw = input("Your move (1-9): ").strip()

        if not raw.isdigit():
            print(f"{RED}Please enter a number between 1 and 9.{RESET}")
            continue

        position = int(raw)
        if position < 1 or position > 9:
            print(f"{RED}Please enter a number between 1 and 9.{RESET}")
            continue

        index = position - 1
        if board[index] != " ":
            print(f"{RED}That cell is already taken. Pick another one.{RESET}")
            continue

        return index


def ask_yes_no(prompt: str) -> bool:
    """Ask a yes/no question and keep asking until the input is valid."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print(f"{RED}Please answer with 'y' or 'n'.{RESET}")


# ---------------------------------------------------------------------------
# GAME LOGIC
# ---------------------------------------------------------------------------

def ai_move(board: list, ai_symbol: str, human_symbol: str) -> None:
    """
    Compute and apply the AI's move, with a short "thinking" message so
    the pause while minimax searches doesn't feel like a freeze.
    """
    print(f"{YELLOW}AI is thinking...{RESET}")
    time.sleep(AI_THINK_DELAY_SECONDS)
    move = best_move(board, ai_symbol, human_symbol)
    board[move] = ai_symbol


def play_round(human_symbol: str, ai_symbol: str) -> str:
    """
    Play one full round of Tic-Tac-Toe to completion.

    Returns:
        'human' if the human wins, 'ai' if the AI wins, or 'draw'.
    """
    board = [" "] * 9
    current_symbol = "X"  # X always opens the game.

    clear_screen()
    print_banner()
    print_board(board)

    while True:
        if current_symbol == human_symbol:
            index = get_human_move(board)
            board[index] = human_symbol
        else:
            ai_move(board, ai_symbol, human_symbol)

        clear_screen()
        print_banner()
        print_board(board)

        winner = get_winner(board)
        if winner is not None:
            return "human" if winner == human_symbol else "ai"
        if is_full(board):
            return "draw"

        current_symbol = ai_symbol if current_symbol == human_symbol else human_symbol


def announce_result(result: str) -> None:
    """Print a clear, friendly message announcing the round's outcome."""
    if result == "human":
        print(f"{GREEN}{BOLD}You win! Well played.{RESET}\n")
    elif result == "ai":
        print(f"{RED}{BOLD}The AI wins this round.{RESET}\n")
    else:
        print(f"{YELLOW}{BOLD}It's a draw!{RESET}\n")


# ---------------------------------------------------------------------------
# MAIN PROGRAM LOOP
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the full game session: setup, rounds, scoreboard, and replay."""
    clear_screen()
    print_banner()
    print("Positions are numbered 1-9, left to right, top to bottom.")
    print("The AI plays a perfect game using the Minimax algorithm -")
    print("the best you can do is force a draw!\n")

    human_symbol, ai_symbol = choose_symbol()
    scores = {"human": 0, "ai": 0, "draws": 0}

    while True:
        result = play_round(human_symbol, ai_symbol)
        announce_result(result)

        if result == "human":
            scores["human"] += 1
        elif result == "ai":
            scores["ai"] += 1
        else:
            scores["draws"] += 1

        print_scoreboard(scores, human_symbol, ai_symbol)

        if not ask_yes_no("Play again? (y/n): "):
            break

    print(f"\n{BOLD}Thanks for playing! Final scoreboard:{RESET}")
    print_scoreboard(scores, human_symbol, ai_symbol)
    print("Goodbye! 👋")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nSession interrupted. Goodbye!")
