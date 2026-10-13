"""Check shared name comparison keys and pure habit lookup."""

from datetime import date
import unittest

from habits import core


class NameKeyTests(unittest.TestCase):
    """Use the same comparison rules for all name-based operations."""

    def test_equivalent_names_have_the_same_key(self) -> None:
        for first, second in (
            ("Leer Python", "  LEER PYTHON  "),
            ("Caf\u00e9", "CAFE\u0301"),
            ("Stra\u00dfe", "STRASSE"),
            ("\u03c3", "\u03c2"),
        ):
            with self.subTest(first=first, second=second):
                self.assertEqual(core.name_key(first), core.name_key(second))

    def test_key_is_nfc_after_case_folding(self) -> None:
        # Case folding decomposes j with caron, so the result needs NFC again.
        self.assertEqual(core.name_key("\u01f0"), "\u01f0")

    def test_accents_inner_spaces_and_character_width_remain_distinct(self) -> None:
        for first, second in (
            ("caf\u00e9", "cafe"),
            ("Leer Python", "Leer  Python"),
            ("\uff21", "A"),
        ):
            with self.subTest(first=first, second=second):
                self.assertNotEqual(core.name_key(first), core.name_key(second))

    def test_invalid_names_cannot_produce_a_key(self) -> None:
        for name in ("", "   ", "Read\t", "\nRead", "Read\u200b"):
            with self.subTest(name=repr(name)):
                with self.assertRaises(core.InvalidNameError):
                    core.name_key(name)


class HabitLookupTests(unittest.TestCase):
    """Look up existing habits without changing their data or presentation."""

    def test_finds_the_requested_habit_and_preserves_the_collection(self) -> None:
        target = core.Habit("Read Python", (date(2026, 10, 1),))
        habits = [core.Habit("Study English"), target]
        original = habits.copy()

        result = core.find_habit(habits, "  READ PYTHON  ")

        self.assertIs(result, target)
        self.assertEqual(habits, original)
        self.assertEqual(target.name, "Read Python")
        self.assertEqual(target.completed_dates, (date(2026, 10, 1),))

    def test_finds_unicode_case_and_canonical_variants(self) -> None:
        for stored, query in (
            ("Caf\u00e9", " CAFE\u0301 "),
            ("Stra\u00dfe", "STRASSE"),
            ("\u01f0", "J\u030c"),
        ):
            with self.subTest(stored=stored, query=query):
                target = core.Habit(stored)
                self.assertIs(core.find_habit([target], query), target)

    def test_keeps_accents_and_inner_spaces_distinct_during_lookup(self) -> None:
        habits = [
            core.Habit("cafe"),
            core.Habit("caf\u00e9"),
            core.Habit("Leer Python"),
            core.Habit("Leer  Python"),
        ]

        for habit in habits:
            with self.subTest(name=habit.name):
                self.assertIs(core.find_habit(habits, habit.name.upper()), habit)

    def test_missing_habit_returns_none_without_modifying_the_collection(self) -> None:
        habits = [core.Habit("Read Python")]
        original = habits.copy()

        self.assertIsNone(core.find_habit(habits, "Study English"))
        self.assertEqual(habits, original)

    def test_empty_collection_returns_none(self) -> None:
        self.assertIsNone(core.find_habit([], "Read Python"))

    def test_invalid_query_is_rejected_even_for_an_empty_collection(self) -> None:
        for habits in ([], [core.Habit("Read Python")]):
            for query in ("", "Read\t"):
                with self.subTest(habits=habits, query=repr(query)):
                    with self.assertRaises(core.InvalidNameError):
                        core.find_habit(habits, query)
