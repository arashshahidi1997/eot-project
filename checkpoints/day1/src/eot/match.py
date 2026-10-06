"""One repeated match (from 02 and 04)."""

import pandas as pd

from .game import score

FLIP = {"C": "D", "D": "C"}


def run_match(fn_a, fn_b, n, noise_a=0.0, noise_b=0.0, rng=None):
    """Play n rounds; one tidy row per round. A mistake (probability noise_a /
    noise_b) flips the move a player intended; the opponent sees the move played."""
    history_a, history_b = [], []
    rows = []
    cum_a = cum_b = 0
    for r in range(1, n + 1):
        move_a, move_b = fn_a(history_b), fn_b(history_a)
        if noise_a and rng.random() < noise_a:
            move_a = FLIP[move_a]
        if noise_b and rng.random() < noise_b:
            move_b = FLIP[move_b]
        payoff_a, payoff_b = score(move_a, move_b)
        cum_a, cum_b = cum_a + payoff_a, cum_b + payoff_b
        rows.append(
            {
                "round": r,
                "move_a": move_a,
                "move_b": move_b,
                "cum_a": cum_a,
                "cum_b": cum_b,
            }
        )
        history_a.append(move_a)
        history_b.append(move_b)
    return pd.DataFrame(rows)


def match_score(fn_a, fn_b, n, noise, rng):
    """Total points (A, B) and the number of cooperative moves in one match."""
    history_a, history_b = [], []
    total_a = total_b = coop = 0
    for _ in range(n):
        move_a, move_b = fn_a(history_b), fn_b(history_a)
        if noise and rng.random() < noise:
            move_a = FLIP[move_a]
        if noise and rng.random() < noise:
            move_b = FLIP[move_b]
        points_a, points_b = score(move_a, move_b)
        total_a, total_b = total_a + points_a, total_b + points_b
        coop += (move_a == "C") + (move_b == "C")
        history_a.append(move_a)
        history_b.append(move_b)
    return total_a, total_b, coop
