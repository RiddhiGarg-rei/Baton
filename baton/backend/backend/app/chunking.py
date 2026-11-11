"""Step 2a: split text into chunks that remember where they came from.

Every chunk keeps the line range it covers in the original file. That line
range is what lets Baton later say "this claim comes from notes.md, lines
14-18" instead of just "somewhere in the notes".
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    index: int       # 0, 1, 2 ... order inside the source
    start_line: int  # 1-based, inclusive
    end_line: int    # 1-based, inclusive
    text: str


def chunk_text(text: str, max_chars: int = 800) -> list[Chunk]:
    """Group lines into chunks of roughly `max_chars` characters.

    Rules:
    - Lines are never cut in half, so line numbers stay exact.
    - Once a chunk is at least half full, a blank line ends it, which keeps
      paragraphs together where possible.
    - A single line longer than `max_chars` becomes its own chunk.
    - Blank lines at the edges of a chunk are dropped.
    """
    if max_chars < 1:
        raise ValueError("max_chars must be at least 1")

    min_chars = max_chars // 2
    chunks: list[Chunk] = []
    current: list[tuple[int, str]] = []  # (line number, line text)
    size = 0

    def flush() -> None:
        nonlocal current, size
        while current and not current[0][1].strip():
            current.pop(0)
        while current and not current[-1][1].strip():
            current.pop()
        if current:
            chunks.append(
                Chunk(
                    index=len(chunks),
                    start_line=current[0][0],
                    end_line=current[-1][0],
                    text="\n".join(line for _, line in current),
                )
            )
        current = []
        size = 0

    for number, line in enumerate(text.splitlines(), start=1):
        if current and size + len(line) + 1 > max_chars:
            flush()
        current.append((number, line))
        size += len(line) + 1
        if not line.strip() and size >= min_chars:
            flush()
    flush()
    return chunks
