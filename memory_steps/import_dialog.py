# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Memory Steps contributors

import time
from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo
from .gen_notes import process_lines, context_for, normalize_pasted_text
from .model import ensure_model
from .anki_utils import initialize_note_step_gate

class ImportDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent or mw); self.setWindowTitle('Memory Steps - Import Text'); self.resize(940,760)
        cfg=mw.addonManager.getConfig(__name__.split('.')[0]) or {}
        self.title=QLineEdit(); self.title.setPlaceholderText('e.g., Psalm 23 / John 3 / 静夜思')
        self.deck=QComboBox(); did=mw.col.decks.id(cfg.get('default_deck','Memory Steps'))
        for deck in sorted(mw.col.decks.all_names_and_ids(), key=lambda deck: deck.name.lower()): self.deck.addItem(deck.name, deck.id)
        idx=self.deck.findData(did); self.deck.setCurrentIndex(idx if idx >= 0 else 0)
        self.mode=QComboBox(); [self.mode.addItem(name) for name in cfg.get('memorization_modes',['CJK Character Steps','Word Initial Steps','Word Outline Steps','Cloze Word Steps'])]; self.mode.setCurrentText(cfg.get('default_memorization_mode','Cloze Word Steps'))
        self.layout=QComboBox(); [self.layout.addItem(name) for name in cfg.get('layout_profiles',['Auto-detect','CJK character layout','Latin word layout','Mixed layout'])]; self.layout.setCurrentText(cfg.get('default_layout_profile','Auto-detect'))
        self.profile=QComboBox(); profiles=cfg.get('anchor_profiles',{}) or {'General / Mixed Text':[]}; [self.profile.addItem(name) for name in profiles.keys()]; self.profile.setCurrentText(cfg.get('default_anchor_profile','General / Mixed Text'))
        self.window=QSpinBox(); self.window.setRange(1,5); self.window.setValue(1)
        self.auto=QCheckBox('Automatically split numbered text into lines'); self.auto.setChecked(True)
        self.text=QTextEdit(); self.preview=QTextEdit(); self.preview.setReadOnly(True); self.preview.setMaximumHeight(150)
        form=QFormLayout(); form.addRow('Text title / collection',self.title); form.addRow('Deck',self.deck); form.addRow('Memorization mode',self.mode); form.addRow('Text layout',self.layout); form.addRow('Anchor-word profile',self.profile); form.addRow('Context window',self.window); form.addRow('',self.auto)
        split=QPushButton('Preview / Split Lines'); split.clicked.connect(self.preview_split); imp=QPushButton('Import'); imp.clicked.connect(self.import_text); cancel=QPushButton('Cancel'); cancel.clicked.connect(self.reject)
        buttons=QHBoxLayout(); buttons.addWidget(split); buttons.addStretch(1); buttons.addWidget(imp); buttons.addWidget(cancel)
        layout=QVBoxLayout(); layout.addLayout(form); layout.addWidget(QLabel('Latin blanks use width-preserving underline spans for better alignment with answer text.')); layout.addWidget(self.text); layout.addWidget(self.preview); layout.addLayout(buttons); self.setLayout(layout)
    def preview_split(self): self.preview.setPlainText(normalize_pasted_text(self.text.toPlainText()) if self.auto.isChecked() else self.text.toPlainText())
    def import_text(self):
        raw=self.text.toPlainText().strip(); title=self.title.text().strip() or 'Memorization Text'
        if not raw: showInfo('Please paste text first.'); return
        cfg=mw.addonManager.getConfig(__name__.split('.')[0]) or {}; profile=self.profile.currentText(); keywords=(cfg.get('anchor_profiles',{}) or {}).get(profile,cfg.get('keywords',[]))
        data=process_lines(raw,title,mask=cfg.get('mask','＿'),keywords=keywords,auto_split=self.auto.isChecked(),memorization_mode=self.mode.currentText(),anchor_profile=profile,layout_request=self.layout.currentText())
        model=ensure_model(mw.col); did=self.deck.currentData(); note_count=card_count=0
        fields=['collection_id','collection_title','line_index','label','answer','memorization_mode','anchor_profile','layout_profile']+[f'step_{i}' for i in range(1,13)]+[f'step_{i}_label' for i in range(1,13)]
        for item in data:
            note=mw.col.new_note(model)
            for field in fields: note[field]=str(getattr(item,field))
            note['audio']=''; front,back=context_for(data,item.line_index,self.window.value()); note['front_context']=front; note['back_context']=back; note['learned']='0'; note['id']=f'{int(time.time()*1000)}-{item.line_index}'
            note.add_tag('memory_steps'); note.add_tag('ms_unlearned'); mw.col.add_note(note,did); card_count += len(note.card_ids()); note_count += 1; initialize_note_step_gate(note,item.line_index==1)
        mw.col.reset(); showInfo(f'Import successful.\n\nLines created: {note_count}\nCards created: {card_count}\nMode: {self.mode.currentText()}\nLayout: {self.layout.currentText()}'); self.accept()
