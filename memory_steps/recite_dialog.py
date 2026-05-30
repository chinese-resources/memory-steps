# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Memory Steps contributors

import html
import re
from aqt import mw
from aqt.qt import *
from .anki_utils import find_ms_notes

BLANK_RE = re.compile(r'&lt;span class=&quot;ms-blank&quot; style=&quot;--ch:(\d{1,2})&quot;&gt;&lt;/span&gt;')

def _render_field(value):
    escaped = html.escape(str(value), quote=True)
    return BLANK_RE.sub(r'<span class="ms-blank" style="--ch:\1"></span>', escaped)

class ReciteDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent or mw); self.setWindowTitle('Memory Steps - Practice Text'); self.resize(860,660); self.collections={}; self.combo=QComboBox(); self.mode=QComboBox(); self.view=QTextBrowser()
        for note in find_ms_notes(): self.collections.setdefault(note['collection_id'],[]).append(note)
        for cid,notes in self.collections.items(): notes.sort(key=lambda note:int(note['line_index'] or 0)); self.combo.addItem(notes[0]['collection_title'],cid)
        for label,field in [('Label only','label')]+[(f'Step {idx}',f'step_{idx}') for idx in range(2,13)]+[('Full text','answer')]: self.mode.addItem(label,field)
        btn=QPushButton('Render'); btn.clicked.connect(self.render); top=QHBoxLayout(); top.addWidget(self.combo); top.addWidget(self.mode); top.addWidget(btn); layout=QVBoxLayout(); layout.addLayout(top); layout.addWidget(self.view); self.setLayout(layout); self.render()
    def render(self):
        if not self.collections: self.view.setHtml('No texts imported yet.'); return
        notes=self.collections[self.combo.currentData()]; field=self.mode.currentData(); self.view.setHtml(''.join([f"<p><b>{_render_field(note['label'])} · {_render_field(note['memorization_mode'])}</b><br><span style='font-size:28px'>{_render_field(note[field])}</span></p>" for note in notes]))
def open_recite_dialog(): ReciteDialog(mw).exec()
