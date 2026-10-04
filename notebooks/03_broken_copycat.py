import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""
    # 03 · The verification sting

    Here is a **finished** tournament notebook — a colleague sends it to you.
    It runs, and the heatmap below looks perfectly plausible.

    **Your job:** decide whether it is *correct*. Work with your agent, but the
    acceptance checks are yours to run and yours to believe. (See the three
    invariants in the exercise sheet — one of them is the one that bites.)
    """)
    return


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import pandas as pd

    return alt, mo, pd


@app.cell
def _():
    R, S, T, P = 2, -1, 3, 0

    def score(move_a, move_b):
        if move_a == "C" and move_b == "C":
            return R, R
        if move_a == "D" and move_b == "D":
            return P, P
        if move_a == "D" and move_b == "C":
            return T, S
        return S, T

    return (score,)


@app.cell
def _():
    # The five strategies. Each reads a history of moves and returns its next move.
    def angel(history):
        return "C"

    def devil(history):
        return "D"

    def copycat(history):
        # cooperate first, then copy the last move in the history
        return history[-1] if history else "C"

    def grudger(history):
        return "D" if "D" in history else "C"

    def copykitten(history):
        if len(history) >= 2 and history[-1] == "D" and history[-2] == "D":
            return "D"
        return "C"

    strategies = {
        "angel": angel,
        "devil": devil,
        "copycat": copycat,
        "grudger": grudger,
        "copykitten": copykitten,
    }
    return (strategies,)


@app.cell
def _(pd, score, strategies):
    def run_match(fn_a, fn_b, n):
        history_a, history_b = [], []
        cum_a = cum_b = 0
        for _r in range(n):
            # each strategy decides from the match history so far
            move_a = fn_a(history_a)
            move_b = fn_b(history_b)
            pa, pb = score(move_a, move_b)
            cum_a += pa
            cum_b += pb
            history_a.append(move_a)
            history_b.append(move_b)
        return cum_a, cum_b

    def round_robin(names, n):
        rows = []
        for a in names:
            for b in names:
                sa, sb = run_match(strategies[a], strategies[b], n)
                rows.append(
                    {
                        "strategy_a": a,
                        "strategy_b": b,
                        "rounds": n,
                        "score_a": sa,
                        "score_b": sb,
                        "mean_payoff_a": sa / n,
                        "mean_payoff_b": sb / n,
                    }
                )
        return pd.DataFrame(rows)

    tournament = round_robin(list(strategies), 10)
    return (tournament,)


@app.cell
def _(alt, strategies, tournament):
    _order = list(strategies)
    alt.Chart(tournament).mark_rect().encode(
        x=alt.X("strategy_b:N", sort=_order, title="opponent"),
        y=alt.Y("strategy_a:N", sort=_order, title="player"),
        color=alt.Color(
            "mean_payoff_a:Q",
            title="mean payoff / round",
            scale=alt.Scale(scheme="redyellowgreen", domain=[-1, 3]),
        ),
        tooltip=["strategy_a", "strategy_b", "mean_payoff_a"],
    ).properties(width=360, height=360, title="EoT tournament — mean payoff per round")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ::: {.callout-important}
    A plausible figure is **not** validation. Before you trust this result, check:
    does **Copycat vs Devil** earn what it should? Does your control (**Angel vs
    Devil**) still agree? One passes, one fails — and the gap tells you where the
    bug lives.
    :::
    """)
    return


if __name__ == "__main__":
    app.run()
