import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""
    # 04 · Evolve — does cooperation survive mistakes?

    **Question all day:** *when does cooperation survive?*

    Now a whole **population** plays. Each generation everyone plays everyone; the
    5 lowest scorers are replaced by copies of the 5 highest (the rule from
    [ncase.me/trust](https://ncase.me/trust/) — a *toy* evolution rule).

    The loop is written for you. Fill **one** hole: the selection step.
    """)
    return


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    return alt, mo, np, pd


@app.cell
def _():
    # Same game as 02 — copied here on purpose. In 05 you stop copying it.
    R, S, T, P = 2, -1, 3, 0

    def score(move_a, move_b):
        """Points to (A, B) for one simultaneous round."""
        if move_a == "C" and move_b == "C":
            return R, R
        if move_a == "D" and move_b == "D":
            return P, P
        if move_a == "D" and move_b == "C":
            return T, S
        return S, T

    def angel(opponent_history):
        return "C"

    def devil(opponent_history):
        return "D"

    def copycat(opponent_history):
        return opponent_history[-1] if opponent_history else "C"

    def grudger(opponent_history):
        return "D" if "D" in opponent_history else "C"

    def copykitten(opponent_history):
        # forgiving: defect only after TWO opponent defects in a row
        if opponent_history[-2:] == ["D", "D"]:
            return "D"
        return "C"

    strategies = {
        "angel": angel,
        "devil": devil,
        "copycat": copycat,
        "grudger": grudger,
        "copykitten": copykitten,
    }
    return score, strategies


@app.cell
def _(score):
    FLIP = {"C": "D", "D": "C"}

    def match_score(fn_a, fn_b, n, noise, rng):
        """Total points (A, B) and the number of cooperative moves in one match.
        A mistake (probability `noise`) flips the move a player intended."""
        history_a, history_b = [], []
        total_a = total_b = coop = 0
        for _ in range(n):
            move_a, move_b = fn_a(history_b), fn_b(history_a)
            if noise and rng.random() < noise:
                move_a = FLIP[move_a]
            if noise and rng.random() < noise:
                move_b = FLIP[move_b]
            points_a, points_b = score(move_a, move_b)
            total_a, total_b = total_a + points_a, total_b + points_b
            coop += (move_a == "C") + (move_b == "C")
            history_a.append(move_a)
            history_b.append(move_b)
        return total_a, total_b, coop

    return (match_score,)


@app.cell
def _(match_score, np, strategies):
    def tournament(population, n, noise, rng):
        """Everyone plays everyone once. Returns each agent's score and the share of
        cooperative moves in this generation."""
        scores = np.zeros(len(population))
        coop = 0
        for i in range(len(population)):
            for j in range(i + 1, len(population)):
                a, b, c = match_score(
                    strategies[population[i]], strategies[population[j]], n, noise, rng
                )
                scores[i] += a
                scores[j] += b
                coop += c
        pairs = len(population) * (len(population) - 1) / 2
        return scores, coop / (2 * n * pairs)

    return (tournament,)


@app.cell
def _(np):
    def select(population, scores, k, rng):
        """The k lowest scorers are replaced by copies of the k highest."""
        order = np.lexsort((rng.random(len(scores)), scores))  # ascending; ties random
        worst, best = order[:k], order[-k:]
        population = population.copy()
        # TODO 1 (selection): make the k worst agents copies of the k best.
        # `worst` and `best` are index arrays into `population`. One line.
        raise NotImplementedError("TODO 1: population[worst] = ...")
        return population

    return (select,)


@app.cell
def _(np, pd, select, tournament):
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

    return (evolve,)


@app.cell
def _(mo, strategies):
    start = {"copycat": 20, "devil": 5}
    counts = mo.ui.dictionary(
        {
            s: mo.ui.number(start=0, stop=50, value=start.get(s, 0), label=s)
            for s in strategies
        },
        label="starting population",
    )
    rounds = mo.ui.slider(1, 30, value=10, label="rounds per match")
    noise = mo.ui.slider(0, 0.3, step=0.01, value=0, label="noise")
    generations = mo.ui.slider(5, 60, value=30, label="generations")
    seed = mo.ui.number(start=0, stop=999, value=0, label="seed")
    mo.hstack([counts, mo.vstack([rounds, noise, generations, seed])], justify="start")
    return counts, generations, noise, rounds, seed


@app.cell
def _(counts, evolve, generations, mo, noise, rounds, seed):
    mo.stop(
        sum(counts.value.values()) < 10,
        mo.md("Need at least **10** agents (5 are replaced each generation)."),
    )
    history = evolve(
        counts.value, rounds.value, noise.value, generations.value, 5, seed.value
    )
    return (history,)


@app.cell
def _(alt, history):
    _shares = (
        alt.Chart(history)
        .mark_area()
        .encode(
            x=alt.X("generation:Q"),
            y=alt.Y("share:Q", stack="normalize", title="population share"),
            color=alt.Color("strategy:N", title=None),
        )
        .properties(width=520, height=220, title="Who is in the population?")
    )
    _coop = (
        alt.Chart(history.drop_duplicates("generation"))
        .mark_line(point=True)
        .encode(
            x=alt.X("generation:Q"),
            y=alt.Y(
                "cooperation:Q",
                title="share of cooperative moves",
                scale=alt.Scale(domain=[0, 1]),
            ),
        )
        .properties(width=520, height=140, title="How much cooperation is there?")
    )
    alt.vconcat(_shares, _coop)
    return


@app.cell
def _(history, mo):
    _final = history[history.generation == history.generation.max()]
    mo.md(
        f"Final cooperation: **{_final.cooperation.iloc[0]:.2f}** · "
        f"largest group: **{_final.loc[_final.share.idxmax(), 'strategy']}**"
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Three runs — predict each one first

    1. **No noise.** 20 Copycats, 5 Devils. Who is left? How much cooperation?
    2. **Add mistakes:** `noise` = 0.05. Does Copycat still win? What happens to
       cooperation? (Remember the echo from 02.)
    3. **Rescue:** swap 5 Copycats for 5 **Copykittens** (15 / 5 / 5), noise still
       0.05. Who wins now — and what happens to cooperation?

    Change the `seed` on runs 2 and 3: is the result luck, or robust?
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ::: {.callout-tip}
    ## ✅ It works when
    The hole is filled and your three runs end with cooperation ≈ **1.0**,
    ≈ **0.8** and ≈ **0.94** (±0.03 across seeds) — and you can say in one
    sentence why forgiving one mistake beats copying it.
    :::
    """)
    return


if __name__ == "__main__":
    app.run()
