#!/usr/bin/env python3
"""Run lightweight static analysis checks for Shadow C2."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


EXCLUDE_DIRS = {"__pycache__", ".git", "venv", ".venv"}


def iter_python_files(base: Path) -> list[Path]:
    files: list[Path] = []
    for path in base.rglob("*.py"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        files.append(path)
    return files


def run_py_compile(files: list[Path]) -> bool:
    if not files:
        print("[!] No Python files found for static checks")
        return True

    print("[+] Running syntax checks with py_compile...")
    compile_cmd = [sys.executable, "-m", "py_compile"] + [str(path) for path in files]
    result = subprocess.run(compile_cmd, check=False)
    if result.returncode == 0:
        print("[✓] Syntax check passed")
        return True

    print("[!] Syntax check failed")
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run static analysis checks")
    parser.parse_args(argv)

    project_root = Path(__file__).resolve().parents[1]
    python_files = iter_python_files(project_root)
    success = run_py_compile(python_files)
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
