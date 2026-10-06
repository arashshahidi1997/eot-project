"""Everyone vs everyone: strategies (03) and agents in a population (04)."""

import numpy as np
import pandas as pd

from .game import STRATEGIES
from .match import match_score, run_match


def round_robin(names, n):
    """Every strategy vs every strategy (incl. self-play), no noise. One row per
    ordered pairing — the 03 data contract."""
    rows = []
    for a in names:
        for b in names:
            match = run_match(STRATEGIES[a], STRATEGIES[b], n)
            score_a, score_b = int(match.cum_a.iloc[-1]), int(match.cum_b.iloc[-1])
            rows.append(
                {
                    "strategy_a": a,
                    "strategy_b": b,
                    "rounds": n,
                    "score_a": score_a,
                    "score_b": score_b,
                    "mean_payoff_a": score_a / n,
                    "mean_payoff_b": score_b / n,
                }
            )
    return pd.DataFrame(rows)


def tournament(population, n, noise, rng):
    """Everyone plays everyone once: each agent's score, and the share of
    cooperative moves in this generation."""
    scores = np.zeros(len(population))
    coop = 0
    for i in range(len(population)):
        for j in range(i + 1, len(population)):
            a, b, c = match_score(
                STRATEGIES[population[i]], STRATEGIES[population[j]], n, noise, rng
            )
            scores[i] += a
            scores[j] += b
            coop += c
    pairs = len(population) * (len(population) - 1) / 2
    return scores, coop / (2 * n * pairs)
