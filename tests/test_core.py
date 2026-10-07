import unittest

from julian_day_number import gregorian_to_jdn, InvalidGregorianDateError


class TestGregorianToJdn(unittest.TestCase):

    def test_known_reference_dates(self):
        # JDN 0 corresponds to 1 January 4713 BC (proleptic Julian), which is
        # 24 November 4714 BC in the proleptic Gregorian calendar.
        self.assertEqual(gregorian_to_jdn(-4713, 11, 24), 0)
        # The Gregorian calendar reform date under proleptic extension.
        self.assertEqual(gregorian_to_jdn(1582, 10, 15), 2299161)
        # A widely cited reference: JDN 2451545 is 1 January 2000.
        self.assertEqual(gregorian_to_jdn(2000, 1, 1), 2451545)
        # JDN 2440588 is the Unix epoch date, 1 January 1970.
        self.assertEqual(gregorian_to_jdn(1970, 1, 1), 2440588)

    def test_returns_python_int(self):
        result = gregorian_to_jdn(2000, 1, 1)
        self.assertIsInstance(result, int)
        self.assertFalse(isinstance(result, bool))

    def test_month_boundaries(self):
        # Last day of a 31-day month versus first day of the next.
        self.assertEqual(gregorian_to_jdn(2023, 1, 31), gregorian_to_jdn(2023, 2, 1) - 1)
        # Last day of a 30-day month.
        self.assertEqual(gregorian_to_jdn(2023, 4, 30), gregorian_to_jdn(2023, 5, 1) - 1)

    def test_february_non_leap(self):
        # 2023 is not a leap year: February has 28 days.
        self.assertEqual(gregorian_to_jdn(2023, 2, 28), gregorian_to_jdn(2023, 3, 1) - 1)

    def test_february_leap_divisible_by_4(self):
        # 2024 is divisible by 4 and not a century: February has 29 days.
        self.assertEqual(gregorian_to_jdn(2024, 2, 29), gregorian_to_jdn(2024, 3, 1) - 1)

    def test_century_not_leap(self):
        # 1900 is divisible by 100 but not 400: not a leap year.
        self.assertEqual(gregorian_to_jdn(1900, 2, 28), gregorian_to_jdn(1900, 3, 1) - 1)

    def test_quadricentennial_is_leap(self):
        # 2000 is divisible by 400: a leap year.
        self.assertEqual(gregorian_to_jdn(2000, 2, 29), gregorian_to_jdn(2000, 3, 1) - 1)

    def test_year_zero_supported(self):
        # Astronomical year numbering: year 0 = 1 BC. The algorithm handles
        # this without special casing; we check the result is an integer and
        # that consecutive days are contiguous.
        self.assertEqual(gregorian_to_jdn(0, 1, 1) + 1, gregorian_to_jdn(0, 1, 2))

    def test_invalid_month_zero(self):
        with self.assertRaises(InvalidGregorianDateError):
            gregorian_to_jdn(2023, 0, 15)

    def test_invalid_month_thirteen(self):
        with self.assertRaises(InvalidGregorianDateError):
            gregorian_to_jdn(2023, 13, 15)

    def test_invalid_day_zero(self):
        with self.assertRaises(InvalidGregorianDateError):
            gregorian_to_jdn(2023, 6, 0)

    def test_invalid_day_overflow_non_leap(self):
        with self.assertRaises(InvalidGregorianDateError):
            gregorian_to_jdn(2023, 2, 29)

    def test_invalid_day_overflow_leap(self):
        with self.assertRaises(InvalidGregorianDateError):
            gregorian_to_jdn(2024, 2, 30)

    def test_rejects_bool_arguments(self):
        # bool is a subclass of int in Python; a date of ``True`` is almost
        # certainly a caller bug, so we reject it.
        with self.assertRaises(InvalidGregorianDateError):
            gregorian_to_jdn(2023, 1, True)
        with self.assertRaises(InvalidGregorianDateError):
            gregorian_to_jdn(2023, True, 1)
        with self.assertRaises(InvalidGregorianDateError):
            gregorian_to_jdn(True, 1, 1)

    def test_rejects_float_arguments(self):
        with self.assertRaises(InvalidGregorianDateError):
            gregorian_to_jdn(2023, 1, 1.0)
        with self.assertRaises(InvalidGregorianDateError):
            gregorian_to_jdn(2023.0, 1, 1)

    def test_error_is_value_error_subclass(self):
        try:
            gregorian_to_jdn(2023, 13, 1)
        except ValueError:
            pass
        else:
            self.fail("expected a ValueError subclass to be raised")


if __name__ == "__main__":
    unittest.main()
