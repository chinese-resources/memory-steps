# Memory Steps: Universal Ladder Player

Memory Steps is an Anki add-on for line-by-line memorization of Scripture, poems, speeches, quotations, language-learning passages, and other texts where exact wording matters.

## What changed in 1.0.0

Memory Steps now uses a **Universal Ladder Player** architecture:

- One Anki card is generated for each line of text.
- The 12 memorization steps are embedded inside that card.
- The front template includes an interactive ladder player with Recall mode and Training mode.
- There are no sibling step cards to bury.
- There is no desktop-only post-answer unlock hook.
- The same review flow works on Anki desktop, AnkiMobile, AnkiDroid, and AnkiWeb.

## Review workflow

Use **Recall** for normal review: it starts with the hardest cue. Tap **Need hint** only when needed.

Use **Train** for first-time learning: it starts with the full line and moves toward harder prompts.

Desktop keys: `H`/left arrow = easier hint, `L`/right arrow = harder prompt, `R` = Recall, `T` = Train, `F` = Full line.

Grade honestly: Easy = no hint, Good = small hint, Hard = several hints, Again = full answer needed.

## Why this works on mobile

The ladder is part of the synced card template and note fields. Anki schedules one card per line. No Python code needs to run after an answer, and no future step card needs to be unburied or unsuspended.

## Importing text

Use `Tools → Memory Steps → Import Text` in Anki desktop. Each imported line becomes one card. New cards are ordered by line number. Sync to mobile after importing if desired.

## Legacy notes

Version 1.0.0 creates a new note type named `Memory Steps: Universal Ladder`. Older imports used `Memory Steps: Line-by-Line Memorizer` and are not automatically migrated. For the cleanest mobile-safe experience, re-import texts with version 1.0.0 or later.

## Build

```bash
python3 scripts/build_release.py
```

This creates `dist/memory_steps_1.0.0.ankiaddon`, a manual install zip, and source-bundle files.

## License

GPL-3.0-or-later.
