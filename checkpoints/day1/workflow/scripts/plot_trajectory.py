"""One run (04's picture): who is in the population, and how much they cooperate."""

import altair as alt
import pandas as pd

run = pd.read_csv(snakemake.input[0])  # noqa: F821
w = snakemake.wildcards  # noqa: F821
shares = (
    alt.Chart(run)
    .mark_area()
    .encode(
        x="generation:Q",
        y=alt.Y("share:Q", stack="normalize", title="population share"),
        color=alt.Color("strategy:N", title=None),
    )
    .properties(
        width=420,
        height=180,
        title=f"rounds {w.rounds} · noise {w.noise} · seed {w.seed}",
    )
)
cooperation = (
    alt.Chart(run.drop_duplicates("generation"))
    .mark_line(point=True)
    .encode(
        x="generation:Q",
        y=alt.Y(
            "cooperation:Q", title="cooperative moves", scale=alt.Scale(domain=[0, 1])
        ),
    )
    .properties(width=420, height=100)
)
alt.vconcat(shares, cooperation).save(snakemake.output[0], ppi=144)  # noqa: F821
