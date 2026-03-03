"""Utilities for xarray integration with PaleoDateTime."""

from typing import Union, List, Optional, Any
import numpy as np

try:
    import xarray as xr

    XARRAY_AVAILABLE = True
except ImportError:
    XARRAY_AVAILABLE = False
    xr = None

from .paleodatetime import PaleoDateTime
from .timedelta import PaleoTimeDelta


def require_xarray():
    """Raise ImportError if xarray is not available."""
    if not XARRAY_AVAILABLE:
        raise ImportError(
            "xarray is required for this functionality. "
            "Install with: pip install paleodatetime[xarray]"
        )


def years_to_paleodatetime(
    years: Union[np.ndarray, List[int], int], month: int = 1, day: int = 1
) -> Union[List[PaleoDateTime], PaleoDateTime]:
    """
    Convert year values to PaleoDateTime objects.

    Args:
        years: Year value(s) to convert
        month: Month to use (default 1)
        day: Day to use (default 1)

    Returns:
        PaleoDateTime object(s)

    Examples:
        >>> years_to_paleodatetime([-66_000_000, -252_000_000])
        [PaleoDateTime(-66000000, 1, 1, 0, 0, 0), PaleoDateTime(-252000000, 1, 1, 0, 0, 0)]
    """
    if isinstance(years, (int, np.integer)):
        return PaleoDateTime(int(years), month, day)

    if isinstance(years, np.ndarray):
        years = years.tolist()

    return [PaleoDateTime(int(y), month, day) for y in years]


def paleodatetime_to_years(
    dates: Union[List[PaleoDateTime], PaleoDateTime]
) -> Union[np.ndarray, int]:
    """
    Convert PaleoDateTime objects to year values.

    Args:
        dates: PaleoDateTime object(s) to convert

    Returns:
        Year value(s) as numpy array or int

    Examples:
        >>> dt1 = PaleoDateTime(-66_000_000, 1, 1)
        >>> dt2 = PaleoDateTime(-252_000_000, 1, 1)
        >>> paleodatetime_to_years([dt1, dt2])
        array([-66000000, -252000000])
    """
    if isinstance(dates, PaleoDateTime):
        return dates.year

    return np.array([dt.year for dt in dates])


def create_time_coordinate(
    years: Union[np.ndarray, List[int]],
    name: str = "time",
    attrs: Optional[dict] = None,
) -> "xr.DataArray":
    """
    Create an xarray time coordinate from year values.

    Args:
        years: Year values for the coordinate
        name: Name of the coordinate (default "time")
        attrs: Additional attributes for the coordinate

    Returns:
        xarray DataArray suitable for use as a coordinate

    Examples:
        >>> years = [-66_000_000, -252_000_000]
        >>> time_coord = create_time_coordinate(years)
        >>> time_coord.name
        'time'
    """
    require_xarray()

    if attrs is None:
        attrs = {
            "long_name": "Time",
            "units": "years",
            "calendar": "proleptic_gregorian",
            "axis": "T",
        }

    years_array = np.array(years)

    coord = xr.DataArray(
        years_array,
        dims=[name],
        attrs=attrs,
    )

    return coord


def add_paleodatetime_labels(
    data_array: "xr.DataArray",
    time_dim: str = "time",
    precision: int = 0,
) -> "xr.DataArray":
    """
    Add formatted geological time labels to an xarray DataArray.

    Adds a new coordinate with human-readable labels (e.g., "66 Ma", "252 Ma")
    that can be used for plotting.

    Args:
        data_array: xarray DataArray with time dimension
        time_dim: Name of the time dimension (default "time")
        precision: Precision for Ma/ka formatting (default 0)

    Returns:
        DataArray with added "{time_dim}_label" coordinate

    Examples:
        >>> import xarray as xr
        >>> years = [-66_000_000, -252_000_000]
        >>> data = xr.DataArray([1, 2], coords={"time": years}, dims=["time"])
        >>> labeled = add_paleodatetime_labels(data)
        >>> labeled.time_label.values
        array(['66 Ma', '252 Ma'], dtype=object)
    """
    require_xarray()

    from .formatting import format_geological

    if time_dim not in data_array.dims:
        raise ValueError(f"Dimension '{time_dim}' not found in DataArray")

    # Get time values
    time_values = data_array[time_dim].values

    # Convert to PaleoDateTime and format
    dates = years_to_paleodatetime(time_values)
    if not isinstance(dates, list):
        dates = [dates]

    labels = [format_geological(dt, precision=precision) for dt in dates]

    # Add as new coordinate
    label_coord_name = f"{time_dim}_label"
    result = data_array.assign_coords({label_coord_name: (time_dim, labels)})

    return result


def decode_paleodatetime_coord(
    coord_values: np.ndarray, units: str = "years", reference_year: int = 0
) -> List[PaleoDateTime]:
    """
    Decode numeric time values to PaleoDateTime objects.

    Args:
        coord_values: Numeric time values
        units: Units of the time values ("years", "ka", "Ma")
        reference_year: Reference year (default 0 for absolute years)

    Returns:
        List of PaleoDateTime objects

    Examples:
        >>> values = np.array([66.0, 252.0])
        >>> dates = decode_paleodatetime_coord(values, units="Ma")
        >>> dates[0].year
        -66000000
    """
    if units == "Ma":
        # Millions of years (typically before present or absolute)
        if reference_year == 0:
            # Absolute years (negative for past)
            years = -coord_values * 1_000_000
        else:
            # Years before reference
            years = reference_year - coord_values * 1_000_000
    elif units == "ka":
        # Thousands of years
        if reference_year == 0:
            years = -coord_values * 1_000
        else:
            years = reference_year - coord_values * 1_000
    elif units == "years":
        # Direct year values
        years = coord_values
    else:
        raise ValueError(f"Unknown units: {units}")

    return years_to_paleodatetime(years.astype(int))


def encode_paleodatetime_coord(
    dates: List[PaleoDateTime], units: str = "years", reference_year: int = 0
) -> np.ndarray:
    """
    Encode PaleoDateTime objects to numeric values for NetCDF storage.

    Args:
        dates: List of PaleoDateTime objects
        units: Desired units ("years", "ka", "Ma")
        reference_year: Reference year (default 0 for absolute years)

    Returns:
        Numpy array of numeric time values

    Examples:
        >>> dates = [PaleoDateTime(-66_000_000, 1, 1), PaleoDateTime(-252_000_000, 1, 1)]
        >>> values = encode_paleodatetime_coord(dates, units="Ma")
        >>> values
        array([ 66., 252.])
    """
    years = paleodatetime_to_years(dates)

    if units == "Ma":
        if reference_year == 0:
            # Convert to positive Ma for past dates
            values = -years / 1_000_000.0
        else:
            values = (reference_year - years) / 1_000_000.0
    elif units == "ka":
        if reference_year == 0:
            values = -years / 1_000.0
        else:
            values = (reference_year - years) / 1_000.0
    elif units == "years":
        values = years.astype(float)
    else:
        raise ValueError(f"Unknown units: {units}")

    return values


def create_dataset_with_time(
    data: dict,
    years: Union[np.ndarray, List[int]],
    coords: Optional[dict] = None,
    time_dim: str = "time",
    attrs: Optional[dict] = None,
) -> "xr.Dataset":
    """
    Create an xarray Dataset with PaleoDateTime-aware time coordinate.

    Args:
        data: Dictionary of data variables {name: array}
        years: Year values for time dimension
        coords: Additional coordinates
        time_dim: Name of time dimension (default "time")
        attrs: Global attributes

    Returns:
        xarray Dataset with time coordinate and labels

    Examples:
        >>> years = [-66_000_000, -252_000_000]
        >>> data = {"temperature": ([5, 10], {"units": "degC"})}
        >>> ds = create_dataset_with_time(data, years)
        >>> ds.time.values
        array([-66000000, -252000000])
    """
    require_xarray()

    if coords is None:
        coords = {}

    # Create time coordinate
    time_coord = create_time_coordinate(years, name=time_dim)
    coords[time_dim] = time_coord

    # Create data variables
    data_vars = {}
    for name, value in data.items():
        if isinstance(value, tuple):
            # (data, attrs) format
            data_array, var_attrs = value
            data_vars[name] = xr.DataArray(
                data_array,
                dims=[time_dim],
                coords={time_dim: time_coord},
                attrs=var_attrs,
            )
        else:
            # Just data
            data_vars[name] = xr.DataArray(
                value,
                dims=[time_dim],
                coords={time_dim: time_coord},
            )

    # Create dataset
    ds = xr.Dataset(data_vars, coords=coords, attrs=attrs or {})

    # Add formatted labels
    from .formatting import format_geological

    dates = years_to_paleodatetime(years)
    if not isinstance(dates, list):
        dates = [dates]
    labels = [format_geological(dt, precision=0) for dt in dates]
    ds = ds.assign_coords({f"{time_dim}_label": (time_dim, labels)})

    return ds


def format_time_axis_labels(
    plot_obj: Any,
    time_coord: str = "time",
    precision: int = 0,
) -> None:
    """
    Format time axis labels on an xarray plot with geological time formatting.

    Modifies the plot in-place to use formatted labels.

    Args:
        plot_obj: xarray plot object (from .plot())
        time_coord: Name of time coordinate
        precision: Precision for Ma/ka formatting

    Examples:
        >>> import xarray as xr
        >>> years = [-66_000_000, -252_000_000]
        >>> data = xr.DataArray([1, 2], coords={"time": years}, dims=["time"])
        >>> p = data.plot()
        >>> format_time_axis_labels(p)
    """
    require_xarray()

    from .formatting import matplotlib_ticker_formatter
    from matplotlib.ticker import FuncFormatter

    # Get the axes
    if hasattr(plot_obj, "axes"):
        ax = plot_obj.axes
    elif hasattr(plot_obj, "ax"):
        ax = plot_obj.ax
    else:
        # Try to get current axes
        import matplotlib.pyplot as plt

        ax = plt.gca()

    # Apply formatter
    formatter = matplotlib_ticker_formatter(precision=precision)

    # Determine which axis has time
    if hasattr(ax, "xaxis"):
        ax.xaxis.set_major_formatter(FuncFormatter(formatter))
    if hasattr(ax, "yaxis"):
        ax.yaxis.set_major_formatter(FuncFormatter(formatter))


def time_slice(
    dataset: "xr.Dataset",
    start: Union[PaleoDateTime, int],
    end: Union[PaleoDateTime, int],
    time_dim: str = "time",
) -> "xr.Dataset":
    """
    Slice a dataset by geological time range.

    Args:
        dataset: xarray Dataset to slice
        start: Start time (PaleoDateTime or year)
        end: End time (PaleoDateTime or year)
        time_dim: Name of time dimension

    Returns:
        Sliced dataset

    Examples:
        >>> ds = create_dataset_with_time({"temp": [1, 2, 3]}, [-300_000_000, -200_000_000, -100_000_000])
        >>> sliced = time_slice(ds, -250_000_000, -150_000_000)
        >>> len(sliced.time)
        1
    """
    require_xarray()

    start_year = start.year if isinstance(start, PaleoDateTime) else start
    end_year = end.year if isinstance(end, PaleoDateTime) else end

    # Ensure correct order (older to younger)
    if start_year > end_year:
        start_year, end_year = end_year, start_year

    return dataset.sel({time_dim: slice(start_year, end_year)})
