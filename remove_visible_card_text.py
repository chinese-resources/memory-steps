#!/usr/bin/env python3
"""Robustly remove visible instructional/helper text from Memory Steps card template.

Run from the repository root:

    python3 remove_visible_card_text.py

This removes card-facing blocks like:
- <div class=\"instructions\">...</div>
- <div class=\"keyboard-help\">...</div>

It handles both escaped quotes used inside Python string literals and unescaped
quotes if the template was edited manually.
"""
from __future__ import annotations

import re
from pathlib import Path

MODEL = Path("memory_steps/model.py")
if not MODEL.exists():
    raise SystemExit("Run this from the repository root; memory_steps/model.py was not found.")

text = MODEL.read_text(encoding="utf-8")
original = text

# Match both forms that can appear in model.py:
#   <div class=\"instructions\">...</div>
#   <div class="instructions">...</div>
# The [^<]* part is intentional: these helper blocks contain only text and inline <b> tags.
patterns = [
    r"<div class=\\\"instructions\\\">.*?</div>",
    r'<div class="instructions">.*?</div>',
    r"<div class=\\\"keyboard-help\\\">.*?</div>",
    r'<div class="keyboard-help">.*?</div>',
]

for pattern in patterns:
    text = re.sub(pattern, "", text)

for forbidden in [
    "Use the ladder player.",
    "No desktop hotkeys are assigned",
    "Desktop keys:",
    "avoid conflicts with Anki shortcuts",
]:
    if forbidden in text:
        raise SystemExit(
            f"Still found forbidden card-facing text: {forbidden!r}. "
            "Open memory_steps/model.py and remove the remaining helper text manually."
        )

if text == original:
    raise SystemExit(
        "No instruction/helper blocks were removed. The file may already be clean, "
        "or the template has changed. Search memory_steps/model.py for 'instructions' "
        "and 'keyboard-help'."
    )

MODEL.write_text(text, encoding="utf-8")
print("Removed visible instruction/hotkey helper text from memory_steps/model.py")
