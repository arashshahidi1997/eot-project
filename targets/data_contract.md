# Data contract — tournament DataFrame

Your tournament must produce a tidy DataFrame with **one row per ordered pairing**
and exactly these columns (the heatmap and the checks both read from it):

| column | type | meaning |
|---|---|---|
| `strategy_a` | str | the row ("player") strategy name |
| `strategy_b` | str | the column ("opponent") strategy name |
| `rounds` | int | match length (10) |
| `score_a` | int | total points `strategy_a` earned in the match |
| `score_b` | int | total points `strategy_b` earned in the match |
| `mean_payoff_a` | float | `score_a / rounds` — the heatmap colour |
| `mean_payoff_b` | float | `score_b / rounds` |

5 strategies × 5 opponents (incl. self-play) → **25 rows**. The heatmap pivots
`mean_payoff_a` over `strategy_a` (rows) × `strategy_b` (columns).
