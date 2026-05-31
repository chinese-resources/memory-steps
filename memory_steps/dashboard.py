# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Memory Steps contributors
from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo
from .anki_utils import grouped_collections,reconcile_all_progress,reorder_new_cards,set_progress_state
from .import_dialog import ImportDialog
from .recite_dialog import ReciteDialog
HELP_TEXT="""Memory Steps Universal Ladder Player

One card per line. Recall starts hard. Training alternates prompt → check full line → harder prompt → check full line. No desktop hotkeys are assigned, to avoid Anki shortcut conflicts.
"""
class Dashboard(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent or mw); reconcile_all_progress(); self.setWindowTitle("Memory Steps - Dashboard"); self.resize(1100,650); self.collections=grouped_collections(); self.combo=QComboBox(); self.table=QTableWidget(0,6); self.table.setHorizontalHeaderLabels(["#","Label","Mode","Status","Preview","Note ID"]); self.table.setColumnHidden(5,True); self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows); self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection); self.summary=QLabel()
        for cid,notes in self.collections.items(): self.combo.addItem(notes[0]["collection_title"],cid)
        self.combo.currentIndexChanged.connect(self.refresh); buttons=[]
        for label,fn in [("Import Text",self.open_import),("Preview Selected",self.preview_selected),("Reorder New Cards",self.reorder_cards),("Mark Learned",self.mark_selected_learned),("Mark Unlearned",self.mark_selected_unlearned),("Recite / Practice Text",self.open_recite),("Help",self.open_help),("Refresh",self.reload)]: btn=QPushButton(label); btn.clicked.connect(fn); buttons.append(btn)
        top=QHBoxLayout(); top.addWidget(QLabel("Collection")); top.addWidget(self.combo,1); top.addWidget(buttons[-1]); row=QHBoxLayout(); [row.addWidget(btn) for btn in buttons[:-1]]; row.addStretch(1)
        layout=QVBoxLayout(); layout.addWidget(self.summary); layout.addLayout(top); layout.addWidget(self.table); layout.addLayout(row); self.setLayout(layout); self.refresh()
    def open_help(self): showInfo(HELP_TEXT)
    def current_notes(self): return self.collections.get(self.combo.currentData(),[])
    def reload(self):
        self.collections=grouped_collections(); current=self.combo.currentData(); self.combo.blockSignals(True); self.combo.clear(); [self.combo.addItem(notes[0]["collection_title"],cid) for cid,notes in self.collections.items()]; idx=self.combo.findData(current); self.combo.setCurrentIndex(max(0,idx)); self.combo.blockSignals(False); self.refresh()
    def refresh(self):
        notes=self.current_notes(); self.table.setRowCount(len(notes)); learned=sum(1 for note in notes if note["learned"]=="1"); self.summary.setText(f"Collections: {len(self.collections)}   Lines/cards: {len(notes)}   Learned: {learned}   Remaining: {len(notes)-learned}   Architecture: Universal Ladder Player")
        for row,note in enumerate(notes):
            preview=note["answer"][:55]+"…" if len(note["answer"])>55 else note["answer"]
            for col,value in enumerate([note["line_index"],note["label"],note["memorization_mode"],"Learned" if note["learned"]=="1" else "Unlearned",preview,str(note.id)]): self.table.setItem(row,col,QTableWidgetItem(str(value)))
        self.table.resizeColumnsToContents()
    def selected_note(self):
        row=self.table.currentRow()
        if row<0 and self.table.selectedItems(): row=self.table.selectedItems()[0].row()
        if row<0: return None
        return mw.col.get_note(int(self.table.item(row,5).text()))
    def preview_selected(self):
        note=self.selected_note(); showInfo("Select a line first." if not note else f"{note['label']} · {note['memorization_mode']}\n\nRecall starts at: {note['step_12']}\n\nAnswer:\n{note['answer']}")
    def reorder_cards(self):
        cid=self.combo.currentData();
        if not cid: showInfo("No collection selected."); return
        changed=reorder_new_cards(cid); showInfo(f"Reordered {changed} new universal line cards for the selected collection."); self.reload()
    def mark_selected_learned(self):
        note=self.selected_note();
        if not note: showInfo("Select a line first."); return
        set_progress_state(note,True); self.reload()
    def mark_selected_unlearned(self):
        note=self.selected_note();
        if not note: showInfo("Select a line first."); return
        set_progress_state(note,False); self.reload()
    def open_import(self): ImportDialog(self).exec(); self.reload()
    def open_recite(self): ReciteDialog(self).exec()
def open_dashboard(): Dashboard(mw).exec()
