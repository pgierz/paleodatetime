"""
PaleoDateTime - A datetime-like library for geological timescales.

This module provides datetime functionality for dates spanning millions of years,
with second-level precision suitable for geological and paleontological research.
"""

from .paleodatetime import PaleoDateTime
from .timedelta import PaleoTimeDelta
from .exceptions import PaleoDateTimeError, PaleoDateTimeValueError, PaleoDateTimeFormatError
from .formatting import (
    format_ma,
    format_ka,
    format_geological,
    matplotlib_ticker_formatter,
    matplotlib_ordinal_formatter,
)

# xarray utilities are optional
try:
    from .xarray_utils import (
        years_to_paleodatetime,
        paleodatetime_to_years,
        create_time_coordinate,
        add_paleodatetime_labels,
        decode_paleodatetime_coord,
        encode_paleodatetime_coord,
        create_dataset_with_time,
        format_time_axis_labels,
        time_slice,
    )

    _xarray_available = True
except ImportError:
    _xarray_available = False

__version__ = "0.1.0"
__all__ = [
    "PaleoDateTime",
    "PaleoTimeDelta",
    "PaleoDateTimeError",
    "PaleoDateTimeValueError",
    "PaleoDateTimeFormatError",
    "format_ma",
    "format_ka",
    "format_geological",
    "matplotlib_ticker_formatter",
    "matplotlib_ordinal_formatter",
]

# Add xarray utilities to __all__ if available
if _xarray_available:
    __all__.extend(
        [
            "years_to_paleodatetime",
            "paleodatetime_to_years",
            "create_time_coordinate",
            "add_paleodatetime_labels",
            "decode_paleodatetime_coord",
            "encode_paleodatetime_coord",
            "create_dataset_with_time",
            "format_time_axis_labels",
            "time_slice",
        ]
    )
