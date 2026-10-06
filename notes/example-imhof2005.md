# imhof2005 — Evolutionary cycles of cooperation and defection

question:    In a finite population, do ALLD, ALLC and TFT settle on ALLD (the only strict
             Nash equilibrium), or does something else happen?
model:       ALLD, ALLC, TFT (= our Devil, Angel, Copycat); repeated game of m rounds;
             TFT pays a small complexity cost c; a Moran process with mutation u.
finding:     The population cycles ALLD → TFT → ALLC → ALLD, and for the right population
             size it spends most of its time at TFT.
parameters:  T = 5, R = 3, P = 1, S = 0.1; m = 10 rounds; c = 0.8; population size N;
             mutation rate u.
limits:      No mistakes (noise) in the main model; three strategies only.
for us:      Our Day-1 model has no mutation, so once Devil is gone it never comes back.
             Add mutation → does the Devil → Copycat → Angel loop recur?

## Evidence

- The loop exists — "The population cycles from ALLD to TFT to ALLC and back to ALLD." (abstract)
- Time sits on TFT — "the time average of these oscillations can be entirely concentrated
  on TFT" (abstract)
- The loop has a direction — "transitions from ALLC to ALLD, from ALLD to TFT, and from TFT
  to ALLC are much more likely than the corresponding reverse transitions" (main text)
- Mistakes speed the cycle up — "with errors, the population leaves TFT sooner" (main text)
- Infinite populations need enough mutation for a cycle — "If the mutation rate exceeds a
  critical value, a stable limit cycle forms around this mixed equilibrium" (main text)
- Noise is future work — "A natural extension of our work would be to accommodate the
  possibility that players make mistakes" (main text)
