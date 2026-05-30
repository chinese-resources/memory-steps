# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Memory Steps contributors

from aqt import mw
from .model import MODEL_NAME
FINAL_STEP_ORD=11

def _get_card(cid): return mw.col.get_card(cid)
def _card_ord(cid):
    try: return int(getattr(_get_card(cid),'ord',0))
    except Exception: return 999

def card_completed_anki_learning(card):
    try: return int(getattr(card,'type',0)) == 2 or int(getattr(card,'queue',0)) == 2
    except Exception: return False

def card_ids_by_ord(note):
    out={}
    for cid in note.card_ids(): out.setdefault(_card_ord(cid),[]).append(cid)
    return out

def all_card_ids_for_ord(note,ord_num): return card_ids_by_ord(note).get(int(ord_num),[])

def suspend_cards(ids):
    ids=list(ids or [])
    if not ids: return
    try: mw.col.sched.suspend_cards(ids)
    except Exception:
        for cid in ids:
            try:
                card=_get_card(cid); card.queue=-1; mw.col.update_card(card)
            except Exception: pass

def unsuspend_cards(ids,due=0):
    ids=list(ids or [])
    if not ids: return
    try: mw.col.sched.unsuspend_cards(ids)
    except Exception: pass
    for offset,cid in enumerate(sorted(ids,key=lambda x:(_card_ord(x),x))):
        try:
            card=_get_card(cid)
            if card.queue == -1: card.queue=0
            if getattr(card,'type',0)==0: card.due=int(due)+offset
            mw.col.update_card(card)
        except Exception: pass

def initialize_note_step_gate(note,active=False):
    suspend_cards(note.card_ids())
    if active:
        unsuspend_cards(all_card_ids_for_ord(note,0),0)
        note['learned']='0'
        try: note.del_tag('ms_learned')
        except Exception: pass
        note.add_tag('ms_unlearned'); mw.col.update_note(note)

def find_ms_notes(extra=''):
    query=f'note:"{MODEL_NAME}"'+((' '+extra) if extra else '')
    return [mw.col.get_note(nid) for nid in mw.col.find_notes(query)]

def grouped_collections():
    grouped={}
    for note in find_ms_notes(): grouped.setdefault(note['collection_id'],[]).append(note)
    for notes in grouped.values(): notes.sort(key=lambda note:int(note['line_index'] or 0))
    return grouped

def find_next_line(note):
    cid=note['collection_id']; idx=int(note['line_index'] or 0)
    for candidate in find_ms_notes(f'collection_id:{cid}'):
        if int(candidate['line_index'] or 0) == idx+1: return candidate
    return None

def unlock_next_step_or_line(note,answered_ord):
    answered_ord=int(answered_ord)
    if answered_ord < FINAL_STEP_ORD:
        suspend_cards(all_card_ids_for_ord(note,answered_ord))
        unsuspend_cards(all_card_ids_for_ord(note,answered_ord+1),0)
        try: mw.col.reset()
        except Exception: pass
        return ('step', answered_ord+1, None)
    note['learned']='1'
    try: note.del_tag('ms_unlearned')
    except Exception: pass
    note.add_tag('ms_learned'); mw.col.update_note(note)
    next_note=find_next_line(note)
    if next_note: initialize_note_step_gate(next_note,True)
    try: mw.col.reset()
    except Exception: pass
    return ('line', None, next_note)

def activate_note_first_step(note):
    initialize_note_step_gate(note,True)
    return all_card_ids_for_ord(note,0)

def reconcile_all_progress():
    return (0,0)
