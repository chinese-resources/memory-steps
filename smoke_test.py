#!/usr/bin/env python3
from __future__ import annotations
import json, py_compile, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ADDON=ROOT/'memory_steps'
def fail(m): print('FAIL:', m); sys.exit(1)
def main():
    for path in ADDON.glob('*.py'):
        py_compile.compile(str(path), doraise=True)
    manifest=json.loads((ADDON/'manifest.json').read_text())
    if manifest.get('version')!='1.0.1':
        fail('manifest version should be 1.0.1')
    model_text=(ADDON/'model.py').read_text()
    forbidden = [
        'Use the ladder player.',
        'No desktop hotkeys are assigned',
        'Desktop keys:',
        'avoid conflicts with Anki shortcuts',
        'class=\\"instructions\\"',
        'class=\\"keyboard-help\\"',
        'class="instructions"',
        'class="keyboard-help"',
    ]
    for item in forbidden:
        if item in model_text:
            fail(f'card-facing helper text remains: {item}')
    for needle in [
        '@media (max-width:640px)',
        'max-height:calc(100vh - 300px)',
        '-webkit-overflow-scrolling:touch',
        'Recall mode</span><span class="badge" id="ms-count">Step 12 / 12',
        "var mode='recall', current=11",
    ]:
        if needle not in model_text:
            fail(f'missing {needle}')
    if 'keydown' in model_text:
        fail('desktop hotkeys should not be registered')
    print('OK: Memory Steps 1.0.1 card helper text removed')
if __name__=='__main__': main()
