"""One simulation: wildcards + config -> eot.simulate -> tidy CSV."""

from eot import simulate

w = snakemake.wildcards  # noqa: F821 — injected by Snakemake
config = {
    "counts": snakemake.params.counts,  # noqa: F821
    "rounds": int(w.rounds),
    "noise": float(w.noise),
    "generations": snakemake.params.generations,  # noqa: F821
}
df = simulate(config, seed=int(w.seed))
df.assign(rounds=config["rounds"], noise=config["noise"], seed=int(w.seed)).to_csv(
    snakemake.output[0],  # noqa: F821
    index=False,
)
