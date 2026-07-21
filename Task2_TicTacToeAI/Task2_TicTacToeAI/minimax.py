"""
minimax.py

Implements the Minimax algorithm (with alpha-beta pruning) for a perfect
Tic-Tac-Toe AI. This module is completely independent of any input/output
logic — it only knows about board states and scores, which makes it easy
to test and reuse.

Board representation:
    A board is a list of 9 characters, indices 0-8, laid out as:

        0 | 1 | 2
        --+---+--
        3 | 4 | 5
        --+---+--
        6 | 7 | 8

    Each cell holds 'X', 'O', or ' ' (empty).

Author: <Your Name>
Project: CodSoft AI Internship - Task 2
"""

import math
from typing import List, Optional

# All possible ways to win: 3 rows, 3 columns, 2 diagonals.
WIN_COMBINATIONS = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
)


def get_winner(board: List[str]) -> Optional[str]:
    """
    Check the board for a winning combination.

    Args:
        board: The 9-cell board state.

    Returns:
        'X' or 'O' if that player has three in a row, otherwise None.
    """
    for a, b, c in WIN_COMBINATIONS:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board: List[str]) -> bool:
    """Return True if there are no empty cells left on the board."""
    return " " not in board


def is_game_over(board: List[str]) -> bool:
    """Return True if someone has won or the board is full (a draw)."""
    return get_winner(board) is not None or is_full(board)


def available_moves(board: List[str]) -> List[int]:
    """Return a list of empty cell indices where a move can be made."""
    return [i for i, cell in enumerate(board) if cell == " "]


def minimax(
    board: List[str],
    depth: int,
    is_maximizing: bool,
    ai_player: str,
    human_player: str,
    alpha: float = -math.inf,
    beta: float = math.inf,
) -> int:
    """
    Recursively score every possible outcome of the game from the current
    board state, assuming both players play perfectly from here on.

    The AI ("maximizing" player) always tries to pick the move with the
    highest score; the human ("minimizing" player) is assumed to always
    pick the move with the lowest score. Scores are biased by depth so
    that the AI prefers to win as quickly as possible and lose (delay
    a loss) for as long as possible.

    Args:
        board: The current board state (mutated and restored in place
            while exploring moves — no copies are made, for speed).
        depth: How many moves deep this call is from the real board.
        is_maximizing: True if it's the AI's turn to move in this
            simulated state, False if it's the human's turn.
        ai_player: The AI's symbol ('X' or 'O').
        human_player: The human's symbol (the other one).
        alpha: Best score the maximizer can already guarantee
            (used for alpha-beta pruning).
        beta: Best score the minimizer can already guarantee
            (used for alpha-beta pruning).

    Returns:
        An integer score for this board state:
            +10 - depth  -> the AI wins (sooner wins score higher)
            depth - 10   -> the human wins (later losses score higher)
            0            -> a draw
    """
    winner = get_winner(board)
    if winner == ai_player:
        return 10 - depth
    if winner == human_player:
        return depth - 10
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in available_moves(board):
            board[move] = ai_player
            score = minimax(
                board, depth + 1, False, ai_player, human_player, alpha, beta
            )
            board[move] = " "
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # Prune: the minimizer will never allow this branch.
        return best_score

    best_score = math.inf
    for move in available_moves(board):
        board[move] = human_player
        score = minimax(
            board, depth + 1, True, ai_player, human_player, alpha, beta
        )
        board[move] = " "
        best_score = min(best_score, score)
        beta = min(beta, best_score)
        if beta <= alpha:
            break  # Prune: the maximizer will never allow this branch.
    return best_score


def best_move(board: List[str], ai_player: str, human_player: str) -> int:
    """
    Determine the AI's optimal move using minimax.

    Tries every empty cell, scores the resulting position with minimax,
    and returns the index of the cell with the highest score. Because
    minimax explores the entire remaining game tree, this move is
    guaranteed to be optimal — the AI can never be beaten, only forced
    into a draw.

    Args:
        board: The current board state.
        ai_player: The AI's symbol ('X' or 'O').
        human_player: The human's symbol (the other one).

    Returns:
        The index (0-8) of the best cell for the AI to play.
    """
    best_score = -math.inf
    move_to_make = available_moves(board)[0]

    for move in available_moves(board):
        board[move] = ai_player
        score = minimax(board, 0, False, ai_player, human_player)
        board[move] = " "

        if score > best_score:
            best_score = score
            move_to_make = move

    return move_to_make
