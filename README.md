# Julian Day Number

Translate Gregorian calendar dates into the Julian Day Number — the continuous
day-count system used by astronomers and historians.

```python
from julian_day_number import gregorian_to_jdn

gregorian_to_jdn(2000, 1, 1)   # 2451545
gregorian_to_jdn(1970, 1, 1)   # 2440588
gregorian_to_jdn(1582, 10, 15) # 2299161 (Gregorian reform date)
```

## Why this exists

Astronomers and historians need a single, unambiguous integer to refer to a
day, regardless of which local calendar was in force. The Julian Day Number
(JDN) provides that. Computing it from a Gregorian date is a solved problem,
but the standard formula is easy to mistype and the leap-year edge cases are
easy to get wrong. This library is a tiny, dependency-free implementation that
gets them right and rejects dates that never existed.

The trade-off: only the **proleptic Gregorian calendar** is supported. That
means Gregorian rules (including the 400-year leap cycle) are applied to *all*
dates, even those that historically used the Julian calendar. This matches
ISO 8601 and most modern astronomical software, but it means pre-1582 dates
will not agree with historical records that used the Julian calendar. If you
need Julian-calendar input, this is the wrong library.

## Edge cases

- Year 0 is accepted and means 1 BC (astronomical year numbering).
- February 29 is rejected in non-leap years (e.g. 1900, 2023) and accepted in
  leap years (e.g. 2000, 2024).
- Months must be 1–12; days must be valid for the given month and year.
  Out-of-range values raise `InvalidGregorianDateError` (a `ValueError`
  subclass).
- `bool` and `float` arguments are rejected even though `bool` is technically
  an `int` subclass — passing `True` as a day is almost always a bug.

## Exports

- `gregorian_to_jdn(year, month, day) -> int`
- `InvalidGregorianDateError` (subclass of `ValueError`)
