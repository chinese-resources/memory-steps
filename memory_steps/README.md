# Memory Steps: Line-by-Line Memorizer

Memory Steps is an Anki desktop add-on for line-by-line memorization. It supports 12-step memory ladders for CJK character memorization, English word initials, English word outlines, and cloze-style word hiding.

## Version

`0.9.8`

## Features

- 12-step memorization ladders.
- CJK, Latin, and Mixed layout profiles.
- English blanks use width-preserving HTML underline spans instead of repeated underscores.
- Dashboard includes a `Mode` column so duplicate texts with different ladder models are distinguishable.
- Importer splits numbered text after closing quotes before verse numbers.
- Step-gated unlocking: non-Again answers unlock the next ladder step immediately.
- Learned-line cleanup deletes intermediate step cards while keeping the final long-term review card.


## Mobile / Sibling-Burying Requirement

Memory Steps currently depends on Anki desktop add-on code to unlock the next ladder step after a successful answer. Mobile clients do not run desktop Python add-ons, so mobile reviews cannot trigger automatic step unlocking.

The Memory Steps deck must also have sibling burying disabled, because each line is represented as 12 sibling cards from the same note.

Use this deck option:

```text
Bury siblings: Do not bury siblings
```

If your Anki version shows separate controls, turn off all sibling-burying options:

```text
Bury new siblings: off
Bury review siblings: off
Bury interday learning siblings: off
```

For now, do automatic ladder progression on Anki desktop. If a mobile review buries the remaining ladder steps, sync back to desktop and unbury/reactivate the line.

## Build

```bash
python3 scripts/build_release.py
```

The script creates:

```text
dist/memory_steps_0.9.8.ankiaddon
dist/memory_steps_manual_install_0.9.8.zip
dist/memory_steps_source_bundle_0.9.8_base64.txt
```

## AnkiWeb note

The `.ankiaddon` archive is intentionally built with `__init__.py` at the root of the archive, not inside a top-level `memory_steps/` folder.
