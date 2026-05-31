# Remove card instruction text patch

This patch removes the visible card text:

> Use the ladder player. Training starts by default and alternates prompt → check full line → continue to next step. On mobile, the controls stay compact and the prompt area scrolls when needed. Use Recall for normal review from the hardest cue.

Recommended apply method from repo root:

```bash
python3 remove_card_instructions.py
python3 scripts/smoke_test.py
python3 scripts/build_release.py
```

Then commit:

```bash
git add memory_steps/model.py
git commit -m "Remove ladder player instruction text from card"
```

The `.patch` file is also included if you prefer to apply it manually.
