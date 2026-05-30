#!/usr/bin/env python3
"""Build deterministic Memory Steps release artifacts."""

from __future__ import annotations

import base64
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADDON_DIR = ROOT / "memory_steps"
DIST_DIR = ROOT / "dist"
FIXED_TIME = (2026, 5, 30, 0, 0, 0)
EXCLUDED_PARTS = {"__pycache__", ".git", "dist"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
EXCLUDED_NAMES = {".DS_Store"}


def version() -> str:
    manifest = json.loads((ADDON_DIR / "manifest.json").read_text(encoding="utf-8"))
    return str(manifest["version"])


def include_path(path: Path) -> bool:
    parts = set(path.relative_to(ROOT).parts)
    return not (parts & EXCLUDED_PARTS) and path.suffix not in EXCLUDED_SUFFIXES and path.name not in EXCLUDED_NAMES


def write_file_to_zip(zf: zipfile.ZipFile, source: Path, arcname: Path) -> None:
    info = zipfile.ZipInfo(str(arcname).replace("\\", "/"), FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, source.read_bytes())


def build_addon(version_id: str) -> Path:
    path = DIST_DIR / f"memory_steps_{version_id}.ankiaddon"
    with zipfile.ZipFile(path, "w") as zf:
        for source in sorted(ADDON_DIR.rglob("*")):
            if source.is_file() and include_path(source):
                write_file_to_zip(zf, source, source.relative_to(ADDON_DIR))
    return path


def build_manual_install(version_id: str) -> Path:
    path = DIST_DIR / f"memory_steps_manual_install_{version_id}.zip"
    with zipfile.ZipFile(path, "w") as zf:
        for source in sorted(ADDON_DIR.rglob("*")):
            if source.is_file() and include_path(source):
                write_file_to_zip(zf, source, source.relative_to(ROOT))
    return path


def build_source_bundle(version_id: str) -> Path:
    zip_path = DIST_DIR / f"memory_steps_source_bundle_{version_id}.zip"
    txt_path = DIST_DIR / f"memory_steps_source_bundle_{version_id}_base64.txt"
    with zipfile.ZipFile(zip_path, "w") as zf:
        for source in sorted(ROOT.rglob("*")):
            if source.is_file() and include_path(source):
                write_file_to_zip(zf, source, source.relative_to(ROOT))
    txt_path.write_text(base64.b64encode(zip_path.read_bytes()).decode("ascii") + "\n", encoding="ascii")
    return txt_path


def main() -> None:
    version_id = version()
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir()
    artifacts = [
        build_addon(version_id),
        build_manual_install(version_id),
        build_source_bundle(version_id),
    ]
    for artifact in artifacts:
        print(artifact.relative_to(ROOT))


if __name__ == "__main__":
    main()
