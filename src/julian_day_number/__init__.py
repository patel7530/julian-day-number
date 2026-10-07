"""Julian Day Number: convert Gregorian calendar dates to the continuous
day-count system used by astronomers and historians.

This package exposes a single function, :func:`gregorian_to_jdn`, which
returns the Julian Day Number for a given Gregorian calendar date.

Interpretation note
-------------------
Only the *Proleptic Gregorian calendar* is supported. That is, the rules
of the Gregorian calendar (including its leap-year rule) are applied to
all dates, including those that historically fell under the Julian
calendar. This is the convention used by ISO 8601 and by most modern
astronomical software, and it is the only convention this library
attempts to honour.

The Julian Day Number returned is the integer count of days since
noon Universal Time on Monday, 1 January 4713 BC (proleptic Julian).
Because this library deals only with whole calendar days, the noon
epoch is not directly relevant to the integer result.
"""

from .core import gregorian_to_jdn, InvalidGregorianDateError

__all__ = ["gregorian_to_jdn", "InvalidGregorianDateError"]
