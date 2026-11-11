"""Step 2b: hide sensitive details before anything is stored.

Redaction never changes the number of lines, so the line numbers used in
citations still match the original file.

This is pattern matching, not magic: it catches common emails, phone numbers,
and secrets, but it will miss unusual formats. Treat it as a safety net, not
a guarantee.
"""
import re
from dataclasses import dataclass, field

_SECRET_WORDS = r"(?:api[_-]?key|secret|token|password|passwd|pwd)"

# (rule name, compiled pattern, replacement). Order matters: secrets first.
_RULES = [
    (
        "secret",
        re.compile(rf"(?i)\b({_SECRET_WORDS})\b(\s*[:=]\s*)(\S+)"),
        lambda m: f"{m.group(1)}{m.group(2)}[REDACTED:SECRET]",
    ),
    ("token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"), "[REDACTED:TOKEN]"),
    ("token", re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "[REDACTED:TOKEN]"),
    ("token", re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"), "[REDACTED:TOKEN]"),
    (
        "email",
        re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"),
        "[REDACTED:EMAIL]",
    ),
    (
        "phone",
        re.compile(r"(?<![\w+])\+\d{1,3}[\s-]?\d{3,5}[\s-]?\d{3,5}(?:[\s-]?\d{1,4})?(?!\d)"),
        "[REDACTED:PHONE]",
    ),
    ("phone", re.compile(r"(?<!\d)[6-9]\d{4}[\s-]\d{5}(?!\d)"), "[REDACTED:PHONE]"),
    ("phone", re.compile(r"(?<!\d)[6-9]\d{9}(?!\d)"), "[REDACTED:PHONE]"),
]


@dataclass
class RedactionResult:
    text: str
    counts: dict[str, int] = field(default_factory=dict)

    @property
    def total(self) -> int:
        return sum(self.counts.values())


def redact(text: str) -> RedactionResult:
    counts: dict[str, int] = {}
    for name, pattern, replacement in _RULES:
        text, n = pattern.subn(replacement, text)
        if n:
            counts[name] = counts.get(name, 0) + n
    return RedactionResult(text=text, counts=counts)
