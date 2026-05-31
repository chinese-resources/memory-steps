# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Memory Steps contributors
import json
from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo
class SettingsDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent or mw); self.setWindowTitle("Memory Steps - Settings"); self.resize(760,640); self.package=__name__.split(".")[0]; self.cfg=mw.addonManager.getConfig(self.package) or {}
        self.default_deck=QLineEdit(self.cfg.get("default_deck","Memory Steps")); self.mask=QLineEdit(self.cfg.get("mask","＿")); self.default_mode=QComboBox(); self.modes=QTextEdit("\n".join(self.cfg.get("memorization_modes",["CJK Character Steps","Word Initial Steps","Word Outline Steps","Cloze Word Steps"])))
        for mode in self.cfg.get("memorization_modes",[]): self.default_mode.addItem(mode)
        self.default_mode.setCurrentText(self.cfg.get("default_memorization_mode","Cloze Word Steps")); self.default_layout=QComboBox()
        for layout in self.cfg.get("layout_profiles",["Auto-detect","CJK character layout","Latin word layout","Mixed layout"]): self.default_layout.addItem(layout)
        self.default_layout.setCurrentText(self.cfg.get("default_layout_profile","Auto-detect")); self.default_anchor=QLineEdit(self.cfg.get("default_anchor_profile","General / Mixed Text")); self.anchor_profiles=QTextEdit(json.dumps(self.cfg.get("anchor_profiles",{}),ensure_ascii=False,indent=2))
        form=QFormLayout(); form.addRow("Review architecture",QLabel("Universal Ladder Player — prompt/check training flow, mobile-safe.")); form.addRow("Default deck",self.default_deck); form.addRow("Mask character",self.mask); form.addRow("Default memorization mode",self.default_mode); form.addRow("Memorization modes, one per line",self.modes); form.addRow("Default layout",self.default_layout); form.addRow("Default anchor profile",self.default_anchor); form.addRow("Anchor profiles JSON",self.anchor_profiles)
        save=QPushButton("Save"); save.clicked.connect(self.save); cancel=QPushButton("Cancel"); cancel.clicked.connect(self.reject); buttons=QHBoxLayout(); buttons.addStretch(1); buttons.addWidget(save); buttons.addWidget(cancel); layout=QVBoxLayout(); layout.addLayout(form); layout.addLayout(buttons); self.setLayout(layout)
    def save(self):
        modes=[line.strip() for line in self.modes.toPlainText().splitlines() if line.strip()]
        try:
            profiles=json.loads(self.anchor_profiles.toPlainText() or "{}")
            if not isinstance(profiles,dict): raise ValueError("Anchor profiles must be a JSON object.")
        except Exception as exc: showInfo(f"Could not parse anchor profiles JSON.\n\n{type(exc).__name__}: {exc}"); return
        self.cfg["review_architecture"]="universal_ladder_player"; self.cfg["default_deck"]=self.default_deck.text().strip() or "Memory Steps"; self.cfg["mask"]=self.mask.text() or "＿"; self.cfg["memorization_modes"]=modes; self.cfg["default_memorization_mode"]=self.default_mode.currentText() if self.default_mode.currentText() in modes else (modes[0] if modes else "Cloze Word Steps"); self.cfg["default_layout_profile"]=self.default_layout.currentText(); self.cfg["default_anchor_profile"]=self.default_anchor.text().strip() or "General / Mixed Text"; self.cfg["anchor_profiles"]=profiles; mw.addonManager.writeConfig(self.package,self.cfg); showInfo("Memory Steps settings saved."); self.accept()
def open_settings_dialog(): SettingsDialog(mw).exec()
