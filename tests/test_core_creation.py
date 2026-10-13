"""Check pure habit creation and its shared name comparison rules."""

from datetime import date
import unittest

from habits import core


class HabitCreationTests(unittest.TestCase):
    """Create habits without changing the caller's collection."""

    def test_creates_the_first_habit_without_completions(self) -> None:
        habits: list[core.Habit] = []

        result = core.create_habit(habits, "Read Python")

        self.assertIsNot(result, habits)
        self.assertEqual(result, [core.Habit("Read Python")])
        self.assertEqual(result[0].completed_dates, ())
        self.assertEqual(habits, [])

    def test_appends_after_existing_habits_and_preserves_their_data(self) -> None:
        habits = [
            core.Habit("Study Python", (date(2026, 10, 1), date(2026, 10, 2))),
            core.Habit("Read notes", (date(2026, 9, 30),)),
        ]
        original = habits.copy()

        result = core.create_habit(habits, "Analyze examples")

        self.assertIsNot(result, habits)
        self.assertEqual(habits, original)
        self.assertEqual(result[:-1], original)
        self.assertIs(result[0], habits[0])
        self.assertIs(result[1], habits[1])
        self.assertEqual(result[-1], core.Habit("Analyze examples"))

    def test_stores_the_normalized_display_name(self) -> None:
        result = core.create_habit([], "  LeEr  Cafe\u0301  ")

        self.assertEqual(result[0].name, "LeEr  Caf\u00e9")

    def test_result_and_input_collections_are_independent(self) -> None:
        habits = [core.Habit("Read Python")]

        result = core.create_habit(habits, "Study English")
        result.append(core.Habit("Review notes"))
        self.assertEqual(habits, [core.Habit("Read Python")])

        habits.append(core.Habit("Practice math"))
        self.assertEqual(
            [habit.name for habit in result],
            ["Read Python", "Study English", "Review notes"],
        )

    def test_accepts_an_immutable_input_collection(self) -> None:
        existing = core.Habit("Read Python")
        habits = (existing,)

        result = core.create_habit(habits, "Study English")

        self.assertEqual(result, [existing, core.Habit("Study English")])
        self.assertEqual(habits, (existing,))

    def test_rejects_duplicates_using_the_lookup_equivalence_rules(self) -> None:
        for stored, candidate in (
            ("Read Python", "Read Python"),
            ("Read Python", "  READ PYTHON  "),
            ("Caf\u00e9", "CAFE\u0301"),
            ("Stra\u00dfe", "STRASSE"),
            ("\u01f0", "J\u030c"),
        ):
            with self.subTest(stored=stored, candidate=candidate):
                target = core.Habit(stored, (date(2026, 10, 1),))
                habits = [core.Habit("Other habit"), target]
                original = habits.copy()
                self.assertIs(core.find_habit(habits, candidate), target)

                with self.assertRaises(core.DuplicateHabitError):
                    core.create_habit(habits, candidate)

                self.assertEqual(habits, original)
                self.assertIs(habits[1], target)
                self.assertEqual(target.completed_dates, (date(2026, 10, 1),))

    def test_allows_names_with_distinct_accents_spaces_or_character_width(self) -> None:
        for first, second in (
            ("caf\u00e9", "cafe"),
            ("Read Python", "Read  Python"),
            ("\uff21", "A"),
        ):
            with self.subTest(first=first, second=second):
                existing = core.Habit(first)
                result = core.create_habit([existing], second)

                self.assertEqual(result, [existing, core.Habit(second)])
                self.assertIs(core.find_habit(result, first), existing)
                self.assertIs(core.find_habit(result, second), result[1])

    def test_rejects_invalid_names_without_changing_the_collection(self) -> None:
        for initial in (
            [],
            [core.Habit("Read Python", (date(2026, 10, 1),))],
        ):
            for name in ("", "   ", "\tRead", "Read\n", "Read\u200b"):
                with self.subTest(initial=initial, name=repr(name)):
                    habits = initial.copy()
                    original = habits.copy()

                    with self.assertRaises(core.InvalidNameError):
                        core.create_habit(habits, name)

                    self.assertEqual(habits, original)

    def test_accepts_a_name_longer_than_eighty_characters(self) -> None:
        name = "A" * 256

        result = core.create_habit([], name)

        self.assertEqual(result[0].name, name)
