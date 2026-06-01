# Robust removal patch for card helper text

The previous patch did not work because `memory_steps/model.py` stores HTML inside Python string literals with escaped quotes, for example:

```python
<div class=\"keyboard-help\">...
```

This patch includes a robust script that removes both escaped and unescaped versions of:

```html
<div class="instructions">...</div>
<div class="keyboard-help">...</div>
```

## Apply

From the repository root:

```bash
python3 remove_visible_card_text.py
cp smoke_test.py scripts/smoke_test.py
python3 scripts/smoke_test.py
python3 scripts/build_release.py
```

Then commit:

```bash
git add memory_steps/model.py scripts/smoke_test.py
git commit -m "Remove helper text from ladder player card"
```
