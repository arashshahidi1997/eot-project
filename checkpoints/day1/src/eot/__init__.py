"""eot — the Evolution of Trust model, moved out of the Day-1 notebooks."""

from .evolve import evolve, select, simulate
from .game import STRATEGIES, score
from .match import match_score, run_match
from .tournament import round_robin, tournament

__all__ = [
    "STRATEGIES",
    "evolve",
    "match_score",
    "round_robin",
    "run_match",
    "score",
    "select",
    "simulate",
    "tournament",
]
