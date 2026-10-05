"""Check the initial package structure and import-time boundaries."""

from pathlib import Path
import subprocess
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]

IMPORT_PROBE = """
import datetime
import importlib
import sys
from contextlib import ExitStack
from unittest.mock import patch


def forbidden(*args: object, **kwargs: object) -> None:
    raise AssertionError("Application imports must not access files or the clock")


class GuardedDate(datetime.date):
    today = classmethod(forbidden)


class GuardedDatetime(datetime.datetime):
    now = classmethod(forbidden)
    today = classmethod(forbidden)
    utcnow = classmethod(forbidden)


with ExitStack() as guards:
    if sys.argv[1] == "files":
        # Source loading remains available; application file access is blocked.
        for target in (
            "builtins.open", "io.open", "os.open", "os.mkdir", "os.makedirs",
            "os.remove", "os.unlink", "os.rename", "os.replace",
        ):
            guards.enter_context(patch(target, side_effect=forbidden))
    elif sys.argv[1] == "clock":
        guards.enter_context(patch("datetime.date", GuardedDate))
        guards.enter_context(patch("datetime.datetime", GuardedDatetime))
        for target in ("time.time", "time.time_ns", "time.localtime", "time.gmtime"):
            guards.enter_context(patch(target, side_effect=forbidden))

    for name in (
        "habits", "habits.core", "habits.storage", "habits.cli", "habits.__main__",
    ):
        importlib.import_module(name)
"""


class PackageScaffoldingTests(unittest.TestCase):
    """Import every planned module in a fresh interpreter without site packages."""

    def assert_imports_succeed(self, guard: str) -> None:
        result = subprocess.run(
            [sys.executable, "-B", "-S", "-c", IMPORT_PROBE, guard],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=15,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")

    def test_planned_modules_import_without_external_dependencies(self) -> None:
        self.assert_imports_succeed("none")

    def test_imports_do_not_access_data_files(self) -> None:
        self.assert_imports_succeed("files")

    def test_imports_do_not_read_the_clock(self) -> None:
        self.assert_imports_succeed("clock")
