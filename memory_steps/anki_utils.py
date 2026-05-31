# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Memory Steps contributors
"""Collection helpers for the universal Memory Steps architecture."""
from __future__ import annotations
from aqt import mw
from .model import MODEL_NAME
PROGRESS_TAGS={"ms_learned","ms_unlearned"}
def refresh_collection():
    try: mw.col.reset()
    except Exception: pass
    try: mw.reset()
    except Exception: pass
def _save_note(note):
    try: mw.col.update_note(note)
    except AttributeError: note.flush()
def _save_card(card):
    try: mw.col.update_card(card)
    except AttributeError: card.flush()
def set_progress_state(note, learned):
    note["learned"]="1" if learned else "0"
    try: note.tags=[tag for tag in note.tags if tag not in PROGRESS_TAGS]
    except Exception:
        for tag in PROGRESS_TAGS:
            try: note.del_tag(tag)
            except Exception: pass
    note.add_tag("ms_learned" if learned else "ms_unlearned"); _save_note(note)
def find_ms_notes(extra=""):
    query=f'note:"{MODEL_NAME}"'+((" "+extra) if extra else "")
    return [mw.col.get_note(nid) for nid in mw.col.find_notes(query)]
def grouped_collections():
    grouped={}
    for note in find_ms_notes(): grouped.setdefault(note["collection_id"],[]).append(note)
    for notes in grouped.values(): notes.sort(key=lambda note:int(note["line_index"] or 0))
    return grouped
def reconcile_all_progress():
    learned=unlearned=0
    for note in find_ms_notes():
        is_learned=note["learned"]=="1"; set_progress_state(note,is_learned)
        if is_learned: learned+=1
        else: unlearned+=1
    refresh_collection(); return learned,unlearned
def reorder_new_cards(collection_id=None):
    query=f"collection_id:{collection_id}" if collection_id else ""; changed=0
    for note in find_ms_notes(query):
        try: line_index=int(note["line_index"] or 0)
        except Exception: line_index=0
        for cid in note.card_ids():
            try:
                card=mw.col.get_card(cid)
                if int(getattr(card,"type",0))==0:
                    card.due=max(0,line_index-1); _save_card(card); changed+=1
            except Exception: pass
    refresh_collection(); return changed
def activate_note_first_step(note): return note.card_ids()
def cleanup_learned_step_cards(collection_id=None): return (0,0)
def initialize_note_step_gate(note,active=False): return None
def unlock_next_step_or_line(note,answered_ord=0): return ("universal",None,None,0)
