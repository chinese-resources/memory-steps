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
    for needle in ['Memory Steps: Universal Ladder','Universal Ladder Player','ms-player','Check full line','Back to step','Training mode']:
        if needle not in model_text: fail(f'missing {needle}')
    if 'keydown' in model_text: fail('desktop hotkeys should not be registered')
    cfg=json.loads((ADDON/'config.json').read_text())
    if cfg.get('review_architecture')!='universal_ladder_player': fail('bad architecture config')
    print('OK: Memory Steps ladder player tweak static smoke tests passed')
if __name__=='__main__': main()
