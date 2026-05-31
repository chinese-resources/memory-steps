#!/usr/bin/env python3
"""Remove visible Ladder Player explanation text from memory_steps/model.py.

Run from the repository root:

    python3 scripts/remove_card_instructions.py

Then rebuild:

    python3 scripts/smoke_test.py
    python3 scripts/build_release.py
"""
from __future__ import annotations

from pathlib import Path

MODEL = Path("memory_steps/model.py")
text = MODEL.read_text(encoding="utf-8")

known_blocks = [
    '<div class="instructions"><b>Use the ladder player.</b> Training starts by default and alternates prompt → check full line → continue to next step. On mobile, the controls stay compact and the prompt area scrolls when needed. Use Recall for normal review from the hardest cue.</div>',
    '<div class="instructions"><b>Use the ladder player.</b> Training starts by default and alternates prompt → check full line → continue to next step. Use Recall for normal review from the hardest cue.</div>',
    '<div class="instructions"><b>Use the ladder player.</b> Recall starts hard. Training alternates prompt → check full line → continue to next step.</div>',
    '<div class="instructions"><b>Use the ladder player.</b> Recall starts hard. Training alternates prompt → check full line → harder prompt → check full line.</div>',
]

changed = False
for block in known_blocks:
    if block in text:
        text = text.replace(block, "")
        changed = True

if not changed:
    raise SystemExit(
        "Could not find the visible Ladder Player instruction block. "
        "Check memory_steps/model.py and remove the <div class=\"instructions\">...</div> block manually."
    )

MODEL.write_text(text, encoding="utf-8")
print("Removed visible Ladder Player instruction text from memory_steps/model.py")
