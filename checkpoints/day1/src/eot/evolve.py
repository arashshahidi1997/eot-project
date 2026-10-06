"""Population dynamics with ncase's TOY rule (from 04) — swap `select` to change it."""

import numpy as np
import pandas as pd

from .tournament import tournament


def select(population, scores, k, rng):
    """The k lowest scorers are replaced by copies of the k highest."""
    order = np.lexsort((rng.random(len(scores)), scores))  # ascending; ties random
    worst, best = order[:k], order[-k:]
    population = population.copy()
    population[worst] = population[best]
    return population


def evolve(counts, n, noise, generations, k, seed):
    """Run the population. One tidy row per (generation, strategy)."""
    rng = np.random.default_rng(seed)
    population = np.array([s for s, c in counts.items() for _ in range(c)])
    rows = []
    for g in range(generations + 1):
        scores, cooperation = tournament(population, n, noise, rng)
        for s in counts:
            count = int((population == s).sum())
            rows.append(
                {
                    "generation": g,
                    "strategy": s,
                    "share": count / len(population),
                    "cooperation": cooperation,
                }
            )
        if g < generations:
            population = select(population, scores, k, rng)
    return pd.DataFrame(rows)


def simulate(config, seed):
    """One run from a config dict (counts, rounds, noise, generations) and a seed."""
    return evolve(
        config["counts"],
        config["rounds"],
        config["noise"],
        config["generations"],
        5,
        seed,
    )
