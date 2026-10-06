**When does cooperation survive?** An Evolution of Trust simulation (Nicky Case,
ncase.me/trust): {{ snakemake.config["counts"] | length }} strategies play repeated
prisoner's dilemmas; each generation the 5 lowest scorers are replaced by copies of the
5 highest (a toy evolution rule), for {{ snakemake.config["generations"] }} generations.

Grid: rounds per match {{ snakemake.config["rounds"] }} × noise
{{ snakemake.config["noise"] }} × seeds {{ snakemake.config["seeds"] }}. Every figure
below was made by a rule in this workflow — open a figure to see the code and the
parameters behind it.
