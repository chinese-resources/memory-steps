# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Memory Steps contributors

from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo
from .anki_utils import grouped_collections, activate_note_first_step, reconcile_all_progress
from .import_dialog import ImportDialog
from .recite_dialog import ReciteDialog
HELP_TEXT='Memory Steps v0.9.7: 12-step ladders, layout-aware formatting, dashboard mode column, and learning-step gated unlocks.'
class Dashboard(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent or mw); reconcile_all_progress(); self.setWindowTitle('Memory Steps - Dashboard'); self.resize(1100,650); self.collections=grouped_collections(); self.combo=QComboBox(); self.table=QTableWidget(0,6); self.table.setHorizontalHeaderLabels(['#','Label','Mode','Status','Preview','Note ID']); self.table.setColumnHidden(5,True); self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows); self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection); self.summary=QLabel()
        for cid,notes in self.collections.items(): self.combo.addItem(notes[0]['collection_title'],cid)
        self.combo.currentIndexChanged.connect(self.refresh)
        buttons=[]
        for label,fn in [('Import Text',self.open_import),('Preview Selected',self.preview_selected),('Activate Selected/Next',self.activate_selected),('Recite / Practice Text',self.open_recite),('Help',self.open_help),('Refresh',self.reload)]:
            btn=QPushButton(label); btn.clicked.connect(fn); buttons.append(btn)
        top=QHBoxLayout(); top.addWidget(QLabel('Collection')); top.addWidget(self.combo,1); top.addWidget(buttons[-1]); row=QHBoxLayout(); [row.addWidget(btn) for btn in buttons[:-1]]; row.addStretch(1)
        layout=QVBoxLayout(); layout.addWidget(self.summary); layout.addLayout(top); layout.addWidget(self.table); layout.addLayout(row); self.setLayout(layout); self.refresh()
    def open_help(self): showInfo(HELP_TEXT)
    def current_notes(self): return self.collections.get(self.combo.currentData(),[])
    def reload(self): self.collections=grouped_collections(); current=self.combo.currentData(); self.combo.blockSignals(True); self.combo.clear(); [self.combo.addItem(notes[0]['collection_title'],cid) for cid,notes in self.collections.items()]; idx=self.combo.findData(current); self.combo.setCurrentIndex(max(0,idx)); self.combo.blockSignals(False); self.refresh()
    def refresh(self):
        notes=self.current_notes(); self.table.setRowCount(len(notes)); learned=sum(1 for note in notes if note['learned']=='1'); self.summary.setText(f'Collections: {len(self.collections)}   Lines: {len(notes)}   Learned: {learned}   Remaining: {len(notes)-learned}')
        for row,note in enumerate(notes):
            values=[note['line_index'],note['label'],note['memorization_mode'],'Learned' if note['learned']=='1' else 'Unlearned',note['answer'][:55]+'…' if len(note['answer'])>55 else note['answer'],str(note.id)]
            for col,value in enumerate(values): self.table.setItem(row,col,QTableWidgetItem(str(value)))
        self.table.resizeColumnsToContents()
    def selected_note(self):
        row=self.table.currentRow()
        if row<0 and self.table.selectedItems(): row=self.table.selectedItems()[0].row()
        if row<0: return None
        return mw.col.get_note(int(self.table.item(row,5).text()))
    def next_unlearned_note(self):
        for note in self.current_notes():
            if note['learned']!='1': return note
    def preview_selected(self):
        note=self.selected_note(); showInfo('Select a line first.' if not note else f'{note["label"]} · {note["memorization_mode"]}\n\n{note["answer"]}')
    def activate_selected(self):
        note=self.selected_note() or self.next_unlearned_note()
        if not note: showInfo('No line to activate.'); return
        ids=activate_note_first_step(note); showInfo(f'First step activated.\n\nActivated: {note["label"]}\nMode: {note["memorization_mode"]}\nCards activated: {len(ids)}'); self.reload()
    def open_import(self): ImportDialog(self).exec(); self.reload()
    def open_recite(self): ReciteDialog(self).exec()
def open_dashboard(): Dashboard(mw).exec()
