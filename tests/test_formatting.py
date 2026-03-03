"""Tests for formatting utilities."""

import pytest
from paleodatetime import (
    PaleoDateTime,
    format_ma,
    format_ka,
    format_geological,
    matplotlib_ticker_formatter,
    matplotlib_ordinal_formatter,
)


class TestFormatMa:
    """Test format_ma function."""

    def test_kt_extinction(self):
        """Test formatting K-Pg extinction event."""
        kt = PaleoDateTime(-66_000_000, 1, 1)
        result = format_ma(kt)
        assert result == "66.0 Ma"

    def test_pt_extinction(self):
        """Test formatting P-T extinction event."""
        pt = PaleoDateTime(-252_000_000, 1, 1)
        result = format_ma(pt)
        assert result == "252.0 Ma"

    def test_precision(self):
        """Test different precision levels."""
        dt = PaleoDateTime(-66_500_000, 1, 1)
        assert format_ma(dt, precision=0) == "67 Ma"
        assert format_ma(dt, precision=1) == "66.5 Ma"
        assert format_ma(dt, precision=2) == "66.50 Ma"

    def test_custom_reference_year(self):
        """Test with custom reference year."""
        dt = PaleoDateTime(-66_000_000, 1, 1)
        result = format_ma(dt, reference_year=2000)
        assert result == "66.0 Ma"

    def test_method(self):
        """Test PaleoDateTime.format_ma method."""
        kt = PaleoDateTime(-66_000_000, 1, 1)
        result = kt.format_ma()
        assert result == "66.0 Ma"

    def test_method_precision(self):
        """Test method with custom precision."""
        dt = PaleoDateTime(-66_500_000, 1, 1)
        assert dt.format_ma(precision=0) == "67 Ma"
        assert dt.format_ma(precision=2) == "66.50 Ma"


class TestFormatKa:
    """Test format_ka function."""

    def test_lgm(self):
        """Test formatting Last Glacial Maximum."""
        lgm = PaleoDateTime(-20_000, 1, 1)
        result = format_ka(lgm)
        assert result == "22.0 ka"

    def test_agriculture(self):
        """Test formatting agricultural revolution."""
        agri = PaleoDateTime(-10_000, 1, 1)
        result = format_ka(agri)
        assert result == "12.0 ka"

    def test_precision(self):
        """Test different precision levels."""
        dt = PaleoDateTime(-10_500, 1, 1)
        # Years from -10,500 to 2024 = 12,524 years = 12.524 ka
        assert format_ka(dt, precision=0) == "13 ka"
        assert format_ka(dt, precision=1) == "12.5 ka"
        assert format_ka(dt, precision=2) == "12.52 ka"

    def test_method(self):
        """Test PaleoDateTime.format_ka method."""
        lgm = PaleoDateTime(-20_000, 1, 1)
        result = lgm.format_ka()
        assert result == "22.0 ka"


class TestFormatGeological:
    """Test format_geological function."""

    def test_ma_range(self):
        """Test formatting in Ma range."""
        kt = PaleoDateTime(-66_000_000, 1, 1)
        result = format_geological(kt)
        assert result == "66.0 Ma"

    def test_ka_range(self):
        """Test formatting in ka range."""
        lgm = PaleoDateTime(-20_000, 1, 1)
        result = format_geological(lgm)
        assert result == "22.0 ka"

    def test_bce_range(self):
        """Test formatting in BCE range."""
        ancient = PaleoDateTime(-500, 1, 1)
        result = format_geological(ancient)
        assert result == "501 BCE"

    def test_ce_range(self):
        """Test formatting in CE range."""
        modern = PaleoDateTime(1492, 1, 1)
        result = format_geological(modern)
        assert result == "1492 CE"

    def test_year_zero(self):
        """Test formatting year 0 (1 BCE)."""
        year_zero = PaleoDateTime(0, 1, 1)
        result = format_geological(year_zero)
        assert result == "1 BCE"

    def test_custom_thresholds(self):
        """Test with custom thresholds."""
        dt = PaleoDateTime(-100_000, 1, 1)
        # Default: should be ka
        assert "ka" in format_geological(dt)
        # Force BCE
        result = format_geological(dt, use_ka_threshold=200_000)
        assert "BCE" in result

    def test_method(self):
        """Test PaleoDateTime.format_geological method."""
        kt = PaleoDateTime(-66_000_000, 1, 1)
        result = kt.format_geological()
        assert result == "66.0 Ma"

        lgm = PaleoDateTime(-20_000, 1, 1)
        result = lgm.format_geological()
        assert result == "22.0 ka"


class TestMatplotlibTickerFormatter:
    """Test matplotlib ticker formatter."""

    def test_formatter_creation(self):
        """Test creating a formatter."""
        formatter = matplotlib_ticker_formatter()
        assert callable(formatter)

    def test_formatter_ma_values(self):
        """Test formatting Ma values."""
        formatter = matplotlib_ticker_formatter()
        result = formatter(-66_000_000, 0)
        assert "Ma" in result

    def test_formatter_ka_values(self):
        """Test formatting ka values."""
        formatter = matplotlib_ticker_formatter()
        result = formatter(-20_000, 0)
        assert "ka" in result

    def test_formatter_historical_values(self):
        """Test formatting historical values."""
        formatter = matplotlib_ticker_formatter()
        result = formatter(-500, 0)
        assert "BCE" in result
        result = formatter(1492, 0)
        assert "CE" in result

    def test_formatter_custom_precision(self):
        """Test formatter with custom precision."""
        formatter = matplotlib_ticker_formatter(precision=0)
        result = formatter(-66_500_000, 0)
        # Should round to 67 Ma
        assert "67 Ma" in result or "66 Ma" in result

    def test_formatter_invalid_value(self):
        """Test formatter with invalid value."""
        formatter = matplotlib_ticker_formatter()
        # Should not raise, should return fallback
        result = formatter(float("inf"), 0)
        assert isinstance(result, str)


class TestMatplotlibOrdinalFormatter:
    """Test matplotlib ordinal formatter."""

    def test_formatter_creation(self):
        """Test creating an ordinal formatter."""
        formatter = matplotlib_ordinal_formatter()
        assert callable(formatter)

    def test_formatter_ma_values(self):
        """Test formatting Ma values."""
        formatter = matplotlib_ordinal_formatter()
        result = formatter(66.0, 0)
        assert result == "66.0 Ma"

    def test_formatter_ka_values(self):
        """Test formatting ka values (< 1 Ma)."""
        formatter = matplotlib_ordinal_formatter()
        result = formatter(0.5, 0)
        assert "ka" in result

    def test_formatter_year_values(self):
        """Test formatting year values (< 1 ka)."""
        formatter = matplotlib_ordinal_formatter()
        result = formatter(0.0001, 0)
        assert "years" in result

    def test_formatter_descending(self):
        """Test formatter with descending=False."""
        formatter = matplotlib_ordinal_formatter(ascending=False)
        result = formatter(66.0, 0)
        assert "Ma" in result

    def test_formatter_negative_values(self):
        """Test formatter with negative values."""
        formatter = matplotlib_ordinal_formatter()
        result = formatter(-66.0, 0)
        assert "Ma" in result

    def test_formatter_invalid_value(self):
        """Test formatter with invalid value."""
        formatter = matplotlib_ordinal_formatter()
        # Should not raise, should return fallback
        result = formatter(float("nan"), 0)
        assert isinstance(result, str)


class TestFormattingIntegration:
    """Test formatting in realistic scenarios."""

    def test_timeline_formatting(self):
        """Test formatting a timeline of events."""
        events = [
            PaleoDateTime(-252_000_000, 1, 1),  # P-T extinction
            PaleoDateTime(-66_000_000, 1, 1),  # K-Pg extinction
            PaleoDateTime(-10_000, 1, 1),  # Agriculture
            PaleoDateTime(-500, 1, 1),  # Ancient history
            PaleoDateTime(2024, 1, 1),  # Present
        ]

        labels = [dt.format_geological() for dt in events]
        assert labels[0] == "252.0 Ma"
        assert labels[1] == "66.0 Ma"
        assert labels[2] == "12.0 ka"
        assert labels[3] == "501 BCE"
        assert labels[4] == "2024 CE"

    def test_axis_labels(self):
        """Test generating axis labels for a plot."""
        # Simulate tick positions on an axis
        years = [-252_000_000, -66_000_000, -20_000, 0, 2024]

        formatter = matplotlib_ticker_formatter()
        labels = [formatter(y, i) for i, y in enumerate(years)]

        assert "252" in labels[0] and "Ma" in labels[0]
        assert "66" in labels[1] and "Ma" in labels[1]
        assert "ka" in labels[2]
        assert "BCE" in labels[3]
        assert "CE" in labels[4]

    def test_ordinal_axis_labels(self):
        """Test generating ordinal axis labels."""
        # Simulate Ma values on an axis (common in stratigraphic plots)
        ma_values = [252.0, 201.0, 145.0, 66.0, 23.0, 2.6, 0.0]

        formatter = matplotlib_ordinal_formatter()
        labels = [formatter(ma, i) for i, ma in enumerate(ma_values)]

        # All should be Ma or ka formatted
        for label in labels[:-1]:  # Except last (0.0)
            assert "Ma" in label or "ka" in label
