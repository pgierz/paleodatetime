"""PaleoDateTime class for representing dates on geological timescales."""

from __future__ import annotations
import re
import time as time_module
from typing import Optional, Union
from .timedelta import PaleoTimeDelta
from .exceptions import PaleoDateTimeValueError, PaleoDateTimeFormatError


class PaleoDateTime:
    """
    A datetime-like class for geological timescales.

    Supports dates spanning millions of years with second-level precision.
    Uses proleptic Gregorian calendar for all date calculations.
    Years can be negative (BCE) or positive (CE).
    """

    # Days in each month (non-leap year)
    DAYS_IN_MONTH = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    def __init__(
        self,
        year: int,
        month: int = 1,
        day: int = 1,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
    ):
        """
        Initialize a PaleoDateTime.

        Args:
            year: Year (can be negative for BCE dates)
            month: Month (1-12)
            day: Day of month (1-31)
            hour: Hour (0-23)
            minute: Minute (0-59)
            second: Second (0-59)

        Raises:
            PaleoDateTimeValueError: If any parameter is out of valid range
        """
        self._validate_and_set(year, month, day, hour, minute, second)

    def _validate_and_set(
        self, year: int, month: int, day: int, hour: int, minute: int, second: int
    ) -> None:
        """Validate all date/time components and set internal state."""
        # Validate month
        if not 1 <= month <= 12:
            raise PaleoDateTimeValueError(f"Month must be in 1..12, got {month}")

        # Validate hour, minute, second
        if not 0 <= hour <= 23:
            raise PaleoDateTimeValueError(f"Hour must be in 0..23, got {hour}")
        if not 0 <= minute <= 59:
            raise PaleoDateTimeValueError(f"Minute must be in 0..59, got {minute}")
        if not 0 <= second <= 59:
            raise PaleoDateTimeValueError(f"Second must be in 0..59, got {second}")

        # Validate day based on month and year
        max_day = self._days_in_month(year, month)
        if not 1 <= day <= max_day:
            raise PaleoDateTimeValueError(
                f"Day must be in 1..{max_day} for {year}-{month:02d}, got {day}"
            )

        # Set attributes
        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second

    @staticmethod
    def _is_leap_year(year: int) -> bool:
        """
        Check if a year is a leap year in the proleptic Gregorian calendar.

        Args:
            year: The year to check (can be negative, using astronomical year numbering)

        Returns:
            True if the year is a leap year, False otherwise

        Note:
            Uses astronomical year numbering where year 0 exists and equals 1 BCE.
            Year -1 = 2 BCE, -2 = 3 BCE, -3 = 4 BCE, etc.
        """
        # Gregorian leap year rules apply directly to astronomical year numbering
        if year % 400 == 0:
            return True
        if year % 100 == 0:
            return False
        if year % 4 == 0:
            return True
        return False

    @classmethod
    def _days_in_month(cls, year: int, month: int) -> int:
        """
        Get the number of days in a given month.

        Args:
            year: The year
            month: The month (1-12)

        Returns:
            Number of days in the month
        """
        if month == 2 and cls._is_leap_year(year):
            return 29
        return cls.DAYS_IN_MONTH[month]

    @property
    def year(self) -> int:
        """The year component."""
        return self._year

    @property
    def month(self) -> int:
        """The month component (1-12)."""
        return self._month

    @property
    def day(self) -> int:
        """The day component (1-31)."""
        return self._day

    @property
    def hour(self) -> int:
        """The hour component (0-23)."""
        return self._hour

    @property
    def minute(self) -> int:
        """The minute component (0-59)."""
        return self._minute

    @property
    def second(self) -> int:
        """The second component (0-59)."""
        return self._second

    @classmethod
    def now(cls) -> PaleoDateTime:
        """
        Create a PaleoDateTime representing the current date and time.

        Returns:
            PaleoDateTime object representing now
        """
        import datetime

        dt = datetime.datetime.now()
        return cls(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

    @classmethod
    def fromtimestamp(cls, timestamp: float) -> PaleoDateTime:
        """
        Create a PaleoDateTime from a Unix timestamp.

        Args:
            timestamp: Unix timestamp (seconds since 1970-01-01)

        Returns:
            PaleoDateTime object

        Note:
            Only works for dates within the Unix timestamp range
        """
        import datetime

        dt = datetime.datetime.fromtimestamp(timestamp)
        return cls(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

    def timestamp(self) -> float:
        """
        Convert to Unix timestamp.

        Returns:
            Unix timestamp (seconds since 1970-01-01)

        Raises:
            PaleoDateTimeValueError: If date is outside Unix timestamp range

        Note:
            Only works for dates within the Unix timestamp range (roughly 1970-2038)
        """
        # Only works for dates that can be represented as Unix timestamps
        if self._year < 1970 or self._year > 2038:
            raise PaleoDateTimeValueError(
                f"Cannot convert {self._year} to Unix timestamp (valid range: 1970-2038)"
            )

        import datetime

        dt = datetime.datetime(
            self._year, self._month, self._day, self._hour, self._minute, self._second
        )
        return dt.timestamp()

    def isoformat(self, sep: str = "T") -> str:
        """
        Return the date and time in ISO 8601 format.

        Args:
            sep: Separator between date and time (default 'T')

        Returns:
            ISO format string (e.g., '-65000000-01-01T00:00:00')
        """
        # Format year with sign for negative years
        if self._year < 0:
            year_str = f"{self._year:010d}"  # -XXXXXXXXX
        else:
            year_str = f"{self._year:04d}"  # YYYY or longer

        return (
            f"{year_str}-{self._month:02d}-{self._day:02d}"
            f"{sep}{self._hour:02d}:{self._minute:02d}:{self._second:02d}"
        )

    @classmethod
    def fromisoformat(cls, date_string: str) -> PaleoDateTime:
        """
        Parse a date string in ISO 8601 format.

        Args:
            date_string: ISO format string (e.g., '-65000000-01-01T00:00:00')

        Returns:
            PaleoDateTime object

        Raises:
            PaleoDateTimeFormatError: If string format is invalid
        """
        # Pattern for ISO format: YYYY-MM-DD[T| ]HH:MM:SS
        # Year can be negative and have many digits
        pattern = r"^(-?\d+)-(\d{2})-(\d{2})[\sT](\d{2}):(\d{2}):(\d{2})$"
        match = re.match(pattern, date_string)

        if not match:
            raise PaleoDateTimeFormatError(
                f"Invalid ISO format string: {date_string}. "
                "Expected format: YYYY-MM-DDTHH:MM:SS or -YYYY-MM-DDTHH:MM:SS"
            )

        year, month, day, hour, minute, second = map(int, match.groups())
        return cls(year, month, day, hour, minute, second)

    def replace(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
        minute: Optional[int] = None,
        second: Optional[int] = None,
    ) -> PaleoDateTime:
        """
        Return a new PaleoDateTime with specified fields replaced.

        Args:
            year: New year value (if None, keep current)
            month: New month value (if None, keep current)
            day: New day value (if None, keep current)
            hour: New hour value (if None, keep current)
            minute: New minute value (if None, keep current)
            second: New second value (if None, keep current)

        Returns:
            New PaleoDateTime object with replaced values
        """
        return PaleoDateTime(
            year if year is not None else self._year,
            month if month is not None else self._month,
            day if day is not None else self._day,
            hour if hour is not None else self._hour,
            minute if minute is not None else self._minute,
            second if second is not None else self._second,
        )

    def _to_comparable_value(self) -> int:
        """
        Convert the date/time to a single comparable integer value.

        This is used for comparisons and arithmetic operations.
        Returns total seconds since an arbitrary epoch.
        """
        # Calculate total seconds from year 0
        # This is approximate but consistent for comparisons

        # Start with year contribution
        total = self._year * PaleoTimeDelta.SECONDS_PER_YEAR

        # Add months (approximate)
        total += (self._month - 1) * PaleoTimeDelta.SECONDS_PER_MONTH

        # Add days (exact within month)
        total += (self._day - 1) * PaleoTimeDelta.SECONDS_PER_DAY

        # Add time components
        total += self._hour * PaleoTimeDelta.SECONDS_PER_HOUR
        total += self._minute * PaleoTimeDelta.SECONDS_PER_MINUTE
        total += self._second

        return total

    def __add__(self, other: PaleoTimeDelta) -> PaleoDateTime:
        """
        Add a PaleoTimeDelta to this PaleoDateTime.

        Args:
            other: PaleoTimeDelta to add

        Returns:
            New PaleoDateTime object
        """
        if not isinstance(other, PaleoTimeDelta):
            return NotImplemented

        # Convert current datetime to total seconds
        total_seconds = self._to_comparable_value()

        # Add the timedelta
        total_seconds += other.total_seconds

        # Convert back to datetime components
        return self._from_comparable_value(total_seconds)

    def __sub__(
        self, other: Union[PaleoDateTime, PaleoTimeDelta]
    ) -> Union[PaleoDateTime, PaleoTimeDelta]:
        """
        Subtract a PaleoTimeDelta or PaleoDateTime from this PaleoDateTime.

        Args:
            other: PaleoTimeDelta or PaleoDateTime to subtract

        Returns:
            If other is PaleoTimeDelta: new PaleoDateTime
            If other is PaleoDateTime: PaleoTimeDelta representing the difference
        """
        if isinstance(other, PaleoTimeDelta):
            # Subtract timedelta, return new datetime
            total_seconds = self._to_comparable_value()
            total_seconds -= other.total_seconds
            return self._from_comparable_value(total_seconds)
        elif isinstance(other, PaleoDateTime):
            # Subtract datetime, return timedelta
            diff = self._to_comparable_value() - other._to_comparable_value()
            result = PaleoTimeDelta()
            result._total_seconds = diff
            return result
        else:
            return NotImplemented

    @classmethod
    def _from_comparable_value(cls, total_seconds: int) -> PaleoDateTime:
        """
        Convert a total seconds value back to PaleoDateTime components.

        Args:
            total_seconds: Total seconds since arbitrary epoch

        Returns:
            PaleoDateTime object
        """
        # Extract year
        years = total_seconds // PaleoTimeDelta.SECONDS_PER_YEAR
        remaining = total_seconds % PaleoTimeDelta.SECONDS_PER_YEAR

        # Handle negative values
        if total_seconds < 0 and remaining != 0:
            years -= 1
            remaining = PaleoTimeDelta.SECONDS_PER_YEAR + remaining

        # Extract month (approximate)
        months = remaining // PaleoTimeDelta.SECONDS_PER_MONTH
        remaining = remaining % PaleoTimeDelta.SECONDS_PER_MONTH

        # Ensure month is in valid range
        month = int(months) + 1
        if month > 12:
            years += month // 12
            month = month % 12
            if month == 0:
                month = 12

        # Extract day
        days = remaining // PaleoTimeDelta.SECONDS_PER_DAY
        remaining = remaining % PaleoTimeDelta.SECONDS_PER_DAY

        day = int(days) + 1

        # Adjust for month/day overflow
        year = int(years)
        max_days = cls._days_in_month(year, month)
        while day > max_days:
            day -= max_days
            month += 1
            if month > 12:
                month = 1
                year += 1
            max_days = cls._days_in_month(year, month)

        # Extract time components
        hours = remaining // PaleoTimeDelta.SECONDS_PER_HOUR
        remaining = remaining % PaleoTimeDelta.SECONDS_PER_HOUR

        minutes = remaining // PaleoTimeDelta.SECONDS_PER_MINUTE
        seconds = remaining % PaleoTimeDelta.SECONDS_PER_MINUTE

        return cls(int(year), month, day, int(hours), int(minutes), int(seconds))

    def __eq__(self, other: object) -> bool:
        """Check equality of two PaleoDateTime objects."""
        if not isinstance(other, PaleoDateTime):
            return NotImplemented
        return (
            self._year == other._year
            and self._month == other._month
            and self._day == other._day
            and self._hour == other._hour
            and self._minute == other._minute
            and self._second == other._second
        )

    def __ne__(self, other: object) -> bool:
        """Check inequality of two PaleoDateTime objects."""
        if not isinstance(other, PaleoDateTime):
            return NotImplemented
        return not self.__eq__(other)

    def __lt__(self, other: PaleoDateTime) -> bool:
        """Check if this PaleoDateTime is less than another."""
        if not isinstance(other, PaleoDateTime):
            return NotImplemented
        return self._to_comparable_value() < other._to_comparable_value()

    def __le__(self, other: PaleoDateTime) -> bool:
        """Check if this PaleoDateTime is less than or equal to another."""
        if not isinstance(other, PaleoDateTime):
            return NotImplemented
        return self._to_comparable_value() <= other._to_comparable_value()

    def __gt__(self, other: PaleoDateTime) -> bool:
        """Check if this PaleoDateTime is greater than another."""
        if not isinstance(other, PaleoDateTime):
            return NotImplemented
        return self._to_comparable_value() > other._to_comparable_value()

    def __ge__(self, other: PaleoDateTime) -> bool:
        """Check if this PaleoDateTime is greater than or equal to another."""
        if not isinstance(other, PaleoDateTime):
            return NotImplemented
        return self._to_comparable_value() >= other._to_comparable_value()

    def __hash__(self) -> int:
        """Return hash of the PaleoDateTime."""
        return hash(
            (self._year, self._month, self._day, self._hour, self._minute, self._second)
        )

    def __repr__(self) -> str:
        """Return a string representation of the PaleoDateTime."""
        return (
            f"PaleoDateTime({self._year}, {self._month}, {self._day}, "
            f"{self._hour}, {self._minute}, {self._second})"
        )

    def __str__(self) -> str:
        """Return a human-readable string representation."""
        return self.isoformat()
