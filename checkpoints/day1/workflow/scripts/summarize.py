"""All simulations -> one row per (rounds, noise): final cooperation (mean over seeds)
and the winner. Winner rule (pinned in targets/spec.md): per seed, the largest group —
"tie" if several share the top; across seeds, the strict majority — else "tie".
(Without noise, the nice retaliators behave identically: who ends largest is drift.)"""

import pandas as pd

runs = pd.concat(pd.read_csv(f) for f in snakemake.input)  # noqa: F821
final = runs[runs.generation == runs.generation.max()]


def seed_winner(g):
    top = g[g.share == g.share.max()].strategy
    return top.iloc[0] if len(top) == 1 else "tie"


def majority(winners):
    counts = winners.value_counts()
    return counts.index[0] if counts.iloc[0] > len(winners) / 2 else "tie"


per_seed = final.groupby(["rounds", "noise", "seed"]).apply(
    lambda g: pd.Series(
        {"cooperation": g.cooperation.iloc[0], "winner": seed_winner(g)}
    ),
    include_groups=False,
)
summary = (
    per_seed.reset_index()
    .groupby(["rounds", "noise"])
    .agg(cooperation=("cooperation", "mean"), winner=("winner", majority))
    .reset_index()
)
summary.to_csv(snakemake.output[0], index=False)  # noqa: F821
