# Evolution of Trust — workshop project

Your project for Days 1–2 of **The Agentic Research Workflow** (GSN-LMU, Oct 2026).
Exercises and instructions: <https://arashshahidi1997.github.io/agentic-workshop/course/>

**Question:** *when does cooperation survive?*

## Start

```bash
pixi install
pixi run selftest
```

## Day 2 — the literature toolbox

```bash
pixi install -e lit       # once: Docling, search, Quarto (~0.7 GB, its own environment)
pixi task list            # convert · index · query · show · review
```

## What's here

- `notebooks/` — the Marimo notebooks you work in
- `targets/` — figures you reproduce, with their spec
- `src/eot/` — the model package (empty: you build it in the afternoon)
- `workflow/` — the Snakemake pipeline (afternoon)
- `library/` — the papers (Day 2): list, `references.bib`; the text comes from the Drive zip
- `tools/lit.py` — search the library (`pixi run query`, `pixi run show`)
- `notes/`, `reports/study.qmd` — your reading notes and your study (Day 2)

New material arrives during the day: your agent pulls it in (see the exercise pages).

Model: Nicky Case, *The Evolution of Trust* — <https://ncase.me/trust/>
