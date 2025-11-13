"""Smoke tests for the Shadow C2 helper scripts."""

from __future__ import annotations

import importlib
import pathlib
import unittest


class QuickStartSmokeTests(unittest.TestCase):
    def test_quick_start_module_loads(self) -> None:
        module = importlib.import_module("quick_start")
        self.assertTrue(hasattr(module, "QuickStart"))

    def test_scripts_are_present(self) -> None:
        expected = [
            pathlib.Path("test_suite.py"),
            pathlib.Path("scripts/run_static_checks.py"),
        ]
        for path in expected:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), f"Required helper script missing: {path}")

    def test_demo_usage_module_imports(self) -> None:
        try:
            module = importlib.import_module("demo_usage")
        except ModuleNotFoundError as exc:  # optional dependencies
            self.skipTest(f"optional dependency missing: {exc}")
        else:
            self.assertIsInstance(getattr(module, "__doc__", None), (str, type(None)))


if __name__ == "__main__":
    unittest.main()
