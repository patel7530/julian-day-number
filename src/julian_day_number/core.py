"""Core conversion logic for Gregorian-to-Julian Day Number translation."""


class InvalidGregorianDateError(ValueError):
    """Raised when a date does not correspond to a real Gregorian calendar day.

    Subclassing :class:`ValueError` lets callers catch either the specific
    error or the broader category, which is the conventional pattern for
    domain-specific validation errors in the standard library.
    """


def _is_leap(year: int) -> bool:
    """Return whether ``year`` is a leap year under Gregorian rules.

    The Gregorian rule is: every 4th year is a leap year, except centuries
    which must be divisible by 400 to count. We apply the rule proleptically
    (to all years, including negative ones for BC dates) because that is the
    single convention this library commits to.
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _days_in_month(year: int, month: int) -> int:
    """Return the number of days in ``month`` of ``year``."""
    if month == 2:
        return 29 if _is_leap(year) else 28
    # Months with 30 days: April (4), June (6), September (9), November (11).
    if month in (4, 6, 9, 11):
        return 30
    return 31


def _validate(year: int, month: int, day: int) -> None:
    """Raise :class:`InvalidGregorianDateError` if the date is not real.

    Month must be 1-12 and day must be within the valid range for that
    month and year. Years may be any integer (including zero and negative
    values for BC dates), consistent with proleptic Gregorian usage.
    """
    if isinstance(year, bool) or isinstance(month, bool) or isinstance(day, bool):
        raise InvalidGregorianDateError("year, month, and day must be integers, not bool")
    if not isinstance(year, int) or not isinstance(month, int) or not isinstance(day, int):
        raise InvalidGregorianDateError("year, month, and day must be integers")
    if month < 1 or month > 12:
        raise InvalidGregorianDateError(f"month must be in 1..12, got {month}")
    max_day = _days_in_month(year, month)
    if day < 1 or day > max_day:
        raise InvalidGregorianDateError(
            f"day must be in 1..{max_day} for year={year}, month={month}, got {day}"
        )


def gregorian_to_jdn(year: int, month: int, day: int) -> int:
    """Return the Julian Day Number for the given Gregorian calendar date.

    Parameters
    ----------
    year:
        Any integer. Negative values denote BC years under the proleptic
        Gregorian calendar; year 0 is the year 1 BC.
    month:
        Integer in the range 1 (January) through 12 (December).
    day:
        Integer day of the month, within the valid range for ``year`` and
        ``month``.

    Returns
    -------
    int
        The Julian Day Number — the whole-day count since the Julian epoch.

    Raises
    ------
    InvalidGregorianDateError
        If ``month`` is out of range, or ``day`` does not exist in the
        given month and year, or any argument is not an integer.

    Notes
    -----
    The algorithm used is the well-known integer formula derived by
    Fliegel and Van Flandern (1968). It is chosen because it is a closed
    arithmetic expression with no loops or lookup tables, which makes its
    behaviour easy to reason about and verify against published reference
    values. The formula as written applies to proleptic Gregorian dates
    with an astronomical year numbering (year 0 = 1 BC), which matches the
    convention documented at the top of this package.
    """
    _validate(year, month, day)
    # Fliegel-Van Flandtern closed-form expression. Each term is an integer
    # by construction (the divisions are floor divisions of integers), so
    # the result is an exact integer day count with no floating-point
    # rounding involved.
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    return day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
