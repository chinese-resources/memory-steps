# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Memory Steps contributors

from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo
from pathlib import Path
import json
ADDON_PACKAGE=__name__.split('.')[0]
DEFAULT_MODES=['CJK Character Steps','Word Initial Steps','Word Outline Steps','Cloze Word Steps']
DEFAULT_LAYOUTS=['Auto-detect','CJK character layout','Latin word layout','Mixed layout']
class SettingsDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent or mw); self.setWindowTitle('Memory Steps - Settings'); self.resize(900,700); self.cfg=mw.addonManager.getConfig(ADDON_PACKAGE) or {}; self.profiles={key:list(value) for key,value in self.cfg.get('anchor_profiles',{}).items()} or {'General / Mixed Text':['and','but','because']}
        self.deck=QLineEdit(self.cfg.get('default_deck','Memory Steps')); self.mask=QLineEdit(self.cfg.get('mask','＿'))
        self.mode=QComboBox(); [self.mode.addItem(name) for name in self.cfg.get('memorization_modes',DEFAULT_MODES)]; self.mode.setCurrentText(self.cfg.get('default_memorization_mode','Cloze Word Steps'))
        self.layout=QComboBox(); [self.layout.addItem(name) for name in self.cfg.get('layout_profiles',DEFAULT_LAYOUTS)]; self.layout.setCurrentText(self.cfg.get('default_layout_profile','Auto-detect'))
        self.default_profile=QComboBox(); [self.default_profile.addItem(name) for name in self.profiles.keys()]; self.default_profile.setCurrentText(self.cfg.get('default_anchor_profile','General / Mixed Text'))
        self.list=QListWidget(); self.editor=QTextEdit(); self.loading=False; [self.list.addItem(name) for name in self.profiles.keys()]; self.list.currentTextChanged.connect(self.load); self.editor.textChanged.connect(self.changed)
        if self.list.count(): self.list.setCurrentRow(0)
        form=QFormLayout(); form.addRow('Default deck',self.deck); form.addRow('Mask',self.mask); form.addRow('Default mode',self.mode); form.addRow('Default layout',self.layout); form.addRow('Default anchor profile',self.default_profile)
        buttons=QHBoxLayout()
        for name,fn in [('Add',self.add),('Rename',self.rename),('Delete',self.delete),('Export Profiles',self.export_profiles),('Import Profiles',self.import_profiles)]:
            btn=QPushButton(name); btn.clicked.connect(fn); buttons.addWidget(btn)
        save=QPushButton('Save'); save.clicked.connect(self.save); cancel=QPushButton('Cancel'); cancel.clicked.connect(self.reject); bottom=QHBoxLayout(); bottom.addStretch(1); bottom.addWidget(save); bottom.addWidget(cancel)
        body=QHBoxLayout(); body.addWidget(self.list,1); body.addWidget(self.editor,3); layout=QVBoxLayout(); layout.addLayout(form); layout.addWidget(QLabel('Anchor words: one word or phrase per line')); layout.addLayout(body); layout.addLayout(buttons); layout.addLayout(bottom); self.setLayout(layout)
    def current_profile(self): return self.list.currentItem().text() if self.list.currentItem() else None
    def load(self,name): self.loading=True; self.editor.setPlainText('\n'.join(self.profiles.get(name,[]))); self.loading=False
    def refresh_profile_lists(self,selected=None):
        selected=selected or self.current_profile() or self.default_profile.currentText()
        self.list.clear(); self.default_profile.clear()
        for name in self.profiles.keys():
            self.list.addItem(name); self.default_profile.addItem(name)
        idx=self.list.findItems(selected,Qt.MatchFlag.MatchExactly)
        if idx: self.list.setCurrentItem(idx[0])
        combo_idx=self.default_profile.findText(selected)
        self.default_profile.setCurrentIndex(combo_idx if combo_idx >= 0 else 0)
    def changed(self):
        if not self.loading and self.current_profile(): self.profiles[self.current_profile()]=[line.strip() for line in self.editor.toPlainText().splitlines() if line.strip()]
    def add(self):
        name,ok=QInputDialog.getText(self,'Add Profile','Name:'); name=name.strip()
        if ok and name and name not in self.profiles: self.profiles[name]=[]; self.refresh_profile_lists(name)
    def rename(self):
        old=self.current_profile(); name,ok=QInputDialog.getText(self,'Rename Profile','Name:',text=old or ''); name=name.strip()
        if ok and old and name and name not in self.profiles: self.profiles[name]=self.profiles.pop(old); self.refresh_profile_lists(name)
    def delete(self):
        old=self.current_profile()
        if old and len(self.profiles)>1: self.profiles.pop(old,None); self.refresh_profile_lists()
    def export_profiles(self):
        self.changed(); path,_=QFileDialog.getSaveFileName(self,'Export Anchor Profiles','memory_steps_anchor_profiles.json','JSON files (*.json)')
        if path: Path(path).write_text(json.dumps({'format':'Memory Steps Anchor Profiles','version':1,'anchor_profiles':self.profiles,'default_anchor_profile':self.default_profile.currentText()},ensure_ascii=False,indent=2),encoding='utf-8'); showInfo('Exported profiles.\n\n'+path)
    def import_profiles(self):
        path,_=QFileDialog.getOpenFileName(self,'Import Anchor Profiles','','JSON files (*.json)')
        if not path: return
        data=json.loads(Path(path).read_text(encoding='utf-8')); profiles=data.get('anchor_profiles',{})
        if not isinstance(profiles,dict): showInfo('No anchor_profiles object found.'); return
        self.changed()
        for key,value in profiles.items(): self.profiles[str(key)]=[str(item).strip() for item in (value if isinstance(value,list) else str(value).splitlines()) if str(item).strip()]
        self.refresh_profile_lists(data.get('default_anchor_profile')); showInfo('Imported profiles. Click Save to keep changes.')
    def save(self):
        self.changed(); self.cfg['default_deck']=self.deck.text().strip() or 'Memory Steps'; self.cfg['mask']=self.mask.text() or '＿'; self.cfg['memorization_modes']=DEFAULT_MODES; self.cfg['layout_profiles']=DEFAULT_LAYOUTS; self.cfg['default_memorization_mode']=self.mode.currentText(); self.cfg['default_layout_profile']=self.layout.currentText(); self.cfg['default_anchor_profile']=self.default_profile.currentText(); self.cfg['anchor_profiles']=self.profiles; mw.addonManager.writeConfig(ADDON_PACKAGE,self.cfg); showInfo('Settings saved.'); self.accept()
def open_settings_dialog(): SettingsDialog(mw).exec()
