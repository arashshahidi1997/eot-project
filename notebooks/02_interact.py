import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
        # 02 · Interact — two strategies, one match

        **Question all day:** *when does cooperation survive?*

        Start at the smallest scale: **two** strategies play the repeated prisoner's
        dilemma. You fill four small holes, then drive the slider and watch the
        notebook recompute itself — a **reactive dependency graph**, not a script.

        Fill the holes marked `TODO 1…4`. Each is one idea, not plumbing.
        """
    )
    return


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import pandas as pd

    return alt, mo, pd


@app.cell
def _():
    # Payoff points for one round (ncase numbers). Hardcoded on purpose —
    # today's lesson is reactivity, not payoff tuning.
    #                          opponent cooperates   opponent defects
    #   you cooperate                R = 2                 S = -1
    #   you defect                   T = 3                 P = 0
    R, S, T, P = 2, -1, 3, 0
    return P, R, S, T


@app.cell
def _(P, R, S, T):
    def score(move_a, move_b):
        """Points to (A, B) for one simultaneous round."""
        if move_a == "C" and move_b == "C":
            return R, R
        if move_a == "D" and move_b == "D":
            return P, P
        if move_a == "D" and move_b == "C":
            return T, S
        # TODO 1 (payoff rule): the last case — A cooperates, B defects.
        # What does each player get? Return (points_to_A, points_to_B).
        raise NotImplementedError("TODO 1: return the cheat-vs-cooperate payoff")

    return (score,)


@app.cell
def _():
    # Four strategies are written for you. A strategy sees ONLY the opponent's
    # past moves (a list like ["C", "D", ...]) and returns its next move.
    def angel(opponent_history):
        return "C"  # always cooperate

    def devil(opponent_history):
        return "D"  # always defect

    def grudger(opponent_history):
        # cooperate until the opponent ever defects, then defect forever
        return "D" if "D" in opponent_history else "C"

    def copykitten(opponent_history):
        # forgiving: defect only after TWO opponent defects in a row
        if (
            len(opponent_history) >= 2
            and opponent_history[-1] == "D"
            and opponent_history[-2] == "D"
        ):
            return "D"
        return "C"

    return angel, copykitten, devil, grudger


@app.cell
def _():
    def copycat(opponent_history):
        """Cooperate first, then copy the opponent's last move (tit-for-tat)."""
        if not opponent_history:
            return "C"
        # TODO 2 (strategy behavior): copy the OPPONENT's most recent move.
        # (You are handed only `opponent_history` — that is deliberate.)
        raise NotImplementedError("TODO 2: return the opponent's last move")

    return (copycat,)


@app.cell
def _(angel, copycat, copykitten, devil, grudger):
    strategies = {
        "angel": angel,
        "devil": devil,
        "copycat": copycat,
        "grudger": grudger,
        "copykitten": copykitten,
    }
    return (strategies,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ::: prediction
        **Predict before you run.** With Copycat vs Devil, who ends ahead, and by how
        much? What about Copycat vs **Copycat**? Write your guess, then check.
        :::
        """
    )
    return


@app.cell
def _(mo, strategies):
    strat_a_ui = mo.ui.dropdown(
        options=list(strategies), value="copycat", label="strategy A"
    )
    strat_b_ui = mo.ui.dropdown(
        options=list(strategies), value="devil", label="strategy B"
    )
    rounds = mo.ui.slider(1, 50, value=10, label="rounds")
    mo.hstack([strat_a_ui, strat_b_ui, rounds], justify="start")
    return rounds, strat_a_ui, strat_b_ui


@app.cell
def _(pd, score):
    def run_match(fn_a, fn_b, n):
        """Play n rounds; return one tidy row per round."""
        history_a, history_b = [], []
        rows = []
        cum_a = cum_b = 0
        for r in range(1, n + 1):
            move_a = fn_a(history_b)  # A reacts to B's past
            move_b = fn_b(history_a)  # B reacts to A's past
            # TODO 3 (simulate interaction): score this round.
            # Use score(move_a, move_b) -> (payoff to A, payoff to B).
            payoff_a, payoff_b = None, None  # <-- replace with the call to score(...)
            if payoff_a is None:
                raise NotImplementedError(
                    "TODO 3: payoff_a, payoff_b = score(move_a, move_b)"
                )
            cum_a += payoff_a
            cum_b += payoff_b
            rows.append(
                {
                    "round": r,
                    "move_a": move_a,
                    "move_b": move_b,
                    "cum_a": cum_a,
                    "cum_b": cum_b,
                }
            )
            history_a.append(move_a)
            history_b.append(move_b)
        return pd.DataFrame(rows)

    return (run_match,)


@app.cell
def _(rounds, run_match, strat_a_ui, strat_b_ui, strategies):
    fn_a = strategies[strat_a_ui.value]
    fn_b = strategies[strat_b_ui.value]
    # TODO 4 (reactive parameter): run the match for the number of rounds the
    # slider currently shows. A ui element's live value is `.value`.
    n = None  # <-- replace None with the slider's value
    if n is None:
        raise NotImplementedError("TODO 4: set n from the rounds slider")
    match_df = run_match(fn_a, fn_b, n)
    return (match_df,)


@app.cell
def _(alt, match_df):
    _long = match_df.melt(
        id_vars=["round"],
        value_vars=["cum_a", "cum_b"],
        var_name="player",
        value_name="cumulative_payoff",
    )
    alt.Chart(_long).mark_line(point=True).encode(
        x=alt.X("round:Q", title="round"),
        y=alt.Y("cumulative_payoff:Q", title="cumulative payoff"),
        color=alt.Color("player:N", title=None),
    ).properties(width=500, height=300, title="Cumulative payoff per round")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ::: prediction
        **Now drag the `rounds` slider.** Did the plot match your guess? Why does giving
        the match *more rounds* change who comes out ahead?
        :::
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ### See the reactive graph

        This notebook is **not** a top-to-bottom script — it's a dependency graph.
        Select the plot cell and open **Dependencies → Graph / Minimap**
        (`Cmd/Ctrl-Shift-I`). Trace the chain:

        `rounds → match_df → chart`

        Now move the slider and watch *only* that chain re-execute. Changing `rounds`
        can't leave a stale plot behind — marimo reruns every cell that depends on it.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ::: {.callout-tip}
        ## ✅ It works when
        The four `TODO`s are filled, moving the `rounds` slider updates the plot with
        **no stale cells**, and you can say in one sentence why more rounds helps
        Copycat against Devil.
        :::
        """
    )
    return


if __name__ == "__main__":
    app.run()
