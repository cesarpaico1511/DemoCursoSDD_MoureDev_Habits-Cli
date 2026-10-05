"""Check immutable habit data and identifiable domain errors."""

from datetime import date
import unittest

from habits import core


class HabitModelTests(unittest.TestCase):
    """Keep habit data independent of changes made by callers."""

    def test_new_habit_has_a_name_and_no_completed_dates(self) -> None:
        habit = core.Habit("Study Python")

        self.assertEqual(habit.name, "Study Python")
        self.assertEqual(habit.completed_dates, ())

    def test_habit_preserves_explicit_calendar_dates(self) -> None:
        dates = (date(2026, 10, 1), date(2026, 10, 2))

        habit = core.Habit("Study Python", dates)

        self.assertEqual(habit.completed_dates, dates)

    def test_habit_copies_dates_from_a_mutable_input(self) -> None:
        dates = [date(2026, 10, 1)]
        habit = core.Habit("Study Python", dates)
        self.assertEqual(dates, [date(2026, 10, 1)])

        dates.append(date(2026, 10, 2))
        dates[0] = date(2026, 10, 3)

        self.assertEqual(habit.completed_dates, (date(2026, 10, 1),))

    def test_habit_fields_cannot_be_reassigned(self) -> None:
        habit = core.Habit("Study Python", (date(2026, 10, 1),))

        for field, value in (
            ("name", "Study English"),
            ("completed_dates", (date(2026, 10, 2),)),
        ):
            with self.subTest(field=field):
                with self.assertRaises(AttributeError):
                    setattr(habit, field, value)

        self.assertEqual(habit.name, "Study Python")
        self.assertEqual(habit.completed_dates, (date(2026, 10, 1),))

    def test_completed_dates_cannot_be_modified_in_place(self) -> None:
        habit = core.Habit("Study Python", (date(2026, 10, 1),))

        with self.assertRaises(TypeError):
            habit.completed_dates[0] = date(2026, 10, 2)

        self.assertEqual(habit.completed_dates, (date(2026, 10, 1),))


class DomainErrorTests(unittest.TestCase):
    """Expose separate failure reasons for translation by the CLI."""

    def test_domain_errors_have_distinct_types_and_english_reasons(self) -> None:
        cases = (
            (core.InvalidNameError, "invalid_name"),
            (core.DuplicateHabitError, "duplicate_habit"),
            (core.HabitNotFoundError, "habit_not_found"),
        )
        self.assertEqual(len({error_type for error_type, _ in cases}), 3)

        for error_type, reason in cases:
            with self.subTest(reason=reason):
                with self.assertRaises(core.DomainError) as raised:
                    raise error_type()

                self.assertIs(type(raised.exception), error_type)
                self.assertEqual(raised.exception.reason, reason)
                self.assertEqual(str(raised.exception), reason)
