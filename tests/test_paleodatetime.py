"""Tests for PaleoDateTime class."""

import pytest
from paleodatetime import PaleoDateTime, PaleoTimeDelta
from paleodatetime.exceptions import PaleoDateTimeValueError, PaleoDateTimeFormatError


class TestPaleoDateTimeInit:
    """Test PaleoDateTime initialization."""

    def test_simple_date(self):
        """Test creating a simple date."""
        dt = PaleoDateTime(2024, 1, 15)
        assert dt.year == 2024
        assert dt.month == 1
        assert dt.day == 15
        assert dt.hour == 0
        assert dt.minute == 0
        assert dt.second == 0

    def test_full_datetime(self):
        """Test creating a full datetime."""
        dt = PaleoDateTime(2024, 3, 15, 14, 30, 45)
        assert dt.year == 2024
        assert dt.month == 3
        assert dt.day == 15
        assert dt.hour == 14
        assert dt.minute == 30
        assert dt.second == 45

    def test_negative_year(self):
        """Test creating a date with negative year (BCE)."""
        dt = PaleoDateTime(-65_000_000, 1, 1)
        assert dt.year == -65_000_000
        assert dt.month == 1
        assert dt.day == 1

    def test_invalid_month(self):
        """Test that invalid month raises error."""
        with pytest.raises(PaleoDateTimeValueError):
            PaleoDateTime(2024, 13, 1)
        with pytest.raises(PaleoDateTimeValueError):
            PaleoDateTime(2024, 0, 1)

    def test_invalid_day(self):
        """Test that invalid day raises error."""
        with pytest.raises(PaleoDateTimeValueError):
            PaleoDateTime(2024, 1, 32)
        with pytest.raises(PaleoDateTimeValueError):
            PaleoDateTime(2024, 2, 30)  # February doesn't have 30 days

    def test_invalid_hour(self):
        """Test that invalid hour raises error."""
        with pytest.raises(PaleoDateTimeValueError):
            PaleoDateTime(2024, 1, 1, 24)
        with pytest.raises(PaleoDateTimeValueError):
            PaleoDateTime(2024, 1, 1, -1)

    def test_invalid_minute(self):
        """Test that invalid minute raises error."""
        with pytest.raises(PaleoDateTimeValueError):
            PaleoDateTime(2024, 1, 1, 0, 60)

    def test_invalid_second(self):
        """Test that invalid second raises error."""
        with pytest.raises(PaleoDateTimeValueError):
            PaleoDateTime(2024, 1, 1, 0, 0, 60)

    def test_leap_year_feb_29(self):
        """Test that Feb 29 is valid in leap year."""
        dt = PaleoDateTime(2024, 2, 29)  # 2024 is a leap year
        assert dt.day == 29

    def test_non_leap_year_feb_29(self):
        """Test that Feb 29 is invalid in non-leap year."""
        with pytest.raises(PaleoDateTimeValueError):
            PaleoDateTime(2023, 2, 29)  # 2023 is not a leap year


class TestPaleoDateTimeLeapYear:
    """Test leap year calculations."""

    def test_regular_leap_year(self):
        """Test regular leap year (divisible by 4)."""
        assert PaleoDateTime._is_leap_year(2024) is True
        assert PaleoDateTime._is_leap_year(2020) is True

    def test_non_leap_year(self):
        """Test non-leap year."""
        assert PaleoDateTime._is_leap_year(2023) is False
        assert PaleoDateTime._is_leap_year(2022) is False

    def test_century_not_leap(self):
        """Test century years not divisible by 400."""
        assert PaleoDateTime._is_leap_year(1900) is False
        assert PaleoDateTime._is_leap_year(2100) is False

    def test_century_leap(self):
        """Test century years divisible by 400."""
        assert PaleoDateTime._is_leap_year(2000) is True
        assert PaleoDateTime._is_leap_year(2400) is True

    def test_negative_year_leap(self):
        """Test leap year calculation for BCE dates using astronomical year numbering."""
        # Year 0 is 1 BCE, which is a leap year (0 % 4 = 0)
        assert PaleoDateTime._is_leap_year(0) is True
        # Year -1 is 2 BCE, not a leap year (-1 % 4 = 3 in Python)
        assert PaleoDateTime._is_leap_year(-1) is False
        # Year -4 is a leap year (-4 % 4 = 0 in Python)
        assert PaleoDateTime._is_leap_year(-4) is True
        # Year -5 is not a leap year (-5 % 4 = 3 in Python)
        assert PaleoDateTime._is_leap_year(-5) is False
        # Year -8 is a leap year (-8 % 4 = 0)
        assert PaleoDateTime._is_leap_year(-8) is True
        # Year -400 is a leap year (-400 % 400 = 0)
        assert PaleoDateTime._is_leap_year(-400) is True
        # Year -100 is not a leap year (-100 % 100 = 0, but not % 400)
        assert PaleoDateTime._is_leap_year(-100) is False


class TestPaleoDateTimeFormatting:
    """Test formatting and parsing."""

    def test_isoformat_positive_year(self):
        """Test ISO format for positive years."""
        dt = PaleoDateTime(2024, 3, 15, 14, 30, 45)
        assert dt.isoformat() == "2024-03-15T14:30:45"

    def test_isoformat_negative_year(self):
        """Test ISO format for negative years."""
        dt = PaleoDateTime(-65_000_000, 1, 1, 0, 0, 0)
        iso = dt.isoformat()
        assert iso.startswith("-065000000-01-01")

    def test_isoformat_custom_separator(self):
        """Test ISO format with custom separator."""
        dt = PaleoDateTime(2024, 3, 15, 14, 30, 45)
        assert dt.isoformat(sep=" ") == "2024-03-15 14:30:45"

    def test_fromisoformat_positive_year(self):
        """Test parsing ISO format with positive year."""
        dt = PaleoDateTime.fromisoformat("2024-03-15T14:30:45")
        assert dt.year == 2024
        assert dt.month == 3
        assert dt.day == 15
        assert dt.hour == 14
        assert dt.minute == 30
        assert dt.second == 45

    def test_fromisoformat_negative_year(self):
        """Test parsing ISO format with negative year."""
        dt = PaleoDateTime.fromisoformat("-065000000-01-01T00:00:00")
        assert dt.year == -65_000_000
        assert dt.month == 1
        assert dt.day == 1

    def test_fromisoformat_space_separator(self):
        """Test parsing ISO format with space separator."""
        dt = PaleoDateTime.fromisoformat("2024-03-15 14:30:45")
        assert dt.year == 2024

    def test_fromisoformat_invalid(self):
        """Test that invalid format raises error."""
        with pytest.raises(PaleoDateTimeFormatError):
            PaleoDateTime.fromisoformat("invalid")
        # Invalid month value will raise PaleoDateTimeValueError (not format error)
        with pytest.raises(PaleoDateTimeValueError):
            PaleoDateTime.fromisoformat("2024-13-01T00:00:00")

    def test_roundtrip(self):
        """Test that formatting and parsing roundtrip correctly."""
        dt1 = PaleoDateTime(-252_000_000, 6, 15, 12, 30, 45)
        iso = dt1.isoformat()
        dt2 = PaleoDateTime.fromisoformat(iso)
        assert dt1 == dt2

    def test_str(self):
        """Test string representation."""
        dt = PaleoDateTime(2024, 3, 15, 14, 30, 45)
        assert str(dt) == "2024-03-15T14:30:45"

    def test_repr(self):
        """Test repr representation."""
        dt = PaleoDateTime(2024, 3, 15, 14, 30, 45)
        r = repr(dt)
        assert "PaleoDateTime" in r
        assert "2024" in r


class TestPaleoDateTimeArithmetic:
    """Test arithmetic operations."""

    def test_add_timedelta_days(self):
        """Test adding days via timedelta."""
        dt = PaleoDateTime(2024, 1, 1)
        td = PaleoTimeDelta(days=10)
        result = dt + td
        assert result.day > dt.day

    def test_add_timedelta_years(self):
        """Test adding years via timedelta."""
        dt = PaleoDateTime(2024, 1, 1)
        td = PaleoTimeDelta(years=1)
        result = dt + td
        assert result.year == 2025

    def test_subtract_timedelta(self):
        """Test subtracting timedelta."""
        dt = PaleoDateTime(2024, 1, 15)
        td = PaleoTimeDelta(days=10)
        result = dt - td
        assert result.day < dt.day

    def test_subtract_datetime(self):
        """Test subtracting two datetimes."""
        dt1 = PaleoDateTime(2024, 1, 15)
        dt2 = PaleoDateTime(2024, 1, 1)
        diff = dt1 - dt2
        assert isinstance(diff, PaleoTimeDelta)
        assert diff.total_seconds > 0

    def test_geological_time_arithmetic(self):
        """Test arithmetic with geological timescales."""
        # K-Pg extinction event (65 Ma)
        kt = PaleoDateTime(-65_000_000, 1, 1)
        # Add 1 million years
        future = kt + PaleoTimeDelta(years=1_000_000)
        assert future.year == -64_000_000

    def test_negative_year_arithmetic(self):
        """Test arithmetic crossing year 0."""
        dt = PaleoDateTime(-10, 1, 1)
        td = PaleoTimeDelta(years=20)
        result = dt + td
        assert result.year == 10


class TestPaleoDateTimeComparison:
    """Test comparison operations."""

    def test_equality(self):
        """Test equality comparison."""
        dt1 = PaleoDateTime(2024, 1, 1, 12, 0, 0)
        dt2 = PaleoDateTime(2024, 1, 1, 12, 0, 0)
        dt3 = PaleoDateTime(2024, 1, 1, 12, 0, 1)
        assert dt1 == dt2
        assert dt1 != dt3

    def test_less_than(self):
        """Test less than comparison."""
        dt1 = PaleoDateTime(2024, 1, 1)
        dt2 = PaleoDateTime(2024, 1, 2)
        assert dt1 < dt2
        assert not dt2 < dt1

    def test_greater_than(self):
        """Test greater than comparison."""
        dt1 = PaleoDateTime(2024, 1, 2)
        dt2 = PaleoDateTime(2024, 1, 1)
        assert dt1 > dt2
        assert not dt2 > dt1

    def test_less_equal(self):
        """Test less than or equal comparison."""
        dt1 = PaleoDateTime(2024, 1, 1)
        dt2 = PaleoDateTime(2024, 1, 2)
        dt3 = PaleoDateTime(2024, 1, 1)
        assert dt1 <= dt2
        assert dt1 <= dt3

    def test_greater_equal(self):
        """Test greater than or equal comparison."""
        dt1 = PaleoDateTime(2024, 1, 2)
        dt2 = PaleoDateTime(2024, 1, 1)
        dt3 = PaleoDateTime(2024, 1, 2)
        assert dt1 >= dt2
        assert dt1 >= dt3

    def test_geological_comparison(self):
        """Test comparison with geological dates."""
        # Permian-Triassic extinction (252 Ma)
        pt = PaleoDateTime(-252_000_000, 1, 1)
        # K-Pg extinction (65 Ma)
        kt = PaleoDateTime(-65_000_000, 1, 1)
        # PT is older (more negative, smaller)
        assert pt < kt
        assert kt > pt


class TestPaleoDateTimeReplace:
    """Test replace method."""

    def test_replace_year(self):
        """Test replacing year."""
        dt = PaleoDateTime(2024, 1, 1)
        new_dt = dt.replace(year=2025)
        assert new_dt.year == 2025
        assert new_dt.month == 1
        assert dt.year == 2024  # Original unchanged

    def test_replace_multiple(self):
        """Test replacing multiple components."""
        dt = PaleoDateTime(2024, 1, 1, 0, 0, 0)
        new_dt = dt.replace(month=6, day=15, hour=12)
        assert new_dt.month == 6
        assert new_dt.day == 15
        assert new_dt.hour == 12
        assert new_dt.year == 2024

    def test_replace_invalid(self):
        """Test that replacing with invalid value raises error."""
        dt = PaleoDateTime(2024, 1, 1)
        with pytest.raises(PaleoDateTimeValueError):
            dt.replace(month=13)


class TestPaleoDateTimeMisc:
    """Test miscellaneous functionality."""

    def test_hash(self):
        """Test that datetimes are hashable."""
        dt1 = PaleoDateTime(2024, 1, 1)
        dt2 = PaleoDateTime(2024, 1, 1)
        assert hash(dt1) == hash(dt2)

    def test_hash_in_set(self):
        """Test using datetimes in sets."""
        dt1 = PaleoDateTime(2024, 1, 1)
        dt2 = PaleoDateTime(2024, 1, 1)
        dt3 = PaleoDateTime(2024, 1, 2)
        s = {dt1, dt2, dt3}
        assert len(s) == 2  # dt1 and dt2 are equal

    def test_now(self):
        """Test that now() returns current time."""
        dt = PaleoDateTime.now()
        assert dt.year == 2026  # Current year based on context
        assert 1 <= dt.month <= 12
        assert 1 <= dt.day <= 31

    def test_fromtimestamp(self):
        """Test creating from timestamp."""
        timestamp = 1234567890  # 2009-02-13
        dt = PaleoDateTime.fromtimestamp(timestamp)
        assert dt.year == 2009
        assert dt.month == 2

    def test_timestamp(self):
        """Test converting to timestamp."""
        dt = PaleoDateTime(2009, 2, 13, 23, 31, 30)
        ts = dt.timestamp()
        # Allow for timezone differences (could be off by hours)
        assert abs(ts - 1234567890) < 86400  # Within 1 day

    def test_timestamp_out_of_range(self):
        """Test that very old dates can't be converted to timestamp."""
        dt = PaleoDateTime(-65_000_000, 1, 1)
        with pytest.raises(PaleoDateTimeValueError):
            dt.timestamp()
