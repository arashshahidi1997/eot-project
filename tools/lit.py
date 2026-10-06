"""Search the library by meaning or by words; show the evidence (optional, exercise 12).

pixi run index                                    # library/docling/*.json → library/index/
pixi run query "why does cooperation cycle?"      # by meaning (embeddings)
pixi run query "tit-for-tat" --by words           # by words (BM25)
pixi run show garcia2018:41                       # one chunk, in full, with its page
"""

import argparse
import functools
import json
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(
    encoding="utf-8"
)  # Windows consoles default to cp1252: ≈, →, λ crash

os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")  # quiet model loading
os.environ.setdefault("HF_HUB_VERBOSITY", "error")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")

LIB = Path(__file__).resolve().parents[1] / "library"
INDEX = LIB / "index"
MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # small, runs on any laptop
SKIP = (
    "reference",
    "bibliograph",
    "acknowledg",
    "competing interest",
    "funding",
    "author contrib",
)


def index():
    import numpy as np
    from docling.chunking import HybridChunker
    from docling_core.types.doc import DoclingDocument

    chunker = HybridChunker()
    chunks = []
    for path in sorted((LIB / "docling").glob("*.json")):
        doc = DoclingDocument.load_from_json(path)
        for i, ch in enumerate(chunker.chunk(doc)):
            section = " > ".join(ch.meta.headings or [])
            # reference lists match every query: leave them out
            if any(word in section.lower() for word in SKIP):
                continue
            pages = sorted({p.page_no for item in ch.meta.doc_items for p in item.prov})
            chunks.append(
                {
                    "id": f"{path.stem}:{i}",
                    "pages": pages,
                    "section": section,
                    "text": ch.text,
                    "embed": chunker.contextualize(ch),  # section headings + text
                }
            )
    vectors = model().encode(
        [c.pop("embed") for c in chunks], normalize_embeddings=True
    )
    INDEX.mkdir(exist_ok=True)
    np.save(INDEX / "embeddings.npy", vectors)
    with open(INDEX / "chunks.jsonl", "w", encoding="utf-8") as f:
        f.writelines(json.dumps(c) + "\n" for c in chunks)
    papers = len({c["id"].split(":")[0] for c in chunks})
    tokens = sum(len(c["text"]) for c in chunks) // 4
    print(f"{papers} papers · {len(chunks)} chunks · ≈{tokens // 1000}k tokens in all")


def load():
    return [json.loads(line) for line in open(INDEX / "chunks.jsonl", encoding="utf-8")]


# Loaded once per process: each CLI call reloads it.
@functools.cache
def model():
    import transformers
    from sentence_transformers import SentenceTransformer

    transformers.logging.disable_progress_bar()
    return SentenceTransformer(MODEL)


def search(text, by="meaning", k=5):
    """The top-k chunks for `text`, each with its score."""
    import numpy as np

    chunks = load()
    if by == "meaning":
        q = model().encode([text], normalize_embeddings=True)[0]
        scores = np.load(INDEX / "embeddings.npy") @ q  # cosine similarity
    else:
        import bm25s

        words = lambda t: bm25s.tokenize(
            t, stopwords="en", return_ids=False, show_progress=False
        )
        bm25 = bm25s.BM25()
        bm25.index(words([c["text"] for c in chunks]), show_progress=False)
        # exact words only: "cycle" won't find "cycles"
        scores = bm25.get_scores(words(text)[0])
    return [
        chunks[i] | {"score": round(float(scores[i]), 2)}
        for i in np.argsort(-scores)[:k]
    ]


def query(text, by, k):
    for rank, c in enumerate(search(text, by, k), 1):
        print(
            f"{rank}. {c['id']}  p.{','.join(map(str, c['pages']))}  {c['section'][:60]}  [{c['score']}]"
        )
        print(f"   {c['text'][:200].replace(chr(10), ' ')}…\n")


def show(chunk_id):
    c = next((c for c in load() if c["id"] == chunk_id), None)
    if c is None:
        sys.exit(
            f"no chunk {chunk_id} — ids look like garcia2018:41 (see pixi run query)"
        )
    key = chunk_id.split(":")[0]
    print(f"{chunk_id} · {c['section']}\n\n{c['text']}\n")
    print(
        f"Check it: library/pdf/{key}.pdf, page {', '.join(map(str, c['pages']))} · cite as [@{key}]"
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("index")
    q = sub.add_parser("query")
    q.add_argument("text")
    q.add_argument("--by", choices=["meaning", "words"], default="meaning")
    q.add_argument("-k", type=int, default=5)
    s = sub.add_parser("show")
    s.add_argument("chunk_id")
    a = ap.parse_args()
    {
        "index": index,
        "query": lambda: query(a.text, a.by, a.k),
        "show": lambda: show(a.chunk_id),
    }[a.cmd]()
