#!/usr/bin/env python3
"""Small import-free smoke tests for release packaging."""

from __future__ import annotations

import compileall
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADDON_DIR = ROOT / "memory_steps"


def load_gen_notes():
    spec = importlib.util.spec_from_file_location("gen_notes", ADDON_DIR / "gen_notes.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    assert_true(compileall.compile_dir(str(ADDON_DIR), quiet=1), "Python syntax check failed")

    manifest = json.loads((ADDON_DIR / "manifest.json").read_text(encoding="utf-8"))
    assert_true(manifest["version"] == "0.9.7", "manifest version should be 0.9.7")

    gen_notes = load_gen_notes()
    normalized = gen_notes.normalize_pasted_text('1 "In the beginning." 2 And then.')
    assert_true(normalized.splitlines() == ['1 "In the beginning."', "2 And then."], "numbered prose split failed")
    numbers = gen_notes.normalize_pasted_text(
        "Numbers 1:5-7 NASB\n"
        "5 These then are the names of the men who shall stand with you: "
        "of the tribe of Reuben, Elizur the son of Shedeur;6 of the tribe "
        "of Simeon, Shelumiel the son of Zurishaddai;7 of the tribe of Judah, "
        "Nahshon the son of Amminadab;"
    )
    assert_true(
        numbers.splitlines() == [
            "Numbers 1:5-7 NASB",
            "5 These then are the names of the men who shall stand with you: of the tribe of Reuben, Elizur the son of Shedeur;",
            "6 of the tribe of Simeon, Shelumiel the son of Zurishaddai;",
            "7 of the tribe of Judah, Nahshon the son of Amminadab;",
        ],
        "punctuation-adjacent verse numbers should split",
    )
    cjk_numbered = gen_notes.normalize_pasted_text("1 起初，神创造天地。2 地是空虚混沌；3 神说，要有光。")
    assert_true(
        cjk_numbered.splitlines() == ["1 起初，神创造天地。", "2 地是空虚混沌；", "3 神说，要有光。"],
        "CJK punctuation-adjacent verse numbers should split",
    )
    label, content = gen_notes.parse_label_content("6起初神创造天地。", 1)
    assert_true((label, content) == ("6", "起初神创造天地。"), "labels without a following space should parse")

    lines = gen_notes.process_lines(
        "1 In the beginning God created the heaven and the earth.",
        "Genesis",
        memorization_mode="Cloze Word Steps",
        layout_request="Latin word layout",
    )
    assert_true(len(lines) == 1, "expected one generated line")
    assert_true(lines[0].layout_profile == "layout-latin", "Latin layout was not applied")
    assert_true('class="ms-blank"' in lines[0].step_2, "Cloze blanks were not generated")
    assert_true('class="ms-blank"' in lines[0].step_10, "Latin punctuation skeleton should use word blanks")
    assert_true("＿" not in lines[0].step_10, "Latin punctuation skeleton should not use character masks")
    assert_true(len([field for field in lines[0].__dataclass_fields__ if field.startswith("step_") and not field.endswith("_label")]) == 12, "expected 12 steps")

    anchor_lines = gen_notes.process_lines(
        "1 Now the Lord spoke to Moses.",
        "Numbers",
        memorization_mode="Cloze Word Steps",
        keywords=["Lord"],
        layout_request="Latin word layout",
    )
    assert_true("Lord" in anchor_lines[0].step_8, "Anchor word should stay visible")
    assert_true('class="ms-blank"' in anchor_lines[0].step_8, "Latin anchor prompt should use word blanks")
    assert_true("＿" not in anchor_lines[0].step_8, "Latin anchor prompt should not use character masks")

    print("smoke tests passed")


if __name__ == "__main__":
    main()
