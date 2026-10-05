import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""
    # 03 · Compete — checkpoint

    A working tournament: every strategy vs every strategy, 10 rounds, no noise.
    """)
    return


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import pandas as pd

    return alt, mo, pd


@app.cell
def _(pd):
    R, S, T, P = 2, -1, 3, 0

    def score(move_a, move_b):
        if move_a == "C" and move_b == "C":
            return R, R
        if move_a == "D" and move_b == "D":
            return P, P
        if move_a == "D" and move_b == "C":
            return T, S
        return S, T

    strategies = {
        "angel": lambda h: "C",
        "devil": lambda h: "D",
        "copycat": lambda h: h[-1] if h else "C",
        "grudger": lambda h: "D" if "D" in h else "C",
        "copykitten": lambda h: "D" if h[-2:] == ["D", "D"] else "C",
    }

    def run_match(fn_a, fn_b, n):
        """n rounds, no noise; one tidy row per round."""
        history_a, history_b, rows = [], [], []
        cum_a = cum_b = 0
        for r in range(1, n + 1):
            move_a, move_b = fn_a(history_b), fn_b(history_a)
            payoff_a, payoff_b = score(move_a, move_b)
            cum_a, cum_b = cum_a + payoff_a, cum_b + payoff_b
            rows.append({"round": r, "cum_a": cum_a, "cum_b": cum_b})
            history_a.append(move_a)
            history_b.append(move_b)
        return pd.DataFrame(rows)

    return run_match, strategies


@app.cell
def _(pd, run_match, strategies):
    def round_robin(names, n):
        """Every strategy vs every strategy, incl. self-play — the data contract."""
        rows = []
        for a in names:
            for b in names:
                m = run_match(strategies[a], strategies[b], n)
                score_a, score_b = int(m.cum_a.iloc[-1]), int(m.cum_b.iloc[-1])
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

    tournament = round_robin(list(strategies), 10)
    return (tournament,)


@app.cell
def _(alt, tournament):
    alt.Chart(tournament).mark_rect().encode(
        x=alt.X("strategy_b:N", title="opponent"),
        y=alt.Y("strategy_a:N", title="player"),
        color=alt.Color(
            "mean_payoff_a:Q",
            title="mean payoff / round",
            scale=alt.Scale(scheme="redyellowgreen", domain=[-1, 3]),
        ),
        tooltip=["strategy_a", "strategy_b", "mean_payoff_a"],
    ).properties(width=360, height=360, title="EoT tournament — mean payoff per round")
    return


@app.cell
def _(pd, tournament):
    # The acceptance checks from targets/spec.md, computed from the tournament itself.
    _expected = {
        ("angel", "devil"): (-10, 30),
        ("copycat", "copycat"): (20, 20),
        ("copycat", "devil"): (-1, 3),
    }
    _t = tournament.set_index(["strategy_a", "strategy_b"])
    checks = pd.DataFrame(
        [
            {
                "check": f"{a} vs {b}",
                "expected": exp,
                "got": (int(_t.loc[(a, b), "score_a"]), int(_t.loc[(a, b), "score_b"])),
            }
            for (a, b), exp in _expected.items()
        ]
    ).assign(ok=lambda d: d.expected == d.got)
    checks
    return


@app.cell
def _(tournament):
    # Leaderboard: mean payoff per round, averaged over opponents.
    tournament.groupby("strategy_a").mean_payoff_a.mean().sort_values(ascending=False)
    return


if __name__ == "__main__":
    app.run()
