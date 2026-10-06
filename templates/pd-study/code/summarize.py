import pandas as pd

events = pd.read_csv(snakemake.input[0], sep="\t")
choices = events["choice"].dropna()  # "n/a" rows are not choices
summary = pd.DataFrame(
    {
        "subject": [snakemake.wildcards.subject],
        "task": [snakemake.wildcards.task],
        "n_trials": [len(choices)],
        "coop_rate": [(choices == 1).mean()],  # 1 = cooperate (see 22)
    }
)
summary.to_csv(snakemake.output[0], sep="\t", index=False)
