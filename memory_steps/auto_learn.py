# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Memory Steps contributors

"""Automatically advance Memory Steps ladder cards after correct answers."""

from __future__ import annotations

import traceback

from aqt import gui_hooks
from aqt.utils import tooltip

from .anki_utils import unlock_next_step_or_line
from .model import MODEL_NAME


def _card_from_args(*args):
    for arg in args:
        if hasattr(arg, "note") and hasattr(arg, "id"):
            return arg
    return None


def _ease_from_args(*args):
    for arg in reversed(args):
        if isinstance(arg, int):
            return arg
    return None


def _note_type_name(note) -> str:
    try:
        note_type = note.note_type()
    except Exception:
        try:
            note_type = note.model()
        except Exception:
            return ""
    return note_type.get("name", "") if isinstance(note_type, dict) else ""


def _is_memory_steps_card(card) -> bool:
    try:
        note = card.note()
        return _note_type_name(note) == MODEL_NAME
    except Exception:
        return False


def _format_success_tooltip(status: str, step, note, next_note, deleted: int) -> str:
    if status == "step":
        return f"Next memorization step unlocked: {int(step) + 1}/12"

    message = "Line learned: " + note["label"]
    if deleted:
        message += "\nDeleted learning-step cards: " + str(deleted)
    if next_note:
        message += "\nNext line unlocked: " + next_note["label"]
    return message


def _reviewer_did_answer_card(*args) -> None:
    """Advance on Hard/Good/Easy, but not Again.

    New-style Anki hook signature is (reviewer, card, ease).  The helper
    functions above keep this tolerant of older/variant hook argument order.
    """
    card = _card_from_args(*args)
    if not card or not _is_memory_steps_card(card):
        return

    try:
        note = card.note()
        if note["learned"] == "1":
            return

        ease = _ease_from_args(*args)
        if ease == 1:
            tooltip("Review this memory step again before moving on.")
            return

        result = unlock_next_step_or_line(note, int(getattr(card, "ord", 0)))
        status, step, next_note = result[:3]
        deleted = result[3] if len(result) > 3 else 0
        tooltip(_format_success_tooltip(status, step, note, next_note, deleted))

    except Exception as exc:
        # Do not silently swallow ladder failures.  In Anki launched from a
        # terminal, this gives a full traceback; in normal use, the tooltip at
        # least exposes the error class/message.
        print("Memory Steps auto-learn error:")
        print(traceback.format_exc())
        tooltip(f"Memory Steps error: {type(exc).__name__}: {exc}")


try:
    gui_hooks.reviewer_did_answer_card.append(_reviewer_did_answer_card)
except Exception as exc:
    print(f"Memory Steps could not register reviewer hook: {type(exc).__name__}: {exc}")
