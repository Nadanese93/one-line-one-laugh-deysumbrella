#!/usr/bin/env python3
"""One Line, One Laugh — Make.fun micro contest entry.

Writes a single one-line joke to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output), UTF-8, no trailing newline. Deterministic.
"""

import hashlib
import os
import sys

ENTRY = "The vending machine ate my dollar, gave me nothing, and still flashed 'thank you' like it did me a favor."


def verify(path):
    """Read the written file back and validate the contest gate."""
    with open(path, "rb") as f:
        raw = f.read()
    if raw.endswith(b"\n"):
        raise ValueError("entry must not end with a trailing newline")
    text = raw.decode("utf-8")
    if not 1 <= len(text) <= 140:
        raise ValueError("entry must be 1-140 characters, got %d" % len(text))
    if text != text.strip() or not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")
    if raw != text.encode("utf-8"):
        raise ValueError("entry bytes are not canonical UTF-8")
    if len(raw) != len(ENTRY.encode("utf-8")):
        raise ValueError("on-disk size does not match entry size")
    return hashlib.sha256(raw).hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    digest = verify(path)
    print("entry.txt written: %d chars, sha256=%s" % (len(ENTRY), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
