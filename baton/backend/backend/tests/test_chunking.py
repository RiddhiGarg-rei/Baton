from app.chunking import chunk_text


def test_empty_text_gives_no_chunks():
    assert chunk_text("") == []
    assert chunk_text("   \n\n  ") == []


def test_short_text_is_one_chunk_with_line_range():
    chunks = chunk_text("one\ntwo\nthree")
    assert len(chunks) == 1
    assert (chunks[0].start_line, chunks[0].end_line) == (1, 3)
    assert chunks[0].text == "one\ntwo\nthree"


def test_chunks_match_original_lines_exactly():
    lines = [f"line {i}" if i % 7 else "" for i in range(1, 101)]
    text = "\n".join(lines)
    chunks = chunk_text(text, max_chars=60)
    assert len(chunks) > 3
    previous_end = 0
    for c in chunks:
        # each chunk's text is exactly the original lines it claims to cover
        assert c.text == "\n".join(lines[c.start_line - 1 : c.end_line]).strip("\n")
        assert c.start_line > previous_end  # no overlap, in order
        previous_end = c.end_line
    assert [c.index for c in chunks] == list(range(len(chunks)))


def test_blank_line_splits_paragraphs_once_chunk_is_half_full():
    text = "a" * 30 + "\n\n" + "b" * 30
    chunks = chunk_text(text, max_chars=50)
    assert [c.text for c in chunks] == ["a" * 30, "b" * 30]
    assert chunks[1].start_line == 3


def test_oversized_line_becomes_its_own_chunk():
    chunks = chunk_text("short\n" + "x" * 500 + "\nshort again", max_chars=100)
    assert any(len(c.text) == 500 for c in chunks)
    assert all(c.start_line <= c.end_line for c in chunks)
