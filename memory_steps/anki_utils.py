# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Memory Steps contributors

from aqt import mw
from .model import MODEL_NAME
FINAL_STEP_ORD=11
PROGRESS_TAGS={'ms_learned','ms_unlearned'}
ADDON_PACKAGE=__name__.split('.')[0]

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

def cleanup_enabled():
    try:
        cfg=mw.addonManager.getConfig(ADDON_PACKAGE) or {}
        return bool(cfg.get('delete_intermediate_step_cards_on_learned', True))
    except Exception:
        return True

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

def delete_cards(ids):
    ids=list(ids or [])
    if not ids: return 0
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

def intermediate_step_card_ids(note):
    by_ord=card_ids_by_ord(note)
    ids=[]
    for ord_num,cids in by_ord.items():
        if int(ord_num) < FINAL_STEP_ORD:
            ids.extend(cids)
    return ids

def delete_intermediate_step_cards(note):
    return delete_cards(intermediate_step_card_ids(note))

def set_progress_state(note, learned):
    note['learned']='1' if learned else '0'
    try:
        note.tags=[tag for tag in note.tags if tag not in PROGRESS_TAGS]
    except Exception:
        for tag in PROGRESS_TAGS:
            try: note.del_tag(tag)
            except Exception: pass
    note.add_tag('ms_learned' if learned else 'ms_unlearned')
    mw.col.update_note(note)

def initialize_note_step_gate(note,active=False):
    suspend_cards(note.card_ids())
    if active:
        unsuspend_cards(all_card_ids_for_ord(note,0),0)
        set_progress_state(note, False)

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
    set_progress_state(note, True)
    deleted=delete_intermediate_step_cards(note) if cleanup_enabled() else 0
    next_note=find_next_line(note)
    if next_note: initialize_note_step_gate(next_note,True)
    try: mw.col.reset()
    except Exception: pass
    return ('line', None, next_note, deleted)

def activate_note_first_step(note):
    initialize_note_step_gate(note,True)
    return all_card_ids_for_ord(note,0)

def reconcile_all_progress():
    return (0,0)

def cleanup_learned_step_cards(collection_id=None):
    query='learned:1'
    if collection_id:
        query += f' collection_id:{collection_id}'
    deleted=0; notes=0
    for note in find_ms_notes(query):
        count=delete_intermediate_step_cards(note)
        if count:
            deleted += count; notes += 1
    try: mw.col.reset()
    except Exception: pass
    return notes, deleted
