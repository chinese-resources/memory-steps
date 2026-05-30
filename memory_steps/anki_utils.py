# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Memory Steps contributors

"""Anki collection helpers for Memory Steps.

The add-on models each memorization line as one note with twelve sibling
cards.  Only one sibling should be available at a time.  Anki can make
siblings unavailable in a few different ways (suspended, buried, or hidden
with a negative queue), so the gate/unlock helpers below intentionally clear
all negative queue states for the next *new* step card instead of only
handling queue == -1.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from aqt import mw

from .model import MODEL_NAME

FINAL_STEP_ORD = 11
PROGRESS_TAGS = {"ms_learned", "ms_unlearned"}
ADDON_PACKAGE = __name__.split(".")[0]


def _ids(ids: Iterable[int] | None) -> list[int]:
    return [int(cid) for cid in (ids or [])]


def _get_card(cid: int):
    return mw.col.get_card(int(cid))


def _card_ord(cid: int) -> int:
    try:
        return int(getattr(_get_card(cid), "ord", 0))
    except Exception:
        return 999


def _save_card(card) -> None:
    """Save a card across old and new Anki versions."""
    try:
        mw.col.update_card(card)
    except AttributeError:
        card.flush()


def _save_note(note) -> None:
    """Save a note across old and new Anki versions."""
    try:
        mw.col.update_note(note)
    except AttributeError:
        note.flush()


def refresh_collection() -> None:
    """Refresh scheduler/browser state after directly changing card queues."""
    try:
        mw.col.reset()
    except Exception:
        pass
    try:
        mw.reset()
    except Exception:
        pass


def card_ids_by_ord(note) -> dict[int, list[int]]:
    out: dict[int, list[int]] = defaultdict(list)
    for cid in note.card_ids():
        out[_card_ord(cid)].append(int(cid))
    return dict(out)


def all_card_ids_for_ord(note, ord_num: int) -> list[int]:
    return card_ids_by_ord(note).get(int(ord_num), [])


def cleanup_enabled() -> bool:
    try:
        cfg = mw.addonManager.getConfig(ADDON_PACKAGE) or {}
        return bool(cfg.get("delete_intermediate_step_cards_on_learned", True))
    except Exception:
        return True


def suspend_cards(ids: Iterable[int] | None) -> None:
    """Suspend cards, with a direct queue fallback for older Anki APIs."""
    ids = _ids(ids)
    if not ids:
        return

    try:
        mw.col.sched.suspend_cards(ids)
        return
    except Exception:
        pass

    for cid in ids:
        try:
            card = _get_card(cid)
            card.queue = -1
            _save_card(card)
        except Exception:
            pass


def _try_scheduler_unbury(ids: list[int]) -> None:
    """Best-effort unbury support across scheduler API versions."""
    if not ids:
        return

    sched = getattr(mw.col, "sched", None)
    if sched is None:
        return

    # Different Anki versions have exposed different unbury helpers.  Try the
    # narrow card-specific names first, then broader no-argument helpers.
    for name in ("unbury_cards", "unburyCards"):
        fn = getattr(sched, name, None)
        if fn:
            try:
                fn(ids)
                return
            except TypeError:
                pass
            except Exception:
                return

    for name in ("unbury_cards_for_deck", "unburyCardsForDeck", "unburyCards"):
        fn = getattr(sched, name, None)
        if fn:
            try:
                fn()
                return
            except Exception:
                pass


def unsuspend_cards(ids: Iterable[int] | None, due: int = 0) -> None:
    """Make the supplied step cards immediately available.

    This is deliberately stronger than a plain scheduler unsuspend.  Step
    cards are siblings, so deck options can bury/hide the next sibling after a
    review.  Any negative queue on a *new* step card means unavailable for the
    ladder, so we reset it to the new-card queue and assign a low due number.
    """
    ids = _ids(ids)
    if not ids:
        return

    try:
        mw.col.sched.unsuspend_cards(ids)
    except Exception:
        pass

    _try_scheduler_unbury(ids)

    for offset, cid in enumerate(sorted(ids, key=lambda x: (_card_ord(x), x))):
        try:
            card = _get_card(cid)
            card_type = int(getattr(card, "type", 0))
            queue = int(getattr(card, "queue", 0))

            if card_type == 0:
                # New cards can be suspended, buried, or otherwise hidden with
                # negative queue values.  All should become visible when this
                # step is unlocked.
                if queue < 0:
                    card.queue = 0
                card.due = int(due) + offset
            elif queue == -1:
                # Do not clobber learning/review scheduling, but do clear an
                # explicit suspension if a user manually suspended the card.
                card.queue = card_type

            _save_card(card)
        except Exception:
            pass


def delete_cards(ids: Iterable[int] | None) -> int:
    ids = _ids(ids)
    if not ids:
        return 0

    try:
        mw.col.remove_cards_and_orphaned_notes(ids)
        return len(ids)
    except Exception:
        pass

    try:
        mw.col.remCards(ids, False)
        return len(ids)
    except TypeError:
        try:
            mw.col.remCards(ids)
            return len(ids)
        except Exception:
            pass
    except Exception:
        pass

    return 0


def intermediate_step_card_ids(note) -> list[int]:
    ids: list[int] = []
    for ord_num, cids in card_ids_by_ord(note).items():
        if int(ord_num) < FINAL_STEP_ORD:
            ids.extend(cids)
    return ids


def delete_intermediate_step_cards(note) -> int:
    return delete_cards(intermediate_step_card_ids(note))


def set_progress_state(note, learned: bool) -> None:
    note["learned"] = "1" if learned else "0"
    try:
        note.tags = [tag for tag in note.tags if tag not in PROGRESS_TAGS]
    except Exception:
        for tag in PROGRESS_TAGS:
            try:
                note.del_tag(tag)
            except Exception:
                pass
    note.add_tag("ms_learned" if learned else "ms_unlearned")
    _save_note(note)


def initialize_note_step_gate(note, active: bool = False) -> None:
    """Hide all steps for a line, optionally activating step 1."""
    suspend_cards(note.card_ids())
    if active:
        unsuspend_cards(all_card_ids_for_ord(note, 0), 0)
        set_progress_state(note, False)
    refresh_collection()


def find_ms_notes(extra: str = ""):
    query = f'note:"{MODEL_NAME}"' + ((" " + extra) if extra else "")
    return [mw.col.get_note(nid) for nid in mw.col.find_notes(query)]


def grouped_collections() -> dict[str, list]:
    grouped: dict[str, list] = {}
    for note in find_ms_notes():
        grouped.setdefault(note["collection_id"], []).append(note)
    for notes in grouped.values():
        notes.sort(key=lambda note: int(note["line_index"] or 0))
    return grouped


def find_next_line(note):
    collection_id = note["collection_id"]
    line_index = int(note["line_index"] or 0)
    for candidate in find_ms_notes(f"collection_id:{collection_id}"):
        if int(candidate["line_index"] or 0) == line_index + 1:
            return candidate
    return None


def unlock_next_step_or_line(note, answered_ord: int):
    """Advance the ladder after a successful answer.

    Returns:
        ("step", next_ord, None) while still inside the current line.
        ("line", None, next_note, deleted_count) after the final step.
    """
    answered_ord = int(answered_ord)

    if answered_ord < FINAL_STEP_ORD:
        current_ids = all_card_ids_for_ord(note, answered_ord)
        next_ids = all_card_ids_for_ord(note, answered_ord + 1)
        suspend_cards(current_ids)
        unsuspend_cards(next_ids, 0)
        refresh_collection()
        return ("step", answered_ord + 1, None)

    set_progress_state(note, True)
    deleted = delete_intermediate_step_cards(note) if cleanup_enabled() else 0
    next_note = find_next_line(note)
    if next_note:
        initialize_note_step_gate(next_note, True)
    refresh_collection()
    return ("line", None, next_note, deleted)


def activate_note_first_step(note) -> list[int]:
    initialize_note_step_gate(note, True)
    return all_card_ids_for_ord(note, 0)


def cleanup_learned_step_cards(collection_id: str | None = None) -> tuple[int, int]:
    query = "learned:1"
    if collection_id:
        query += f" collection_id:{collection_id}"

    deleted = 0
    notes = 0
    for note in find_ms_notes(query):
        count = delete_intermediate_step_cards(note)
        if count:
            deleted += count
            notes += 1

    refresh_collection()
    return notes, deleted


def reconcile_all_progress() -> tuple[int, int]:
    """Repair tags/learned field for existing Memory Steps notes."""
    learned = 0
    unlearned = 0
    for note in find_ms_notes():
        is_learned = note["learned"] == "1"
        set_progress_state(note, is_learned)
        if is_learned:
            learned += 1
        else:
            unlearned += 1
    refresh_collection()
    return learned, unlearned
