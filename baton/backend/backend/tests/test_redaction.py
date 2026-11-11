from app.redaction import redact

SAMPLE = (
    "Reach me at test.user@example.com or +91 98765 43210 / 9876543210. "
    "api_key = sk-ABCDEFGHIJKLMNOPQRSTUV and password: hunter2. "
    "Meeting on 2026-03-12, see lines 14-18."
)


def test_sensitive_values_are_removed():
    result = redact(SAMPLE)
    for secret in ["test.user@example.com", "98765 43210", "9876543210",
                   "ABCDEFGHIJKLMNOPQRSTUV", "hunter2"]:
        assert secret not in result.text
    assert result.total == 5


def test_harmless_numbers_and_dates_survive():
    result = redact(SAMPLE)
    assert "2026-03-12" in result.text
    assert "lines 14-18" in result.text


def test_line_count_never_changes():
    text = "a@b.com\npassword: x\n\n9876543210\nplain line"
    assert redact(text).text.count("\n") == text.count("\n")


def test_clean_text_is_unchanged():
    text = "We decided to use PostgreSQL.\nOwner: Asha."
    result = redact(text)
    assert result.text == text and result.total == 0
