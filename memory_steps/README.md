# Memory Steps: Universal Ladder Player

Memory Steps is an Anki add-on for line-by-line memorization.

## What changed in 1.0.0

Memory Steps uses a **Universal Ladder Player** architecture: one Anki card per line, with all 12 memorization steps embedded inside the card. There are no sibling step cards, no burying problem, and no desktop-only unlock hook.

## Review workflow

Use **Recall** for normal review. It starts with the hardest cue. Tap **Need hint** only when needed.

Use **Train** for first-time learning. Training alternates:

```text
prompt → check full line → harder prompt → check full line → even harder prompt → check full line
```

The **Check full line** button reveals the full answer without changing the current step. Tap **Back to step** to return to the same prompt.

No desktop hotkeys are assigned, to avoid conflicts with Anki shortcuts.

## Build

```bash
python3 scripts/build_release.py
```

This creates `dist/memory_steps_1.0.0.ankiaddon`, a manual install zip, and source-bundle files.
