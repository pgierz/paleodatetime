"""PaleoTimeDelta class for representing durations in geological time."""

from __future__ import annotations
from typing import Union


class PaleoTimeDelta:
    """
    Represents a duration in geological time.

    Supports years, months, days, hours, minutes, and seconds with second-level precision.
    Internally stores the duration as total seconds for accurate arithmetic.
    """

    # Constants for conversions
    SECONDS_PER_MINUTE = 60
    SECONDS_PER_HOUR = 3600
    SECONDS_PER_DAY = 86400
    SECONDS_PER_YEAR = 31557600  # 365.25 days (accounting for leap years)
    SECONDS_PER_MONTH = 2629800  # Average month length (365.25 / 12 days)

    def __init__(
        self,
        years: Union[int, float] = 0,
        months: Union[int, float] = 0,
        days: Union[int, float] = 0,
        hours: Union[int, float] = 0,
        minutes: Union[int, float] = 0,
        seconds: Union[int, float] = 0,
    ):
        """
        Initialize a PaleoTimeDelta.

        Args:
            years: Number of years
            months: Number of months
            days: Number of days
            hours: Number of hours
            minutes: Number of minutes
            seconds: Number of seconds
        """
        # Convert all components to seconds
        total = 0
        total += int(years * self.SECONDS_PER_YEAR)
        total += int(months * self.SECONDS_PER_MONTH)
        total += int(days * self.SECONDS_PER_DAY)
        total += int(hours * self.SECONDS_PER_HOUR)
        total += int(minutes * self.SECONDS_PER_MINUTE)
        total += int(seconds)

        self._total_seconds = total

    @property
    def total_seconds(self) -> int:
        """Return the total duration in seconds."""
        return self._total_seconds

    @property
    def years(self) -> int:
        """Return the years component of the duration."""
        return self._total_seconds // self.SECONDS_PER_YEAR

    @property
    def days(self) -> int:
        """Return the days component (remaining after years)."""
        remaining = abs(self._total_seconds) % self.SECONDS_PER_YEAR
        return remaining // self.SECONDS_PER_DAY

    @property
    def seconds(self) -> int:
        """Return the seconds component (remaining after days)."""
        remaining = abs(self._total_seconds) % self.SECONDS_PER_DAY
        return remaining if self._total_seconds >= 0 else -remaining

    def __repr__(self) -> str:
        """Return a string representation of the PaleoTimeDelta."""
        return f"PaleoTimeDelta(years={self.years}, days={self.days}, seconds={self.seconds})"

    def __str__(self) -> str:
        """Return a human-readable string representation."""
        parts = []

        total_abs = abs(self._total_seconds)
        years = total_abs // self.SECONDS_PER_YEAR
        remaining = total_abs % self.SECONDS_PER_YEAR
        days = remaining // self.SECONDS_PER_DAY
        remaining = remaining % self.SECONDS_PER_DAY
        hours = remaining // self.SECONDS_PER_HOUR
        remaining = remaining % self.SECONDS_PER_HOUR
        minutes = remaining // self.SECONDS_PER_MINUTE
        seconds = remaining % self.SECONDS_PER_MINUTE

        if years:
            parts.append(f"{years} year{'s' if years != 1 else ''}")
        if days:
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        if hours or minutes or seconds or not parts:
            time_parts = []
            if hours:
                time_parts.append(f"{hours:02d}")
            else:
                time_parts.append("00")
            time_parts.append(f"{minutes:02d}")
            time_parts.append(f"{seconds:02d}")
            parts.append(":".join(time_parts))

        result = ", ".join(parts)
        if self._total_seconds < 0:
            result = "-" + result

        return result

    def __add__(self, other: PaleoTimeDelta) -> PaleoTimeDelta:
        """Add two PaleoTimeDelta objects."""
        if not isinstance(other, PaleoTimeDelta):
            return NotImplemented
        result = PaleoTimeDelta()
        result._total_seconds = self._total_seconds + other._total_seconds
        return result

    def __sub__(self, other: PaleoTimeDelta) -> PaleoTimeDelta:
        """Subtract two PaleoTimeDelta objects."""
        if not isinstance(other, PaleoTimeDelta):
            return NotImplemented
        result = PaleoTimeDelta()
        result._total_seconds = self._total_seconds - other._total_seconds
        return result

    def __mul__(self, other: Union[int, float]) -> PaleoTimeDelta:
        """Multiply a PaleoTimeDelta by a scalar."""
        if not isinstance(other, (int, float)):
            return NotImplemented
        result = PaleoTimeDelta()
        result._total_seconds = int(self._total_seconds * other)
        return result

    def __rmul__(self, other: Union[int, float]) -> PaleoTimeDelta:
        """Multiply a PaleoTimeDelta by a scalar (reverse operation)."""
        return self.__mul__(other)

    def __truediv__(self, other: Union[int, float]) -> PaleoTimeDelta:
        """Divide a PaleoTimeDelta by a scalar."""
        if not isinstance(other, (int, float)):
            return NotImplemented
        if other == 0:
            raise ZeroDivisionError("Cannot divide PaleoTimeDelta by zero")
        result = PaleoTimeDelta()
        result._total_seconds = int(self._total_seconds / other)
        return result

    def __floordiv__(self, other: Union[int, float]) -> PaleoTimeDelta:
        """Floor divide a PaleoTimeDelta by a scalar."""
        if not isinstance(other, (int, float)):
            return NotImplemented
        if other == 0:
            raise ZeroDivisionError("Cannot divide PaleoTimeDelta by zero")
        result = PaleoTimeDelta()
        result._total_seconds = self._total_seconds // int(other)
        return result

    def __neg__(self) -> PaleoTimeDelta:
        """Negate a PaleoTimeDelta."""
        result = PaleoTimeDelta()
        result._total_seconds = -self._total_seconds
        return result

    def __pos__(self) -> PaleoTimeDelta:
        """Return a copy of the PaleoTimeDelta."""
        result = PaleoTimeDelta()
        result._total_seconds = self._total_seconds
        return result

    def __abs__(self) -> PaleoTimeDelta:
        """Return the absolute value of a PaleoTimeDelta."""
        result = PaleoTimeDelta()
        result._total_seconds = abs(self._total_seconds)
        return result

    def __eq__(self, other: object) -> bool:
        """Check equality of two PaleoTimeDelta objects."""
        if not isinstance(other, PaleoTimeDelta):
            return NotImplemented
        return self._total_seconds == other._total_seconds

    def __ne__(self, other: object) -> bool:
        """Check inequality of two PaleoTimeDelta objects."""
        if not isinstance(other, PaleoTimeDelta):
            return NotImplemented
        return self._total_seconds != other._total_seconds

    def __lt__(self, other: PaleoTimeDelta) -> bool:
        """Check if this PaleoTimeDelta is less than another."""
        if not isinstance(other, PaleoTimeDelta):
            return NotImplemented
        return self._total_seconds < other._total_seconds

    def __le__(self, other: PaleoTimeDelta) -> bool:
        """Check if this PaleoTimeDelta is less than or equal to another."""
        if not isinstance(other, PaleoTimeDelta):
            return NotImplemented
        return self._total_seconds <= other._total_seconds

    def __gt__(self, other: PaleoTimeDelta) -> bool:
        """Check if this PaleoTimeDelta is greater than another."""
        if not isinstance(other, PaleoTimeDelta):
            return NotImplemented
        return self._total_seconds > other._total_seconds

    def __ge__(self, other: PaleoTimeDelta) -> bool:
        """Check if this PaleoTimeDelta is greater than or equal to another."""
        if not isinstance(other, PaleoTimeDelta):
            return NotImplemented
        return self._total_seconds >= other._total_seconds

    def __bool__(self) -> bool:
        """Return True if the duration is non-zero."""
        return self._total_seconds != 0

    def __hash__(self) -> int:
        """Return hash of the PaleoTimeDelta."""
        return hash(self._total_seconds)
