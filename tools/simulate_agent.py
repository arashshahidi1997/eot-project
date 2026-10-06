"""Day 3 · 20 — plays your agent, so everyone reviews the same diff.

    pixi run python tools/simulate_agent.py

"I tidied up game.py and added a test." Three edits — two useful, one not.
Your job: find out which, and keep only what should survive.
"""

import re
from pathlib import Path

game = Path("src/eot/game.py")
tests = Path("tests/test_eot.py")
src = game.read_text(encoding="utf-8")

# 1. Docstrings for the two simplest strategies.
for name, doc in [("angel", "Always cooperate."), ("devil", "Always defect.")]:
    src = re.sub(
        rf'(def {name}\(opponent_history\):\n)(?!\s+""")',
        rf'\1    """{doc}"""\n',
        src,
    )

# 2. "Textbook" payoffs.
src = re.sub(r"^(R, S, T, P = 2, -1, )3(, 0)", r"\g<1>5\2", src, flags=re.M)
game.write_text(src, encoding="utf-8")

# 3. A test for copycat's opening move.
t = tests.read_text(encoding="utf-8")
if "test_copycat_opens_with_cooperation" not in t:
    tests.write_text(
        t.rstrip("\n")
        + '\n\n\ndef test_copycat_opens_with_cooperation():\n'
        + '    assert STRATEGIES["copycat"]([]) == "C"\n',
        encoding="utf-8",
    )

print("Agent: I tidied up game.py and added a test. 3 edits in 2 files.")
