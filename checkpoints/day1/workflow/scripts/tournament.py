"""Every strategy vs every strategy, 10 rounds, no noise — the 03 tournament."""

from eot import STRATEGIES, round_robin

round_robin(list(STRATEGIES), snakemake.params.rounds).to_csv(  # noqa: F821
    snakemake.output[0],  # noqa: F821
    index=False,
)
