#!/usr/bin/env python3
"""Remove visible hotkey/no-hotkey text from memory_steps/model.py.

Run from the repository root:

    python3 remove_hotkey_text.py

Then rebuild:

    python3 scripts/smoke_test.py
    python3 scripts/build_release.py
"""
from __future__ import annotations

from pathlib import Path

MODEL = Path("memory_steps/model.py")
text = MODEL.read_text(encoding="utf-8")

known_blocks = [
    '<div class="keyboard-help">No desktop hotkeys are assigned, to avoid conflicts with Anki shortcuts.</div>',
    '<div class="keyboard-help">Desktop keys: H/← easier hint · L/→ harder · R recall · T train · F full line.</div>',
]

changed = False
for block in known_blocks:
    if block in text:
        text = text.replace(block, "")
        changed = True

if not changed:
    raise SystemExit(
        "Could not find the visible hotkey/help text block. "
        "Check memory_steps/model.py and remove the <div class=\"keyboard-help\">...</div> block manually."
    )

MODEL.write_text(text, encoding="utf-8")
print("Removed visible hotkey/help text from memory_steps/model.py")
