# Changelog

## 1.0.0

- Rebuilt Memory Steps around a Universal Ladder Player architecture.
- Changed imports to generate one Anki card per line instead of 12 sibling cards.
- Added in-card Recall mode and Training mode.
- Updated Training mode to alternate prompt → check full line → harder prompt → check full line.
- Changed full-line checking so it reveals the answer without changing the current ladder step.
- Removed desktop hotkeys to avoid conflicts with Anki shortcuts.
- Removed desktop-only post-answer step unlocking from the review path.

## 0.9.8

- Fixed English anchor-word and punctuation-skeleton prompts to use width-preserving word blanks.
- Improved numbered-text splitting after English and CJK punctuation, including punctuation-adjacent verse numbers.
- Switched memorization progression to ladder mode by suspending completed intermediate steps.
- Added learned-line cleanup to delete intermediate step cards while keeping the final long-term review card.
- Changed step advancement to unlock after non-Again answers instead of waiting for Anki learning delays.

## 0.9.7

- Restored deterministic release packaging and smoke-test scripts.
- Added GitHub Actions syntax, smoke-test, and packaging workflow.
- Updated release metadata from 0.9.5-publication-ready to 0.9.7.
- Hardened practice rendering so imported labels/text are escaped while Memory Steps blanks still render.
- Fixed anchor-profile list synchronization after add, rename, delete, and import operations.
- Made reviewer note-type detection more tolerant across Anki API versions.

## 0.9.5-publication-ready

- Added GitHub-ready repository structure.
- Added deterministic `scripts/build_release.py`.
- Added `scripts/smoke_test.py`.
- Added `.github/workflows/build.yml` for syntax/package checks.
- Kept v0.9.4 functional fixes: width-preserving English blanks, Dashboard Mode column, quote-aware importer splitting, lazy-loaded menu, CSS/model fix, and 12-step ladders.