# Remove hotkey text patch

This patch removes the visible card text:

> No desktop hotkeys are assigned, to avoid conflicts with Anki shortcuts.

Recommended apply method from repo root:

```bash
python3 remove_hotkey_text.py
python3 scripts/smoke_test.py
python3 scripts/build_release.py
```

Then commit:

```bash
git add memory_steps/model.py
git commit -m "Remove hotkey note from ladder player card"
```

The `.patch` file is also included if you prefer to apply it manually.
