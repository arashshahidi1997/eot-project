"""The 03 heatmap: mean payoff per round of the row strategy against the column."""

import altair as alt
import pandas as pd

t = pd.read_csv(snakemake.input[0])  # noqa: F821
order = list(dict.fromkeys(t.strategy_a))
alt.Chart(t).mark_rect().encode(
    x=alt.X("strategy_b:N", sort=order, title="opponent", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("strategy_a:N", sort=order, title="player"),
    color=alt.Color(
        "mean_payoff_a:Q",
        title="mean payoff / round",
        scale=alt.Scale(scheme="redyellowgreen", domain=[-1, 3]),
    ),
).properties(width=320, height=320, title="Tournament — mean payoff per round").save(
    snakemake.output[0],  # noqa: F821
    ppi=144,
)
