"""Formatting utilities for PaleoDateTime, especially for matplotlib integration."""

from typing import Optional, Callable
from .paleodatetime import PaleoDateTime


def format_ma(dt: PaleoDateTime, precision: int = 1, reference_year: int = 2024) -> str:
    """
    Format a PaleoDateTime as millions of years ago (Ma).

    Args:
        dt: PaleoDateTime to format
        precision: Number of decimal places (default 1)
        reference_year: Reference year for "ago" calculation (default 2024)

    Returns:
        Formatted string like "66.0 Ma" or "252.5 Ma"

    Examples:
        >>> from paleodatetime import PaleoDateTime
        >>> kt = PaleoDateTime(-66_000_000, 1, 1)
        >>> format_ma(kt)
        '66.0 Ma'
    """
    years_ago = reference_year - dt.year
    ma = years_ago / 1_000_000
    return f"{ma:.{precision}f} Ma"


def format_ka(dt: PaleoDateTime, precision: int = 1, reference_year: int = 2024) -> str:
    """
    Format a PaleoDateTime as thousands of years ago (ka).

    Args:
        dt: PaleoDateTime to format
        precision: Number of decimal places (default 1)
        reference_year: Reference year for "ago" calculation (default 2024)

    Returns:
        Formatted string like "10.5 ka" or "125.0 ka"

    Examples:
        >>> from paleodatetime import PaleoDateTime
        >>> lgm = PaleoDateTime(-20_000, 1, 1)
        >>> format_ka(lgm)
        '22.0 ka'
    """
    years_ago = reference_year - dt.year
    ka = years_ago / 1_000
    return f"{ka:.{precision}f} ka"


def format_geological(
    dt: PaleoDateTime,
    reference_year: int = 2024,
    use_ma_threshold: int = 1_000_000,
    use_ka_threshold: int = 10_000,
    precision: int = 1,
) -> str:
    """
    Intelligently format a PaleoDateTime based on its magnitude.

    Uses Ma (millions of years) for dates > 1 million years ago,
    ka (thousands of years) for dates > 10,000 years ago,
    and CE/BCE for more recent dates.

    Args:
        dt: PaleoDateTime to format
        reference_year: Reference year for "ago" calculation (default 2024)
        use_ma_threshold: Threshold for using Ma format (default 1,000,000)
        use_ka_threshold: Threshold for using ka format (default 10,000)
        precision: Number of decimal places for Ma/ka (default 1)

    Returns:
        Formatted string appropriate for the date's magnitude

    Examples:
        >>> from paleodatetime import PaleoDateTime
        >>> format_geological(PaleoDateTime(-66_000_000, 1, 1))
        '66.0 Ma'
        >>> format_geological(PaleoDateTime(-20_000, 1, 1))
        '22.0 ka'
        >>> format_geological(PaleoDateTime(-500, 1, 1))
        '500 BCE'
        >>> format_geological(PaleoDateTime(1492, 1, 1))
        '1492 CE'
    """
    years_ago = reference_year - dt.year

    if abs(years_ago) >= use_ma_threshold:
        ma = years_ago / 1_000_000
        return f"{ma:.{precision}f} Ma"
    elif abs(years_ago) >= use_ka_threshold:
        ka = years_ago / 1_000
        return f"{ka:.{precision}f} ka"
    elif dt.year <= 0:
        # BCE dates (astronomical year numbering: year 0 = 1 BCE)
        bce_year = 1 - dt.year
        return f"{bce_year} BCE"
    else:
        return f"{dt.year} CE"


def matplotlib_ticker_formatter(
    reference_year: int = 2024, precision: int = 1
) -> Callable[[float, int], str]:
    """
    Create a matplotlib FuncFormatter for geological time axes.

    Returns a formatter function that can be used with matplotlib's
    FuncFormatter to format tick labels on a geological time axis.

    Args:
        reference_year: Reference year for "ago" calculation (default 2024)
        precision: Number of decimal places for Ma/ka (default 1)

    Returns:
        Formatter function suitable for matplotlib.ticker.FuncFormatter

    Example:
        >>> import matplotlib.pyplot as plt
        >>> from matplotlib.ticker import FuncFormatter
        >>> from paleodatetime.formatting import matplotlib_ticker_formatter
        >>>
        >>> fig, ax = plt.subplots()
        >>> ax.plot([-66_000_000, -252_000_000], [1, 2])
        >>> formatter = matplotlib_ticker_formatter()
        >>> ax.xaxis.set_major_formatter(FuncFormatter(formatter))
        >>> plt.show()
    """

    def formatter(x: float, pos: int) -> str:
        """Format a numerical value as geological time."""
        try:
            # x is the year value
            year = int(x)
            dt = PaleoDateTime(year, 1, 1)
            return format_geological(dt, reference_year=reference_year, precision=precision)
        except Exception:
            # Fallback for invalid values
            return f"{x:.0f}"

    return formatter


def matplotlib_ordinal_formatter(ascending: bool = True) -> Callable[[float, int], str]:
    """
    Create a matplotlib FuncFormatter for ordinal geological time (oldest to youngest).

    Returns a formatter function that formats years as "66 Ma", "252 Ma" etc,
    suitable for axes where older dates have larger values (common in geology).

    Args:
        ascending: If True, assumes larger values = older (default)
                  If False, assumes larger values = younger

    Returns:
        Formatter function suitable for matplotlib.ticker.FuncFormatter

    Example:
        >>> import matplotlib.pyplot as plt
        >>> from matplotlib.ticker import FuncFormatter
        >>> from paleodatetime.formatting import matplotlib_ordinal_formatter
        >>>
        >>> fig, ax = plt.subplots()
        >>> # Plot with age on x-axis (larger = older)
        >>> ax.plot([66, 252], [1, 2])  # Ma values
        >>> formatter = matplotlib_ordinal_formatter(ascending=True)
        >>> ax.xaxis.set_major_formatter(FuncFormatter(formatter))
        >>> plt.show()
    """

    def formatter(x: float, pos: int) -> str:
        """Format a Ma value as geological time."""
        try:
            ma_value = abs(x) if ascending else x
            if ma_value >= 1.0:
                return f"{ma_value:.1f} Ma"
            elif ma_value >= 0.001:
                ka_value = ma_value * 1000
                return f"{ka_value:.1f} ka"
            else:
                years = ma_value * 1_000_000
                return f"{years:.0f} years"
        except Exception:
            return f"{x:.0f}"

    return formatter


# Add methods to PaleoDateTime class dynamically
def _add_formatting_methods():
    """Add formatting methods to PaleoDateTime class."""

    def format_ma_method(self, precision: int = 1, reference_year: int = 2024) -> str:
        """
        Format this PaleoDateTime as millions of years ago (Ma).

        Args:
            precision: Number of decimal places (default 1)
            reference_year: Reference year for "ago" calculation (default 2024)

        Returns:
            Formatted string like "66.0 Ma"
        """
        return format_ma(self, precision=precision, reference_year=reference_year)

    def format_ka_method(self, precision: int = 1, reference_year: int = 2024) -> str:
        """
        Format this PaleoDateTime as thousands of years ago (ka).

        Args:
            precision: Number of decimal places (default 1)
            reference_year: Reference year for "ago" calculation (default 2024)

        Returns:
            Formatted string like "22.0 ka"
        """
        return format_ka(self, precision=precision, reference_year=reference_year)

    def format_geological_method(
        self,
        reference_year: int = 2024,
        use_ma_threshold: int = 1_000_000,
        use_ka_threshold: int = 10_000,
        precision: int = 1,
    ) -> str:
        """
        Intelligently format this PaleoDateTime based on its magnitude.

        Args:
            reference_year: Reference year for "ago" calculation (default 2024)
            use_ma_threshold: Threshold for using Ma format (default 1,000,000)
            use_ka_threshold: Threshold for using ka format (default 10,000)
            precision: Number of decimal places for Ma/ka (default 1)

        Returns:
            Formatted string appropriate for the date's magnitude
        """
        return format_geological(
            self,
            reference_year=reference_year,
            use_ma_threshold=use_ma_threshold,
            use_ka_threshold=use_ka_threshold,
            precision=precision,
        )

    # Add methods to PaleoDateTime
    PaleoDateTime.format_ma = format_ma_method
    PaleoDateTime.format_ka = format_ka_method
    PaleoDateTime.format_geological = format_geological_method


# Add methods when module is imported
_add_formatting_methods()
