# Checkpoint — end of Day 1

The reference for exercises 05–09, released at 16:00: the `eot` package (`src/eot`),
the workflow (`workflow/`) and its parameters (`config/config.yaml`).

To start Day 2 from here, ask Claude:

> Back up my `src/`, `workflow/` and `config/`. Then copy `checkpoints/day1/src`,
> `workflow` and `config` into the project, and run `pixi run pytest` and
> `pixi run snakemake -n`.

Expect: 8 tests pass; the dry run lists 78 jobs; `pixi run snakemake -c4` takes ~20 s.
