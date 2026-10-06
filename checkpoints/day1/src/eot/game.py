"""The game: payoff for one round, and the five strategies (from 02)."""

R, S, T, P = 2, -1, 3, 0  # ncase payoffs


def score(move_a, move_b):
    """Points to (A, B) for one simultaneous round."""
    if move_a == "C" and move_b == "C":
        return R, R
    if move_a == "D" and move_b == "D":
        return P, P
    if move_a == "D" and move_b == "C":
        return T, S
    return S, T


# A strategy sees ONLY the opponent's past moves and returns its next move.
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
    return "D" if opponent_history[-2:] == ["D", "D"] else "C"


STRATEGIES = {
    "angel": angel,
    "devil": devil,
    "copycat": copycat,
    "grudger": grudger,
    "copykitten": copykitten,
}
