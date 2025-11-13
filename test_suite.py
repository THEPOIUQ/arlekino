#!/usr/bin/env python3
"""Run the Shadow C2 test suite using unittest discovery."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parent
    tests_dir = project_root / "tests"

    if not tests_dir.exists():
        print("[!] Tests directory not found:", tests_dir)
        return 1

    loader = unittest.defaultTestLoader
    suite = loader.discover(str(tests_dir))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
