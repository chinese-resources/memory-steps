# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Memory Steps contributors

from aqt import mw
from aqt.qt import QAction
from aqt.utils import showInfo

def _safe(label, fn):
    try: return fn()
    except Exception as exc: showInfo(f'Memory Steps could not open {label}.\n\nError:\n{type(exc).__name__}: {exc}')

def open_dashboard_safe():
    return _safe('Dashboard', lambda: (__import__(__name__+'.dashboard', fromlist=['open_dashboard']).open_dashboard()))

def open_import_dialog_safe():
    def run():
        if mw.col is None:
            showInfo('Please open a collection first.'); return
        from .model import ensure_model
        from .import_dialog import ImportDialog
        ensure_model(mw.col); ImportDialog(mw).exec()
    return _safe('Import Text', run)

def open_recite_dialog_safe():
    return _safe('Practice Text', lambda: (__import__(__name__+'.recite_dialog', fromlist=['open_recite_dialog']).open_recite_dialog()))

def open_settings_dialog_safe():
    return _safe('Settings', lambda: (__import__(__name__+'.settings_dialog', fromlist=['open_settings_dialog']).open_settings_dialog()))

def setup_menu():
    menu=mw.form.menuTools.addMenu('Memory Steps')
    for label,fn in [('Dashboard',open_dashboard_safe),('Import Text',open_import_dialog_safe),('Practice Text',open_recite_dialog_safe),('Settings',open_settings_dialog_safe)]:
        action=QAction(label,mw); action.triggered.connect(fn); menu.addAction(action)
    try: from . import auto_learn
    except Exception: pass

setup_menu()
