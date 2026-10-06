import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

table = pd.concat(pd.read_csv(f, sep="\t") for f in snakemake.input)
table.to_csv(snakemake.output.tsv, sep="\t", index=False)

ax = table.plot.bar(x="subject", y="coop_rate", legend=False, figsize=(10, 3.5))
ax.set_ylim(0, 1)
ax.set_ylabel("cooperation rate")
ax.set_title(f"ds007822 · task-{table['task'].iloc[0]} · {len(table)} participants")
plt.tight_layout()
plt.savefig(snakemake.output.png, dpi=150)
