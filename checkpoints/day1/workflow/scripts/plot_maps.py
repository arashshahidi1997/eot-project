"""Two linked maps over rounds × noise: WHERE cooperation survives, WHICH strategy wins."""

import altair as alt
import pandas as pd

summary = pd.read_csv(snakemake.input[0])  # noqa: F821
base = alt.Chart(summary).encode(
    x=alt.X("noise:O", title="noise", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("rounds:O", sort="descending", title="rounds per match"),
)
cooperation = (
    base.mark_rect().encode(
        color=alt.Color(
            "cooperation:Q",
            scale=alt.Scale(scheme="blues", domain=[0, 1]),
            title="cooperation",
        )
    )
    + base.mark_text().encode(
        text=alt.Text("cooperation:Q", format=".2f"),
        color=alt.condition(
            "datum.cooperation > 0.6", alt.value("white"), alt.value("black")
        ),
    )
).properties(width=260, height=220, title="Where does cooperation survive?")
winner = (
    base.mark_rect().encode(color=alt.Color("winner:N", title="winner"))
    + base.mark_text(fontSize=10).encode(text="winner:N")
).properties(width=260, height=220, title="Which strategy wins?")
alt.hconcat(cooperation, winner).resolve_scale(color="independent").save(
    snakemake.output[0],  # noqa: F821
    ppi=144,
)
