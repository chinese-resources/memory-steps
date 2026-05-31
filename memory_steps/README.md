# Memory Steps: Universal Ladder Player

Memory Steps is an Anki add-on for memorizing exact texts line by line: Scripture, poetry, speeches, quotations, prayers, catechisms, language-learning passages, and other texts where the exact wording matters.

Instead of asking you to memorize a whole passage at once, Memory Steps splits your text into lines and gives each line a 12-step memorization ladder.

## What’s New in 1.0.1

Version 1.0.1 is a mobile usability fix for the Universal Ladder Player.

It keeps the one-card-per-line architecture from 1.0.0, but improves the card template on mobile:

- The player starts in **Training Mode** at **Step 1**.
- The mobile layout is more compact.
- The controls stay visible above the prompt.
- Long prompts scroll inside the prompt area instead of pushing the buttons off-screen.
- No desktop hotkeys are assigned, to avoid conflicts with Anki shortcuts.

## Universal Ladder Player

The current version creates:

```text
1 Anki card per line
12 memory prompts inside that card
1 interactive Ladder Player
```

This means:

- Works on desktop and mobile.
- No sibling-card burying issues.
- No hidden or suspended future steps.
- No desktop-only unlock hook.
- One clean review card per memorized line.

## How It Works

Each imported line becomes one Anki card.

Inside that card, the Ladder Player shows one prompt at a time. The prompts go from easy to hard:

```text
Step 1  = easiest / most visible
Step 12 = hardest / minimal cue
```

You can use the player in two ways: **Training Mode** and **Recall Mode**.

## Training Mode

Training Mode is the default starting mode.

Use **Train** for first-time learning or extra practice. Training Mode walks you upward through the ladder:

```text
prompt → check full line → harder prompt → check full line → even harder prompt
```

This lets you attempt each step, reveal the full line to check your answer, then continue to a harder prompt.

## Recall Mode

Use **Recall** for normal reviews.

Recall Mode starts with the hardest cue. Try to recite the full line from memory. If you need help, tap:

```text
Need hint ←
```

This moves to an easier prompt.

Suggested grading:

```text
Easy  = recalled from the hardest cue
Good  = needed a small hint
Hard  = needed several hints
Again = needed the full answer
```

## Check Full Line

The **Check full line** button reveals the full answer without changing your current step.

```text
Current step → Check full line → Back to step
```

It does not jump back to the easiest step. It is only a temporary answer check.

## Memorization Modes

Memory Steps includes several prompt styles:

- **CJK Character Steps** — best for Chinese, Japanese, Korean, and mixed CJK texts.
- **Word Initial Steps** — best for English and other Latin-script texts.
- **Word Outline Steps** — uses initials, word shapes, hidden vowels, anchor words, and punctuation cues.
- **Cloze Word Steps** — progressively hides whole words while preserving approximate spacing.

## Importing Text

Import from Anki desktop:

```text
Tools → Memory Steps → Import Text
```

Then:

1. Enter a title.
2. Choose a deck.
3. Choose a memorization mode.
4. Paste your text.
5. Preview and split the lines.
6. Import.

Each line becomes one card, ordered by line number.

## Mobile Use

Import on Anki desktop, then sync to mobile.

Because the ladder is inside the card template, the review experience works on mobile without needing the desktop add-on to run during review.

## Legacy Notes

Version 1.0.1 uses this note type:

```text
Memory Steps: Universal Ladder
```

Older versions used:

```text
Memory Steps: Line-by-Line Memorizer
```

Old notes are not automatically migrated. For the best mobile-safe experience, re-import your texts with version 1.0.1 or later.

## Build From Source

From the repository root:

```bash
python3 scripts/build_release.py
```

This creates:

```text
dist/memory_steps_1.0.1.ankiaddon
dist/memory_steps_manual_install_1.0.1.zip
dist/memory_steps_source_bundle_1.0.1.zip
dist/memory_steps_source_bundle_1.0.1_base64.txt
```

Run the smoke test with:

```bash
python3 scripts/smoke_test.py
```

## License

GPL-3.0-or-later.
