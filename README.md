# PaleoDateTime

A Python library providing datetime-like functionality for geological timescales, supporting dates spanning millions of years with second-level precision.

## Features

- **Geological Timescales**: Handle dates from millions of years ago to millions of years in the future
- **Datetime-like API**: Familiar interface for Python developers
- **Second Precision**: Maximum precision of seconds (no nanoseconds)
- **Arithmetic Operations**: Add/subtract time deltas, compare dates
- **String Formatting**: ISO-8601-like formatting and parsing
- **Pure Python**: No external dependencies

## Installation

Using pixi:
```bash
pixi add paleodatetime
```

Using pip:
```bash
pip install paleodatetime
```

## Quick Start

```python
from paleodatetime import PaleoDateTime, PaleoTimeDelta

# Create a date 65 million years ago (K-Pg boundary)
kt_extinction = PaleoDateTime(year=-65_000_000, month=1, day=1)

# Create a date 252 million years ago (Permian-Triassic boundary)
pt_extinction = PaleoDateTime(year=-252_000_000, month=1, day=1)

# Calculate time difference
time_span = kt_extinction - pt_extinction
print(f"Time between extinctions: {time_span.years} million years")

# Add time deltas
future_date = kt_extinction + PaleoTimeDelta(years=1_000_000)
print(f"One million years later: {future_date}")

# Format as string
print(kt_extinction.isoformat())  # -65000000-01-01T00:00:00

# Parse from string
date = PaleoDateTime.fromisoformat("-252000000-01-01T00:00:00")
```

## Matplotlib Integration

PaleoDateTime includes built-in support for matplotlib tick label formatting:

```python
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from paleodatetime import PaleoDateTime, matplotlib_ticker_formatter

# Create a plot with geological time on x-axis
fig, ax = plt.subplots()

# Sample data: mass extinctions
extinctions = [
    PaleoDateTime(-445_000_000, 1, 1),  # Ordovician-Silurian
    PaleoDateTime(-375_000_000, 1, 1),  # Late Devonian
    PaleoDateTime(-252_000_000, 1, 1),  # Permian-Triassic
    PaleoDateTime(-66_000_000, 1, 1),   # K-Pg
]
years = [dt.year for dt in extinctions]
extinctions_pct = [85, 75, 96, 76]

ax.scatter(years, extinctions_pct)

# Format x-axis with geological time labels
formatter = matplotlib_ticker_formatter(precision=0)
ax.xaxis.set_major_formatter(FuncFormatter(formatter))

ax.set_xlabel("Time")
ax.set_ylabel("Species Extinction (%)")
plt.show()
```

### Formatting Methods

```python
# Format as "Ma" (millions of years ago)
dt = PaleoDateTime(-66_000_000, 1, 1)
print(dt.format_ma())  # "66.0 Ma"

# Format as "ka" (thousands of years ago)
dt = PaleoDateTime(-20_000, 1, 1)
print(dt.format_ka())  # "22.0 ka"

# Intelligent formatting based on magnitude
print(PaleoDateTime(-66_000_000, 1, 1).format_geological())  # "66.0 Ma"
print(PaleoDateTime(-20_000, 1, 1).format_geological())      # "22.0 ka"
print(PaleoDateTime(-500, 1, 1).format_geological())         # "501 BCE"
print(PaleoDateTime(1492, 1, 1).format_geological())         # "1492 CE"
```

## API Reference

### PaleoDateTime

Main class for representing a point in geological time.

**Constructor:**
```python
PaleoDateTime(year, month=1, day=1, hour=0, minute=0, second=0)
```

**Class Methods:**
- `now()` - Current date and time
- `fromisoformat(date_string)` - Parse ISO-8601-like string
- `fromtimestamp(timestamp)` - Create from Unix timestamp

**Instance Methods:**
- `isoformat()` - Return ISO-8601-like string representation
- `timestamp()` - Return Unix timestamp (for dates within valid range)
- `replace(**kwargs)` - Return new instance with replaced fields
- `format_ma(precision=1)` - Format as "66.0 Ma" (millions of years ago)
- `format_ka(precision=1)` - Format as "22.0 ka" (thousands of years ago)
- `format_geological()` - Intelligently format based on magnitude (Ma/ka/BCE/CE)

**Arithmetic:**
- `paleodatetime + timedelta` → `paleodatetime`
- `paleodatetime - timedelta` → `paleodatetime`
- `paleodatetime - paleodatetime` → `timedelta`

**Comparisons:**
- All comparison operators supported (`<`, `<=`, `==`, `!=`, `>=`, `>`)

### PaleoTimeDelta

Represents a duration in geological time.

**Constructor:**
```python
PaleoTimeDelta(years=0, months=0, days=0, hours=0, minutes=0, seconds=0)
```

**Properties:**
- `total_seconds` - Total duration in seconds
- `years` - Years component
- `days` - Days component
- `seconds` - Seconds component

## Design Rationale

Standard Python `datetime` is limited to years 1-9999 CE. Geological research requires:

1. **Extended Range**: Support for millions of years (Ma)
2. **Negative Years**: BCE dates represented as negative years
3. **Reduced Precision**: Second-level precision is sufficient; nanoseconds unnecessary
4. **Familiar API**: Maintain datetime-like interface for easy adoption

## Limitations

- Maximum precision is seconds (no microseconds/nanoseconds)
- Calendar calculations assume proleptic Gregorian calendar
- No timezone support (geological time is absolute)
- Timestamp conversion only works for dates within Unix timestamp range

### Matplotlib Utilities

**Formatter Functions:**
- `matplotlib_ticker_formatter(reference_year=2024, precision=1)` - Create FuncFormatter for axes with year values
- `matplotlib_ordinal_formatter(ascending=True)` - Create FuncFormatter for axes with Ma values
- `format_ma(dt, precision=1)` - Format PaleoDateTime as Ma
- `format_ka(dt, precision=1)` - Format PaleoDateTime as ka
- `format_geological(dt)` - Intelligently format PaleoDateTime

### xarray Integration

PaleoDateTime integrates seamlessly with xarray for multidimensional paleoclimate data analysis:

**Installation:**
```bash
pip install paleodatetime[xarray]
```

**Key Functions:**
```python
from paleodatetime import (
    create_dataset_with_time,      # Create xarray Dataset with geological time
    add_paleodatetime_labels,       # Add formatted time labels to existing data
    time_slice,                      # Slice datasets by geological period
    encode_paleodatetime_coord,     # Encode for NetCDF storage (Ma/ka/years)
    decode_paleodatetime_coord,     # Decode from NetCDF (Ma/ka/years)
)

# Create a paleoclimate dataset
import numpy as np
years = np.linspace(-540_000_000, 0, 1000)  # Phanerozoic Eon
temperature = 15 + 5 * np.sin(years / 100_000_000)

ds = create_dataset_with_time(
    {"temperature": (temperature, {"units": "degC"})},
    years,
    attrs={"title": "Phanerozoic Climate"}
)

# Slice to Mesozoic Era
from paleodatetime import PaleoDateTime
mesozoic = time_slice(
    ds,
    PaleoDateTime(-252_000_000, 1, 1),  # Start of Triassic
    PaleoDateTime(-66_000_000, 1, 1)    # End of Cretaceous
)

# Encode for NetCDF storage
dates = [PaleoDateTime(-66_000_000, 1, 1), PaleoDateTime(-252_000_000, 1, 1)]
ma_values = encode_paleodatetime_coord(dates, units="Ma")  # [66.0, 252.0]

# Save to NetCDF with Ma encoding
ds.to_netcdf("paleoclimate.nc")
```

**Features:**
- Automatic geological time label generation (Ma/ka/BCE/CE)
- Time coordinate creation with proper metadata
- NetCDF encoding/decoding with multiple unit options (years/ka/Ma)
- Time-based slicing with PaleoDateTime objects
- Integration with xarray plotting

## Examples

See the `examples/` directory for complete examples:
- `basic_usage.py` - Basic operations and formatting
- `geological_timescale.py` - Mass extinctions and geological periods
- `matplotlib_example.py` - Five complete matplotlib plotting examples
- `xarray_example.py` - xarray integration for paleoclimate data analysis

## Development

Setup development environment:
```bash
pixi install -e dev
```

Run tests:
```bash
pixi run -e dev pytest
```

Run examples:
```bash
pixi run python examples/basic_usage.py
pixi run python examples/geological_timescale.py
MPLBACKEND=Agg pixi run -e dev python examples/matplotlib_example.py
```

Format code:
```bash
pixi run -e dev black src tests
pixi run -e dev ruff check src tests
```

### Releasing

Releases are published to PyPI by the `Publish` workflow, which runs on `v*` tags:

1. Bump `__version__` in `src/paleodatetime/__init__.py` (the only place the version lives).
2. Move the `Unreleased` section of `CHANGELOG.md` under the new version.
3. Commit, then tag and push:
   ```bash
   git tag v0.2.0
   git push origin master v0.2.0
   ```

The workflow refuses to publish if the tag and `__version__` disagree. To exercise the
publication path without a release, run the `Publish` workflow by hand from the Actions
tab; that uploads to TestPyPI instead.

## License

MIT License - See LICENSE file for details
