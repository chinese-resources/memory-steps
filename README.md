# Memory Steps: Line-by-Line Memorizer
An Anki Add-On designed to memorize word-for-word line-by-line Scripture, poems, speeches, etc. in Chinese, Japanese, Korean, English, and other languages.

Inspired by https://github.com/zefanja/bible-memorizer/ but with a different method and workflow. It was originally built for Chinese Bible memorization, but it now supports Chinese, English, mixed-language texts, poems, speeches, scripture passages, quotations, language-learning material, and any other text you want to know by heart.

Instead of asking you to memorize a whole passage all at once, Memory Steps turns each line into a sequence of gradually harder prompts. You read the full line first, then review versions with more and more of the text hidden, until you can recall the line from only a reference, label, or minimal cue.

## Brief Changelog

### 0.9.8

- Added ladder-mode cleanup: completed intermediate step cards can be deleted after a line is learned, while the final card remains for long-term review.
- Added a dashboard cleanup button for deleting intermediate step cards from already-learned lines.
- Changed ladder advancement to move to the next step immediately after a non-Again answer, instead of waiting for Anki's learning delay to graduate the card.
- Improved numbered text splitting after English and CJK punctuation, including verse numbers followed by opening quotes.
- Fixed English anchor-word and punctuation-skeleton prompts so they use correctly sized word blanks.
- Made learned/unlearned progress tags mutually exclusive.

## What It Does

Memory Steps creates a structured memorization ladder inside Anki.

When you import a text, the add-on:

1. Splits the text into lines.
2. Detects or uses labels such as verse numbers, line numbers, or section names.
3. Generates 12 cards for each line.
4. Starts with only the first card available.
5. Unlocks the next memory step after a non-Again answer.
6. Suspends completed intermediate steps so only the current ladder step stays active.
7. Deletes completed intermediate step cards when the line is learned, keeping the final long-term review card.
8. Unlocks the next line after the previous line has been learned.

This gives you a controlled path through the text. You are not flooded with every card at once, and you do not have to manually manage which prompt comes next.


## Mobile and Sibling-Burying Requirement

Memory Steps currently uses Anki desktop add-on code to advance the ladder after each successful answer. Desktop Anki runs this Python hook; AnkiMobile, AnkiDroid, and AnkiWeb do not run desktop Python add-ons. If you review a Memory Steps card on mobile, the add-on cannot unlock or unbury the next ladder step after the answer.

Because each line is implemented as one Anki note with 12 sibling cards, Anki's sibling-burying feature can hide the remaining ladder steps after you answer one step. For Memory Steps, the deck used for these cards must have sibling burying turned off.

Required deck option for the Memory Steps deck:

```text
Bury siblings: Do not bury siblings
```

If your Anki version shows separate burying controls, turn all of these off for the Memory Steps deck/options group:

```text
Bury new siblings: off
Bury review siblings: off
Bury interday learning siblings: off
```

Recommended workflow for the current desktop-gated ladder mode:

1. Import and activate Memory Steps material on Anki desktop.
2. Make sure the Memory Steps deck has sibling burying disabled.
3. Do ladder progression reviews on Anki desktop when you need automatic step unlocking.
4. If you reviewed on mobile and the next step is hidden, sync back to desktop and use Anki's Unbury action or reactivate the line from the Memory Steps dashboard.

Mobile-safe ladder progression is planned as a separate architecture: instead of unlocking one sibling at a time after each answer, the active line would pre-release all 12 steps in order so mobile clients do not need desktop add-on code between answers.

## Why Use It?

Memory Steps is designed for people who want exact recall, not just recognition.

It is useful for:

- Scripture and Bible memorization.
- Poetry.
- Speeches.
- Classical texts.
- Language-learning passages.
- Quotations.
- Prayers, creeds, catechisms, songs, or liturgical texts.
- Any passage where the exact wording matters.

The goal is to make memorization feel more manageable by breaking it down into individual steps.

## How the Memorization Ladder Works

Each line becomes a 12-step ladder. The exact prompts depend on the memorization mode you choose.

For English and other Latin-script texts, Memory Steps can use word-based prompts:

- Full line.
- Word initials.
- Alternating word initials.
- Word outlines.
- Hidden vowels.
- Every few words hidden.
- Anchor words.
- Punctuation skeleton.
- Label plus first word.
- Label only.

For Chinese and CJK (Chinese, Japanese, Korean) texts, Memory Steps can use character-based prompts:

- Full line.
- Alternating visible characters.
- Every third, fourth, or fifth character.
- First and last character per phrase.
- Anchor words.
- Punctuation skeleton.
- First character plus punctuation.
- Label plus first character.
- Label only.

For cloze-style practice, Memory Steps hides whole words while preserving their approximate width, so the prompt layout stays visually aligned with the answer.

## Memorization Modes

Memory Steps includes four main modes.

### CJK Character Steps

Best for Chinese, Japanese, Korean, and mixed texts where character-level recall is useful.

This mode hides characters progressively while keeping punctuation and structure visible.

### Word Initial Steps

Best for English prose, speeches, scripture passages, and quotations.

This mode gives you initials as recall cues, then gradually removes support.

Example idea:

```text
In the beginning God created the heaven and the earth.
I t b G c t h a t e.
```

### Word Outline Steps

Best when initials feel too sparse.

This mode keeps the shape of words by showing first and last letters while hiding the middle. It gives more support than initials but less than the full text.

### Cloze Word Steps

Best for general-purpose memorization.

This mode hides whole words in a staged pattern. It is a good default for English and mixed-language texts.

## Basic Workflow

### 1. Install the Add-on

Download the `.ankiaddon` file from the release page and open it with Anki.

After installation, restart Anki. You should see a new menu:

```text
Tools -> Memory Steps
```

If you are installing manually, copy the `memory_steps` folder into Anki's `addons21` folder, then restart Anki.

### 2. Open the Import Dialog

In Anki, choose:

```text
Tools -> Memory Steps -> Import Text
```

Paste the text you want to memorize.

You can import text such as:

```text
1 In the beginning God created the heaven and the earth.
2 And the earth was without form, and void; and darkness was upon the face of the deep.
3 And God said, Let there be light: and there was light.
```

Or:

```text
静夜思
床前明月光，
疑是地上霜。
举头望明月，
低头思故乡。
```

### 3. Choose Your Settings

Before importing, choose:

- Text title / collection: the name of the passage. (Optional but helpful for dashboard use)
- Deck: where the cards should be created.
- Memorization mode: CJK, word initials, word outlines, or cloze words.
- Text layout: auto-detect, CJK, Latin, or mixed.
- Anchor-word profile: optional keywords to leave visible in some prompts. (These can be imported/exported and shared)
- Context window: how much surrounding text to show as context.

For most English texts, start with:

```text
Memorization mode: Cloze Word Steps
Text layout: Auto-detect
```

For Chinese texts, start with:

```text
Memorization mode: CJK Character Steps
Text layout: Auto-detect
```

### 4. Preview and Import

Click `Preview / Split Lines` to see how Memory Steps will divide your text.

If the lines look right, click `Import`.

Memory Steps will create the notes and cards in Anki. The first line's first step will be activated automatically. Later steps and later lines remain suspended until you earn them.

### 5. Review in Anki

Review the cards normally in Anki.

When you answer the current step with a non-Again rating, Memory Steps unlocks the next memorization step for that same line.

Completed intermediate steps are suspended as you move forward, so Anki does not keep scheduling every prompt in the ladder.

After you complete the final step for a line, Memory Steps marks that line as learned, deletes the intermediate learning-step cards for that line, keeps the final card for long-term review, and unlocks the first step of the next line.

This means your review flow looks like:

```text
Line 1, Step 1
Line 1, Step 2
Line 1, Step 3
...
Line 1, Step 12
Line 2, Step 1
Line 2, Step 2
...
```

You can keep using Anki normally. Memory Steps simply controls which generated cards are available at each stage.

## Dashboard

Open the dashboard from:

```text
Tools -> Memory Steps -> Dashboard
```

The dashboard shows your imported collections and their lines.

You can use it to:

- See how many lines are learned or unlearned.
- View each line's label, mode, and preview.
- Activate a selected line.
- Activate the next unlearned line.
- Delete intermediate step cards for already-learned lines.
- Open the import dialog.
- Open the practice dialog.

This is useful when you want to restart, inspect, or manually advance a passage.

## Practice Text View

Open practice mode from:

```text
Tools -> Memory Steps -> Practice Text
```

The practice view lets you render a whole imported text at a chosen prompt level.

For example, you can view:

- Label only.
- Step 2.
- Step 5.
- Step 12.
- Full text.

This is helpful for reciting an entire passage outside the normal Anki card flow.

## Settings

Open settings from:

```text
Tools -> Memory Steps -> Settings
```

Settings let you choose defaults and manage anchor-word profiles.

### Default Deck

The deck Memory Steps should use by default when importing new texts.

### Mask Character

The character used for hidden CJK characters and some text prompts.

The default is:

```text
＿
```

### Default Mode

The memorization mode selected by default in the import dialog.

### Default Layout

The visual layout selected by default.

Use `Auto-detect` unless you have a reason to force CJK, Latin, or mixed layout.

### Anchor Profiles

Anchor profiles are lists of words or phrases that Memory Steps can keep visible during anchor-word prompts.

For example, a scripture profile might keep words like:

```text
God
Lord
Christ
Spirit
faith
grace
truth
```

A Chinese poetry profile might keep words like:

```text
月
风
山
水
故乡
```

Anchor words are just memory handles. They give you a few stable points in a line while the rest of the text is hidden.

You can create, rename, delete, import, and export anchor profiles.

## Text Formatting Tips

Memory Steps works best when each line is a meaningful unit of memorization.

Good inputs:

```text
1 The Lord is my shepherd; I shall not want.
2 He maketh me to lie down in green pastures.
3 He leadeth me beside the still waters.
```

```text
1. Friends, Romans, countrymen, lend me your ears;
2. I come to bury Caesar, not to praise him.
```

```text
床前明月光，
疑是地上霜。
举头望明月，
低头思故乡。
```

If your text has verse numbers, Memory Steps will try to detect them as labels. It also tries to split numbered text after sentence-ending punctuation, including after closing quotes.

## Layouts

Memory Steps includes layout profiles so prompts are readable for different writing systems.

### Auto-detect

Recommended for most users. Memory Steps chooses CJK, Latin, or mixed layout based on the line content.

### CJK Character Layout

Uses larger character-focused formatting and wrapping behavior for Chinese/Japanese/Korean texts.

### Latin Word Layout

Uses word-oriented spacing and typography for English and other Latin-script texts.

### Mixed Layout

Useful for bilingual material or lines containing both CJK and Latin text.

## What Gets Created in Anki?

Memory Steps creates an Anki note type named:

```text
Memory Steps: Line-by-Line Memorizer
```

Each imported line is one note.

Each note has 12 card templates, one for each memorization step.

The note stores:

- Collection title.
- Line label.
- Full answer.
- Memorization mode.
- Layout profile.
- Anchor profile.
- Step prompts.
- Previous/next context.
- Learned status.

The generated cards are ordinary Anki cards, but Memory Steps manages their suspension state so the learning sequence stays ordered.

## Frequently Asked Questions

### Can I use this for English?

Yes. Use `Cloze Word Steps`, `Word Initial Steps`, or `Word Outline Steps`.

### Can I use this for Chinese?

Yes. Use `CJK Character Steps`.

### Can I use it for Bible memorization?

Yes. That was the original use case. It works well with verse-numbered text.

### Can I use it for non-religious texts?

Yes. Memory Steps is text-agnostic. It works for poetry, speeches, literature, language learning, and personal memorization projects.

### Why are only some cards available?

That is intentional. Memory Steps suspends future steps until you answer the current step successfully. This keeps your memorization path ordered.

### Can I manually activate a line?

Yes. Use the dashboard and click `Activate Selected/Next`.

### Can I edit the generated cards?

Yes, but be careful. Memory Steps depends on its note fields, tags, and card order. Editing text fields is usually fine. Deleting fields, templates, or cards may break the step flow.

### Does this sync through AnkiWeb?

The cards and notes sync like normal Anki content. The add-on itself must be installed separately on each desktop Anki installation where you want to use the Memory Steps menus and unlock behavior.

### Can I add audio to the cards?

Yes, there is an audio field on the back of the cards. You can use add-ons like AwesomeTTS to add high quality TTS audio or record your own.

## Troubleshooting

### I do not see the Memory Steps menu

Restart Anki after installing the add-on.

Then check:

```text
Tools -> Add-ons
```

Make sure Memory Steps is installed and enabled.

### My text split into lines incorrectly

Use `Preview / Split Lines` before importing.

If needed, manually insert line breaks where you want each memorization unit to begin.

### My English blanks look strange

Memory Steps uses width-preserving underline spans for hidden words. This is intentional: it keeps the prompt closer to the shape of the full answer.

### The next step did not unlock

The next Memory Steps prompt unlocks after a non-Again answer. If you answered Again, review the same step again before moving on.

You can also open the dashboard and activate a selected or next line manually.

## Installation Files

For normal Anki installation, use:

```text
memory_steps_0.9.8.ankiaddon
```

For manual installation, use:

```text
memory_steps_manual_install_0.9.8.zip
```

The manual install archive contains the `memory_steps` folder that can be copied into Anki's `addons21` directory.

## Building from Source

Most users do not need this section.

To run the smoke test and build release artifacts:

```bash
python3 scripts/smoke_test.py
python3 scripts/build_release.py
```

The build script creates:

```text
dist/memory_steps_0.9.8.ankiaddon
dist/memory_steps_manual_install_0.9.8.zip
dist/memory_steps_source_bundle_0.9.8_base64.txt
```

The `.ankiaddon` archive is built with `__init__.py` at the root of the archive, which is the structure Anki expects for add-on installation.

## License

Memory Steps is released under the GPL-3.0-or-later license.

See `LICENSE` and `COPYING` for details.
