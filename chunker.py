"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def guard(text: str) -> list[str]:
    """
    Character windows that heading split does not reach.

    Two cases: a document with no headings at all, and a single section longer
    than CHUNK_SIZE.
    """
    if len(text) <= config.CHUNK_SIZE:
        return [text]
    return [c.text for c in fallback_split([Document(source="", text=text)])]


def split_one(doc: Document) -> list[str]:
    """The chunk texts for one document, in order."""
    headings = list(re.compile(r"(?m)^(#{1,2})[ \t]+(.+?)[ \t]*$").finditer(doc.text))
    if not headings:
        return guard(doc.text.strip())

    texts: list[str] = []

    preface = doc.text[: headings[0].start()].strip()
    if preface:
        texts.extend(guard(preface))

    scope = ""
    for position, heading in enumerate(headings):
        level = len(heading.group(1))
        title = heading.group(2).strip()

        if level == 1:
            scope = title
            label = title
        else:
            label = f"{scope} — {title}" if scope else title

        after = (
            headings[position + 1].start()
            if position + 1 < len(headings)
            else len(doc.text)
        )
        body = doc.text[heading.end() : after].strip()
        if not body:
            continue

        texts.extend(f"{label}\n\n{piece}" for piece in guard(body))

    return texts


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents on their Markdown headings with the H1 as a scope.

    city_guides documents are composed of labelled sections. Cutting 
    on sections means no cut off sentences.

    H1 of town specific guides provides a scope for chunks from that 
    document, giving town context to every chunk.

    Section splitting does not need an overlap since it is not an arbitrary 
    cut and thus does not need to repair anything. Applied inside 'guard' 
    which can call fallback_split applies an arbitrary cut and thus needs 
    the overlap repair again.
    """
    chunks: list[Chunk] = []
    for doc in documents:
        for index, text in enumerate(split_one(doc)):
            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )
    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
