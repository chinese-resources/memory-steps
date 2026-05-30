# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Memory Steps contributors

from aqt import gui_hooks
from aqt.utils import tooltip
from .model import MODEL_NAME
from .anki_utils import unlock_next_step_or_line, card_completed_anki_learning

def _card_from_args(*args):
    for arg in args:
        if hasattr(arg,'note') and hasattr(arg,'id'):
            return arg
    return None

def _note_type_name(note):
    try:
        note_type = note.note_type()
    except Exception:
        try:
            note_type = note.model()
        except Exception:
            return ''
    return note_type.get('name','') if isinstance(note_type,dict) else ''

def _reviewer_did_answer_card(*args):
    card=_card_from_args(*args)
    if not card: return
    try:
        note=card.note()
        if _note_type_name(note) != MODEL_NAME or note['learned'] == '1': return
        if not card_completed_anki_learning(card):
            tooltip('Keep reviewing this memory step until its Anki learning steps are complete.'); return
        result = unlock_next_step_or_line(note,int(getattr(card,'ord',0)))
        status, step, next_note = result[:3]
        deleted = result[3] if len(result) > 3 else 0
        tooltip(f'Next memorization step unlocked: {step+1}/12' if status=='step' else 'Line learned: '+note['label']+(('\nDeleted learning-step cards: '+str(deleted)) if deleted else '')+(('\nNext line unlocked: '+next_note['label']) if next_note else ''))
    except Exception:
        pass

try: gui_hooks.reviewer_did_answer_card.append(_reviewer_did_answer_card)
except Exception: pass
