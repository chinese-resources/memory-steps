# Memory Steps: Line-by-Line Memorizer

Memory Steps is an Anki desktop add-on for line-by-line memorization. It supports 12-step memory ladders for CJK character memorization, English word initials, English word outlines, and cloze-style word hiding.

## Version

`0.9.7`

## Features

- 12-step memorization ladders.
- CJK, Latin, and Mixed layout profiles.
- English blanks use width-preserving HTML underline spans instead of repeated underscores.
- Dashboard includes a `Mode` column so duplicate texts with different ladder models are distinguishable.
- Importer splits numbered text after closing quotes before verse numbers.
- Step-gated unlocking: the next memory step unlocks after the current Anki learning step graduates.

## Build

```bash
python3 scripts/build_release.py
```

The script creates:

```text
dist/memory_steps_0.9.7.ankiaddon
dist/memory_steps_manual_install_0.9.7.zip
dist/memory_steps_source_bundle_0.9.7_base64.txt
```

## AnkiWeb note

The `.ankiaddon` archive is intentionally built with `__init__.py` at the root of the archive, not inside a top-level `memory_steps/` folder.
