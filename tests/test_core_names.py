"""Check the approved name validation and presentation rules."""

import unittest

from habits import core


class NameNormalizationTests(unittest.TestCase):
    """Validate names without implementing lookup or duplicate detection."""

    def test_trims_spaces_at_both_ends(self) -> None:
        for padding in (" ", "   ", "\u00a0", "\u2003", "\u3000"):
            with self.subTest(padding=repr(padding)):
                self.assertEqual(
                    core.normalize_name(padding + "Read Python" + padding),
                    "Read Python",
                )

    def test_normalizes_canonical_unicode_to_nfc(self) -> None:
        for raw_name, expected in (
            ("  Cafe\u0301  ", "Caf\u00e9"),
            ("\u1100\u1161", "\uac00"),
        ):
            with self.subTest(raw_name=raw_name):
                self.assertEqual(core.normalize_name(raw_name), expected)

    def test_preserves_case_accents_and_inner_spaces(self) -> None:
        self.assertEqual(
            core.normalize_name("  LeEr  PYTHON y caf\u00e9  "),
            "LeEr  PYTHON y caf\u00e9",
        )

    def test_preserves_compatibility_characters(self) -> None:
        name = "Read \ufb03 \u2460 \uff21"

        self.assertEqual(core.normalize_name(name), name)

    def test_accepts_names_longer_than_eighty_characters(self) -> None:
        for length in (81, 256, 4096):
            with self.subTest(length=length):
                name = "A" * length
                self.assertEqual(core.normalize_name(name), name)

    def test_rejects_empty_and_space_only_names(self) -> None:
        for name in ("", " ", "   ", "\u00a0\u2003\u3000"):
            with self.subTest(name=repr(name)):
                with self.assertRaises(core.InvalidNameError):
                    core.normalize_name(name)

    def test_rejects_controls_and_line_breaks_even_at_edges(self) -> None:
        forbidden_characters = (
            "\t", "\n", "\r", "\v", "\f", "\x00", "\x1b",
            "\x7f", "\x85", "\u2028", "\u2029",
        )
        for character in forbidden_characters:
            for name in (
                character + "Read",
                "Read" + character,
                "Read" + character + "Python",
            ):
                with self.subTest(name=repr(name)):
                    with self.assertRaises(core.InvalidNameError):
                        core.normalize_name(name)

    def test_rejects_other_non_printable_characters(self) -> None:
        for character in ("\u200b", "\u202e", "\ufeff", "\ud800", "\ue000"):
            for name in (
                character + "Read",
                "Read" + character,
                "Read" + character + "Python",
            ):
                with self.subTest(name=repr(name)):
                    with self.assertRaises(core.InvalidNameError):
                        core.normalize_name(name)

    def test_normalizing_an_already_normalized_name_is_stable(self) -> None:
        name = core.normalize_name("  Cafe\u0301  Python  ")

        self.assertEqual(core.normalize_name(name), name)
