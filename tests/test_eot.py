"""Exercise 05 — your `eot` package must pass these.  Run:  pixi run pytest

They pin the package's API (what notebooks and Snakemake rules import) and the
checks you already trust from 03 and 04. Failing at first is expected.
"""

import pandas as pd
import pytest
from eot import STRATEGIES, round_robin, run_match, simulate


def test_five_strategies():
    assert set(STRATEGIES) == {"angel", "devil", "copycat", "grudger", "copykitten"}


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        ("angel", "devil", (-10, 30)),  # control
        ("copycat", "copycat", (20, 20)),  # necessary, not sufficient
        ("copycat", "devil", (-1, 3)),  # the one that bites
    ],
)
def test_match_invariants(a, b, expected):
    df = run_match(STRATEGIES[a], STRATEGIES[b], 10)
    assert (df.cum_a.iloc[-1], df.cum_b.iloc[-1]) == expected


def test_round_robin_data_contract():
    df = round_robin(list(STRATEGIES), 10)
    assert len(df) == 25
    assert {
        "strategy_a",
        "strategy_b",
        "rounds",
        "score_a",
        "score_b",
        "mean_payoff_a",
        "mean_payoff_b",
    } <= set(df.columns)


CONFIG = {
    "counts": {"copycat": 20, "devil": 5},
    "rounds": 10,
    "noise": 0.05,
    "generations": 30,
}


def final_cooperation(df):
    return df[df.generation == df.generation.max()].cooperation.iloc[0]


def test_simulate_is_tidy_and_reproducible():
    a, b = simulate(CONFIG, seed=0), simulate(CONFIG, seed=0)
    assert {"generation", "strategy", "share", "cooperation"} <= set(a.columns)
    pd.testing.assert_frame_equal(a, b)  # same seed -> same result


def test_no_noise_full_cooperation():
    assert final_cooperation(simulate({**CONFIG, "noise": 0.0}, seed=0)) == 1.0


def test_noise_erodes_cooperation():  # your 04 finding, as a test
    assert 0.7 < final_cooperation(simulate(CONFIG, seed=0)) < 0.85
