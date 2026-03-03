"""Exception classes for paleodatetime module."""


class PaleoDateTimeError(Exception):
    """Base exception for all paleodatetime errors."""
    pass


class PaleoDateTimeValueError(PaleoDateTimeError, ValueError):
    """Raised when an invalid value is provided to a paleodatetime operation."""
    pass


class PaleoDateTimeFormatError(PaleoDateTimeError, ValueError):
    """Raised when a string format is invalid for parsing."""
    pass
