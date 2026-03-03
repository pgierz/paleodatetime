"""Tests for PaleoTimeDelta class."""

import pytest
from paleodatetime import PaleoTimeDelta


class TestPaleoTimeDeltaInit:
    """Test PaleoTimeDelta initialization."""

    def test_default_initialization(self):
        """Test creating a zero timedelta."""
        td = PaleoTimeDelta()
        assert td.total_seconds == 0
        assert td.years == 0
        assert td.days == 0
        assert td.seconds == 0

    def test_years_only(self):
        """Test initialization with years."""
        td = PaleoTimeDelta(years=1)
        assert td.years == 1
        assert td.total_seconds == PaleoTimeDelta.SECONDS_PER_YEAR

    def test_months_only(self):
        """Test initialization with months."""
        td = PaleoTimeDelta(months=6)
        expected = 6 * PaleoTimeDelta.SECONDS_PER_MONTH
        assert td.total_seconds == expected

    def test_days_only(self):
        """Test initialization with days."""
        td = PaleoTimeDelta(days=100)
        assert td.total_seconds == 100 * PaleoTimeDelta.SECONDS_PER_DAY

    def test_time_components(self):
        """Test initialization with hours, minutes, seconds."""
        td = PaleoTimeDelta(hours=2, minutes=30, seconds=45)
        expected = 2 * 3600 + 30 * 60 + 45
        assert td.total_seconds == expected

    def test_combined_components(self):
        """Test initialization with multiple components."""
        td = PaleoTimeDelta(years=1, days=10, hours=5)
        expected = (
            PaleoTimeDelta.SECONDS_PER_YEAR
            + 10 * PaleoTimeDelta.SECONDS_PER_DAY
            + 5 * PaleoTimeDelta.SECONDS_PER_HOUR
        )
        assert td.total_seconds == expected

    def test_negative_values(self):
        """Test initialization with negative values."""
        td = PaleoTimeDelta(years=-5)
        assert td.total_seconds < 0
        assert td.years == -5


class TestPaleoTimeDeltaArithmetic:
    """Test arithmetic operations on PaleoTimeDelta."""

    def test_addition(self):
        """Test adding two timedeltas."""
        td1 = PaleoTimeDelta(years=1)
        td2 = PaleoTimeDelta(days=30)
        result = td1 + td2
        assert result.total_seconds == td1.total_seconds + td2.total_seconds

    def test_subtraction(self):
        """Test subtracting two timedeltas."""
        td1 = PaleoTimeDelta(years=2)
        td2 = PaleoTimeDelta(years=1)
        result = td1 - td2
        assert result.years == 1

    def test_multiplication_by_int(self):
        """Test multiplying timedelta by integer."""
        td = PaleoTimeDelta(years=1)
        result = td * 3
        assert result.years == 3

    def test_multiplication_by_float(self):
        """Test multiplying timedelta by float."""
        td = PaleoTimeDelta(days=10)
        result = td * 2.5
        assert result.total_seconds == int(td.total_seconds * 2.5)

    def test_rmul(self):
        """Test reverse multiplication."""
        td = PaleoTimeDelta(years=1)
        result = 3 * td
        assert result.years == 3

    def test_division(self):
        """Test dividing timedelta by scalar."""
        td = PaleoTimeDelta(years=10)
        result = td / 2
        assert result.years == 5

    def test_floor_division(self):
        """Test floor division."""
        td = PaleoTimeDelta(years=10)
        result = td // 3
        expected_seconds = td.total_seconds // 3
        assert result.total_seconds == expected_seconds

    def test_division_by_zero(self):
        """Test that division by zero raises error."""
        td = PaleoTimeDelta(years=1)
        with pytest.raises(ZeroDivisionError):
            td / 0

    def test_negation(self):
        """Test negating a timedelta."""
        td = PaleoTimeDelta(years=5)
        result = -td
        assert result.years == -5

    def test_absolute_value(self):
        """Test absolute value of timedelta."""
        td = PaleoTimeDelta(years=-5)
        result = abs(td)
        assert result.years == 5


class TestPaleoTimeDeltaComparison:
    """Test comparison operations on PaleoTimeDelta."""

    def test_equality(self):
        """Test equality comparison."""
        td1 = PaleoTimeDelta(years=1)
        td2 = PaleoTimeDelta(days=365, hours=6)  # Exactly 1 year (365.25 days)
        td3 = PaleoTimeDelta(years=1)
        # All three are equal since 365.25 days = 1 year in our constants
        assert td1 == td3
        assert td1 == td2  # 365.25 days equals 1 year
        # Test inequality with different value
        td4 = PaleoTimeDelta(years=2)
        assert td1 != td4

    def test_less_than(self):
        """Test less than comparison."""
        td1 = PaleoTimeDelta(years=1)
        td2 = PaleoTimeDelta(years=2)
        assert td1 < td2
        assert not td2 < td1

    def test_less_equal(self):
        """Test less than or equal comparison."""
        td1 = PaleoTimeDelta(years=1)
        td2 = PaleoTimeDelta(years=2)
        td3 = PaleoTimeDelta(years=1)
        assert td1 <= td2
        assert td1 <= td3

    def test_greater_than(self):
        """Test greater than comparison."""
        td1 = PaleoTimeDelta(years=2)
        td2 = PaleoTimeDelta(years=1)
        assert td1 > td2
        assert not td2 > td1

    def test_greater_equal(self):
        """Test greater than or equal comparison."""
        td1 = PaleoTimeDelta(years=2)
        td2 = PaleoTimeDelta(years=1)
        td3 = PaleoTimeDelta(years=2)
        assert td1 >= td2
        assert td1 >= td3


class TestPaleoTimeDeltaString:
    """Test string representations of PaleoTimeDelta."""

    def test_str_years_only(self):
        """Test string representation with years."""
        td = PaleoTimeDelta(years=5)
        s = str(td)
        assert "5 years" in s

    def test_str_negative(self):
        """Test string representation of negative timedelta."""
        td = PaleoTimeDelta(years=-10)
        s = str(td)
        assert s.startswith("-")

    def test_repr(self):
        """Test repr representation."""
        td = PaleoTimeDelta(years=1, days=10, seconds=30)
        r = repr(td)
        assert "PaleoTimeDelta" in r


class TestPaleoTimeDeltaMisc:
    """Test miscellaneous PaleoTimeDelta functionality."""

    def test_bool_nonzero(self):
        """Test that non-zero timedelta is truthy."""
        td = PaleoTimeDelta(years=1)
        assert bool(td) is True

    def test_bool_zero(self):
        """Test that zero timedelta is falsy."""
        td = PaleoTimeDelta()
        assert bool(td) is False

    def test_hash(self):
        """Test that timedeltas are hashable."""
        td1 = PaleoTimeDelta(years=1)
        td2 = PaleoTimeDelta(years=1)
        assert hash(td1) == hash(td2)

    def test_hash_in_set(self):
        """Test using timedeltas in sets."""
        td1 = PaleoTimeDelta(years=1)
        td2 = PaleoTimeDelta(years=1)
        td3 = PaleoTimeDelta(years=2)
        s = {td1, td2, td3}
        assert len(s) == 2  # td1 and td2 are equal
