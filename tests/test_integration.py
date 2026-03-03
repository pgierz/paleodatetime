"""Integration tests for paleodatetime package."""

import pytest
from paleodatetime import PaleoDateTime, PaleoTimeDelta


class TestGeologicalTimescales:
    """Test realistic geological timescale scenarios."""

    def test_mass_extinctions(self):
        """Test working with major mass extinction events."""
        # Ordovician-Silurian (445 Ma)
        ordovician = PaleoDateTime(-445_000_000, 1, 1)

        # Late Devonian (375 Ma)
        devonian = PaleoDateTime(-375_000_000, 1, 1)

        # Permian-Triassic (252 Ma)
        permian_triassic = PaleoDateTime(-252_000_000, 1, 1)

        # Triassic-Jurassic (201 Ma)
        triassic_jurassic = PaleoDateTime(-201_000_000, 1, 1)

        # Cretaceous-Paleogene (66 Ma)
        kt = PaleoDateTime(-66_000_000, 1, 1)

        # Verify chronological order
        assert ordovician < devonian < permian_triassic < triassic_jurassic < kt

        # Calculate time between P-T and K-Pg extinctions
        time_span = kt - permian_triassic
        # Should be approximately 186 million years
        assert time_span.years > 185_000_000
        assert time_span.years < 187_000_000

    def test_human_evolution(self):
        """Test dates relevant to human evolution."""
        # Earliest Homo sapiens fossils (~300,000 years ago)
        early_sapiens = PaleoDateTime(-300_000, 1, 1)

        # Agricultural revolution (~10,000 years ago)
        agriculture = PaleoDateTime(-10_000, 1, 1)

        # Present day
        present = PaleoDateTime(2024, 1, 1)

        assert early_sapiens < agriculture < present

        # Time from agriculture to present
        # Note: from year -10,000 to 2024 is 12,024 years (astronomical year numbering)
        time_span = present - agriculture
        # Should be approximately 12,024 years
        assert 12_000 < time_span.years < 12_100

    def test_dinosaur_era(self):
        """Test dates during the age of dinosaurs."""
        # Start of Triassic (252 Ma)
        triassic_start = PaleoDateTime(-252_000_000, 1, 1)

        # Start of Jurassic (201 Ma)
        jurassic_start = PaleoDateTime(-201_000_000, 1, 1)

        # Start of Cretaceous (145 Ma)
        cretaceous_start = PaleoDateTime(-145_000_000, 1, 1)

        # End of Cretaceous / K-Pg extinction (66 Ma)
        kt_extinction = PaleoDateTime(-66_000_000, 1, 1)

        # Total duration of dinosaur dominance
        total_duration = kt_extinction - triassic_start

        # Approximately 186 million years
        assert 185_000_000 < total_duration.years < 187_000_000

        # Duration of Jurassic period
        jurassic_duration = cretaceous_start - jurassic_start
        # Approximately 56 million years
        assert 55_000_000 < jurassic_duration.years < 57_000_000

    def test_geological_periods_arithmetic(self):
        """Test arithmetic operations across geological periods."""
        # Cambrian explosion (~541 Ma)
        cambrian = PaleoDateTime(-541_000_000, 1, 1)

        # Add 100 million years
        later = cambrian + PaleoTimeDelta(years=100_000_000)
        assert later.year == -441_000_000

        # Subtract 50 million years
        earlier = cambrian - PaleoTimeDelta(years=50_000_000)
        assert earlier.year == -591_000_000


class TestLongTermCalculations:
    """Test calculations over very long time periods."""

    def test_billion_year_span(self):
        """Test working with billion-year timescales."""
        # Earth formation (~4.5 Ga)
        earth_formation = PaleoDateTime(-4_500_000_000, 1, 1)

        # Present
        present = PaleoDateTime(2024, 1, 1)

        # Calculate age of Earth
        earth_age = present - earth_formation
        assert earth_age.years > 4_500_000_000

    def test_multiple_timedelta_operations(self):
        """Test chaining multiple timedelta operations."""
        start = PaleoDateTime(-100_000_000, 1, 1)

        # Add and subtract various periods
        result = start + PaleoTimeDelta(years=10_000_000)
        result = result - PaleoTimeDelta(years=5_000_000)
        result = result + PaleoTimeDelta(years=2_000_000)

        # Net change: +7 million years
        assert result.year == -93_000_000

    def test_fractional_year_precision(self):
        """Test that second-level precision is maintained."""
        dt1 = PaleoDateTime(-65_000_000, 1, 1, 12, 30, 45)
        dt2 = PaleoDateTime(-65_000_000, 1, 1, 12, 30, 46)

        diff = dt2 - dt1
        assert diff.total_seconds == 1


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_year_zero_crossing(self):
        """Test arithmetic that crosses year 0 (BCE/CE boundary)."""
        # Note: In astronomical year numbering, year 0 exists,
        # but in historical dating, 1 BCE is followed by 1 CE
        bce = PaleoDateTime(-100, 1, 1)
        ce = PaleoDateTime(100, 1, 1)

        diff = ce - bce
        # Should be approximately 200 years
        assert 199 < diff.years < 201

    def test_same_datetime_difference(self):
        """Test difference between identical datetimes."""
        dt1 = PaleoDateTime(-252_000_000, 6, 15, 12, 30, 45)
        dt2 = PaleoDateTime(-252_000_000, 6, 15, 12, 30, 45)

        diff = dt1 - dt2
        assert diff.total_seconds == 0

    def test_very_large_numbers(self):
        """Test with very large year values."""
        # Far future date
        far_future = PaleoDateTime(1_000_000_000, 1, 1)

        # Very ancient date
        very_old = PaleoDateTime(-1_000_000_000, 1, 1)

        # Verify they can be compared
        assert very_old < far_future

        # Calculate span
        span = far_future - very_old
        assert span.years > 1_999_000_000

    def test_leap_year_in_past(self):
        """Test leap year handling in geological past."""
        # Create Feb 29 in a year that would be a leap year
        # Year -4 is a leap year (-4 % 4 = 0 in Python)
        dt = PaleoDateTime(-4, 2, 29)
        assert dt.day == 29
        # Year -8 is also a leap year
        dt2 = PaleoDateTime(-8, 2, 29)
        assert dt2.day == 29

    def test_month_day_overflow_in_arithmetic(self):
        """Test that month/day overflow is handled in arithmetic."""
        # Jan 31
        dt = PaleoDateTime(2024, 1, 31)

        # Add 1 month worth of days
        result = dt + PaleoTimeDelta(days=31)

        # Should be in March (Feb has 29 days in 2024)
        assert result.month >= 2


class TestRealWorldScenarios:
    """Test realistic usage scenarios."""

    def test_climate_cycles(self):
        """Test dating ice age cycles."""
        # Last Glacial Maximum (~20,000 years ago)
        lgm = PaleoDateTime(-20_000, 1, 1)

        # Previous interglacial (Eemian, ~115,000 years ago)
        eemian = PaleoDateTime(-115_000, 1, 1)

        # Calculate glacial cycle length
        cycle = lgm - eemian
        # Approximately 95,000 years
        assert 94_000 < cycle.years < 96_000

    def test_fossil_dating_workflow(self):
        """Test a typical fossil dating workflow."""
        # Discovery of fossil dated to 75 Ma
        fossil_date = PaleoDateTime(-75_000_000, 6, 15)

        # Compare to known extinction events
        kt_extinction = PaleoDateTime(-66_000_000, 1, 1)

        # This fossil predates the K-Pg extinction
        assert fossil_date < kt_extinction

        # By how much?
        time_before = kt_extinction - fossil_date
        # Approximately 9 million years
        assert 8_500_000 < time_before.years < 9_500_000

    def test_stratigraphy_layer_dating(self):
        """Test dating stratigraphic layers."""
        # Bottom layer (oldest)
        layer_1 = PaleoDateTime(-150_000_000, 1, 1)

        # Middle layer
        layer_2 = PaleoDateTime(-125_000_000, 1, 1)

        # Top layer (youngest)
        layer_3 = PaleoDateTime(-100_000_000, 1, 1)

        # Verify superposition principle
        assert layer_1 < layer_2 < layer_3

        # Calculate deposition rates
        time_1_to_2 = layer_2 - layer_1
        time_2_to_3 = layer_3 - layer_2

        # Both should be 25 million years
        assert time_1_to_2.years == 25_000_000
        assert time_2_to_3.years == 25_000_000

    def test_evolutionary_timeline(self):
        """Test creating an evolutionary timeline."""
        events = [
            ("Cambrian Explosion", PaleoDateTime(-541_000_000, 1, 1)),
            ("First land plants", PaleoDateTime(-470_000_000, 1, 1)),
            ("First tetrapods", PaleoDateTime(-375_000_000, 1, 1)),
            ("First dinosaurs", PaleoDateTime(-230_000_000, 1, 1)),
            ("First flowering plants", PaleoDateTime(-130_000_000, 1, 1)),
            ("First primates", PaleoDateTime(-55_000_000, 1, 1)),
        ]

        # Verify chronological order
        for i in range(len(events) - 1):
            assert events[i][1] < events[i + 1][1], f"{events[i][0]} should be before {events[i+1][0]}"

        # Calculate time from Cambrian to first primates
        time_span = events[-1][1] - events[0][1]
        # Approximately 486 million years
        assert 485_000_000 < time_span.years < 487_000_000


class TestFormatting:
    """Test formatting in realistic scenarios."""

    def test_geological_date_formatting(self):
        """Test formatting geological dates for display."""
        dates = [
            PaleoDateTime(-4_500_000_000, 1, 1),  # Earth formation
            PaleoDateTime(-541_000_000, 1, 1),  # Cambrian
            PaleoDateTime(-66_000_000, 1, 1),  # K-Pg extinction
            PaleoDateTime(-10_000, 1, 1),  # End of last ice age
            PaleoDateTime(2024, 1, 1),  # Present
        ]

        for dt in dates:
            # Should be able to format and parse back
            iso = dt.isoformat()
            parsed = PaleoDateTime.fromisoformat(iso)
            assert dt == parsed

    def test_timeline_display(self):
        """Test creating formatted timeline."""
        kt_extinction = PaleoDateTime(-66_000_000, 1, 1)
        now = PaleoDateTime(2024, 1, 1)

        time_since = now - kt_extinction

        # Format for display
        million_years = time_since.years / 1_000_000
        assert 66 < million_years < 67
