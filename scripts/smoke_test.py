#!/usr/bin/env python3
from __future__ import annotations
import json, py_compile, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; ADDON=ROOT/'memory_steps'
def fail(m): print('FAIL:',m); sys.exit(1)
def main():
    for path in ADDON.glob('*.py'): py_compile.compile(str(path), doraise=True)
    manifest=json.loads((ADDON/'manifest.json').read_text())
    if manifest.get('version')!='1.0.0': fail('manifest version should be 1.0.0')
    model_text=(ADDON/'model.py').read_text()
    for needle in ["var mode='train', current=0", 'Training mode</span><span class="badge" id="ms-count">Step 1 / 12', '{{step_1_label}}', '{{step_1}}', "function train(){mode='train'; current=0"]:
        if needle not in model_text: fail(f'missing {needle}')
    if 'keydown' in model_text: fail('desktop hotkeys should not be registered')
    print('OK: Memory Steps starts in Training mode at Step 1')
if __name__=='__main__': main()
