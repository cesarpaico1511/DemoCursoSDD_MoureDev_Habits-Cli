"""Pure habit and streak logic, independent of I/O and the clock."""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from typing import ClassVar
import unicodedata


@dataclass(frozen=True)
class Habit:
    """Store a name and immutable completion dates."""

    name: str
    completed_dates: tuple[date, ...]

    def __init__(self, name: str, completed_dates: Iterable[date] = ()) -> None:
        """Copy the supplied dates so caller mutations cannot affect this habit."""
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "completed_dates", tuple(completed_dates))


class DomainError(Exception):
    """Identify a domain failure for translation at the CLI boundary."""

    reason: ClassVar[str] = "domain_error"

    def __init__(self) -> None:
        super().__init__(self.reason)


class InvalidNameError(DomainError):
    """Indicate that a habit name does not satisfy the naming rules."""

    reason: ClassVar[str] = "invalid_name"


class DuplicateHabitError(DomainError):
    """Indicate that an equivalent habit name already exists."""

    reason: ClassVar[str] = "duplicate_habit"


class HabitNotFoundError(DomainError):
    """Indicate that no habit matches the requested name."""

    reason: ClassVar[str] = "habit_not_found"


def normalize_name(name: str) -> str:
    """Return the NFC display name, or raise InvalidNameError for invalid input."""
    # Reject controls and line separators before stripping can hide them.
    if any(
        unicodedata.category(character) in {"Cc", "Zl", "Zp"}
        for character in name
    ):
        raise InvalidNameError()

    normalized_name = unicodedata.normalize("NFC", name.strip())
    if not normalized_name or not normalized_name.isprintable():
        raise InvalidNameError()

    return normalized_name
