"""Tests for xarray integration."""

import pytest
import numpy as np

# Check if xarray is available
try:
    import xarray as xr

    XARRAY_AVAILABLE = True
except ImportError:
    XARRAY_AVAILABLE = False

from paleodatetime import PaleoDateTime, PaleoTimeDelta

# Skip all tests if xarray not available
pytestmark = pytest.mark.skipif(not XARRAY_AVAILABLE, reason="xarray not installed")

if XARRAY_AVAILABLE:
    from paleodatetime import (
        years_to_paleodatetime,
        paleodatetime_to_years,
        create_time_coordinate,
        add_paleodatetime_labels,
        decode_paleodatetime_coord,
        encode_paleodatetime_coord,
        create_dataset_with_time,
        time_slice,
    )


@pytest.mark.skipif(not XARRAY_AVAILABLE, reason="xarray not installed")
class TestYearsConversion:
    """Test conversion between years and PaleoDateTime."""

    def test_single_year_to_paleodatetime(self):
        """Test converting single year to PaleoDateTime."""
        dt = years_to_paleodatetime(-66_000_000)
        assert isinstance(dt, PaleoDateTime)
        assert dt.year == -66_000_000
        assert dt.month == 1
        assert dt.day == 1

    def test_array_to_paleodatetime(self):
        """Test converting array of years to PaleoDateTime."""
        years = np.array([-66_000_000, -252_000_000])
        dates = years_to_paleodatetime(years)
        assert isinstance(dates, list)
        assert len(dates) == 2
        assert dates[0].year == -66_000_000
        assert dates[1].year == -252_000_000

    def test_list_to_paleodatetime(self):
        """Test converting list of years to PaleoDateTime."""
        years = [-66_000_000, -252_000_000]
        dates = years_to_paleodatetime(years)
        assert isinstance(dates, list)
        assert len(dates) == 2

    def test_custom_month_day(self):
        """Test conversion with custom month and day."""
        dt = years_to_paleodatetime(-66_000_000, month=6, day=15)
        assert dt.month == 6
        assert dt.day == 15

    def test_paleodatetime_to_years_single(self):
        """Test converting single PaleoDateTime to year."""
        dt = PaleoDateTime(-66_000_000, 1, 1)
        year = paleodatetime_to_years(dt)
        assert year == -66_000_000

    def test_paleodatetime_to_years_list(self):
        """Test converting list of PaleoDateTime to years."""
        dates = [PaleoDateTime(-66_000_000, 1, 1), PaleoDateTime(-252_000_000, 1, 1)]
        years = paleodatetime_to_years(dates)
        assert isinstance(years, np.ndarray)
        assert len(years) == 2
        assert years[0] == -66_000_000
        assert years[1] == -252_000_000


@pytest.mark.skipif(not XARRAY_AVAILABLE, reason="xarray not installed")
class TestTimeCoordinate:
    """Test time coordinate creation."""

    def test_create_time_coordinate(self):
        """Test creating a time coordinate."""
        years = [-66_000_000, -252_000_000]
        coord = create_time_coordinate(years)

        assert isinstance(coord, xr.DataArray)
        assert "time" in coord.dims
        assert len(coord) == 2
        assert coord.values[0] == -66_000_000

    def test_custom_name(self):
        """Test creating coordinate with custom name."""
        years = [-66_000_000, -252_000_000]
        coord = create_time_coordinate(years, name="age")

        assert "age" in coord.dims

    def test_custom_attrs(self):
        """Test creating coordinate with custom attributes."""
        years = [-66_000_000, -252_000_000]
        attrs = {"description": "Test time coordinate"}
        coord = create_time_coordinate(years, attrs=attrs)

        assert coord.attrs["description"] == "Test time coordinate"

    def test_default_attrs(self):
        """Test that default attributes are set."""
        years = [-66_000_000, -252_000_000]
        coord = create_time_coordinate(years)

        assert "units" in coord.attrs
        assert coord.attrs["units"] == "years"
        assert coord.attrs["calendar"] == "proleptic_gregorian"


@pytest.mark.skipif(not XARRAY_AVAILABLE, reason="xarray not installed")
class TestLabeling:
    """Test adding geological time labels."""

    def test_add_labels(self):
        """Test adding formatted labels to DataArray."""
        years = [-66_000_000, -252_000_000]
        data = xr.DataArray([1, 2], coords={"time": years}, dims=["time"])

        labeled = add_paleodatetime_labels(data)

        assert "time_label" in labeled.coords
        assert len(labeled.time_label) == 2
        assert "Ma" in labeled.time_label.values[0]

    def test_custom_time_dim(self):
        """Test adding labels with custom time dimension."""
        years = [-66_000_000, -252_000_000]
        data = xr.DataArray([1, 2], coords={"age": years}, dims=["age"])

        labeled = add_paleodatetime_labels(data, time_dim="age")

        assert "age_label" in labeled.coords

    def test_custom_precision(self):
        """Test adding labels with custom precision."""
        years = [-66_500_000, -252_000_000]
        data = xr.DataArray([1, 2], coords={"time": years}, dims=["time"])

        labeled = add_paleodatetime_labels(data, precision=1)

        # Check that label has decimal
        assert "66.5" in labeled.time_label.values[0] or "67" in labeled.time_label.values[0]

    def test_missing_dimension_error(self):
        """Test error when dimension doesn't exist."""
        data = xr.DataArray([1, 2], dims=["x"])

        with pytest.raises(ValueError, match="Dimension 'time' not found"):
            add_paleodatetime_labels(data)


@pytest.mark.skipif(not XARRAY_AVAILABLE, reason="xarray not installed")
class TestEncoding:
    """Test encoding/decoding PaleoDateTime coordinates."""

    def test_decode_ma_absolute(self):
        """Test decoding Ma values (absolute)."""
        values = np.array([66.0, 252.0])
        dates = decode_paleodatetime_coord(values, units="Ma")

        assert len(dates) == 2
        assert dates[0].year == -66_000_000
        assert dates[1].year == -252_000_000

    def test_decode_ka_absolute(self):
        """Test decoding ka values (absolute)."""
        values = np.array([20.0, 10.0])
        dates = decode_paleodatetime_coord(values, units="ka")

        assert dates[0].year == -20_000
        assert dates[1].year == -10_000

    def test_decode_years(self):
        """Test decoding year values."""
        values = np.array([-66_000_000, -252_000_000])
        dates = decode_paleodatetime_coord(values, units="years")

        assert dates[0].year == -66_000_000
        assert dates[1].year == -252_000_000

    def test_decode_ma_with_reference(self):
        """Test decoding Ma with reference year."""
        values = np.array([66.0, 252.0])
        dates = decode_paleodatetime_coord(values, units="Ma", reference_year=2024)

        # 2024 - 66,000,000 = -65,997,976
        assert dates[0].year == -65_997_976

    def test_encode_ma_absolute(self):
        """Test encoding to Ma values (absolute)."""
        dates = [PaleoDateTime(-66_000_000, 1, 1), PaleoDateTime(-252_000_000, 1, 1)]
        values = encode_paleodatetime_coord(dates, units="Ma")

        assert isinstance(values, np.ndarray)
        assert values[0] == 66.0
        assert values[1] == 252.0

    def test_encode_ka_absolute(self):
        """Test encoding to ka values (absolute)."""
        dates = [PaleoDateTime(-20_000, 1, 1), PaleoDateTime(-10_000, 1, 1)]
        values = encode_paleodatetime_coord(dates, units="ka")

        assert values[0] == 20.0
        assert values[1] == 10.0

    def test_encode_years(self):
        """Test encoding to year values."""
        dates = [PaleoDateTime(-66_000_000, 1, 1), PaleoDateTime(-252_000_000, 1, 1)]
        values = encode_paleodatetime_coord(dates, units="years")

        assert values[0] == -66_000_000.0
        assert values[1] == -252_000_000.0

    def test_roundtrip(self):
        """Test encoding and decoding roundtrip."""
        original_dates = [
            PaleoDateTime(-66_000_000, 1, 1),
            PaleoDateTime(-252_000_000, 1, 1),
        ]

        # Encode to Ma
        values = encode_paleodatetime_coord(original_dates, units="Ma")

        # Decode back
        decoded_dates = decode_paleodatetime_coord(values, units="Ma")

        assert len(decoded_dates) == len(original_dates)
        assert decoded_dates[0].year == original_dates[0].year
        assert decoded_dates[1].year == original_dates[1].year


@pytest.mark.skipif(not XARRAY_AVAILABLE, reason="xarray not installed")
class TestDatasetCreation:
    """Test creating xarray datasets."""

    def test_create_simple_dataset(self):
        """Test creating a simple dataset."""
        years = [-66_000_000, -252_000_000]
        data = {"temperature": [5.0, 10.0]}

        ds = create_dataset_with_time(data, years)

        assert isinstance(ds, xr.Dataset)
        assert "time" in ds.dims
        assert "temperature" in ds.data_vars
        assert len(ds.time) == 2

    def test_create_dataset_with_attrs(self):
        """Test creating dataset with variable attributes."""
        years = [-66_000_000, -252_000_000]
        data = {"temperature": ([5.0, 10.0], {"units": "degC", "long_name": "Temperature"})}

        ds = create_dataset_with_time(data, years)

        assert ds.temperature.attrs["units"] == "degC"
        assert ds.temperature.attrs["long_name"] == "Temperature"

    def test_create_dataset_with_labels(self):
        """Test that labels are automatically added."""
        years = [-66_000_000, -252_000_000]
        data = {"temperature": [5.0, 10.0]}

        ds = create_dataset_with_time(data, years)

        assert "time_label" in ds.coords
        assert "Ma" in ds.time_label.values[0]

    def test_create_dataset_multiple_vars(self):
        """Test creating dataset with multiple variables."""
        years = [-66_000_000, -252_000_000]
        data = {
            "temperature": [5.0, 10.0],
            "co2": [280.0, 300.0],
        }

        ds = create_dataset_with_time(data, years)

        assert "temperature" in ds.data_vars
        assert "co2" in ds.data_vars
        assert len(ds.data_vars) == 2

    def test_create_dataset_global_attrs(self):
        """Test creating dataset with global attributes."""
        years = [-66_000_000, -252_000_000]
        data = {"temperature": [5.0, 10.0]}
        attrs = {"title": "Test Dataset", "source": "PaleoDateTime"}

        ds = create_dataset_with_time(data, years, attrs=attrs)

        assert ds.attrs["title"] == "Test Dataset"
        assert ds.attrs["source"] == "PaleoDateTime"


@pytest.mark.skipif(not XARRAY_AVAILABLE, reason="xarray not installed")
class TestTimeSlicing:
    """Test slicing datasets by time."""

    def test_time_slice_years(self):
        """Test slicing with year values."""
        years = [-300_000_000, -200_000_000, -100_000_000]
        data = {"temperature": [1.0, 2.0, 3.0]}
        ds = create_dataset_with_time(data, years)

        sliced = time_slice(ds, -250_000_000, -150_000_000)

        assert len(sliced.time) == 1
        assert sliced.time.values[0] == -200_000_000

    def test_time_slice_paleodatetime(self):
        """Test slicing with PaleoDateTime objects."""
        years = [-300_000_000, -200_000_000, -100_000_000]
        data = {"temperature": [1.0, 2.0, 3.0]}
        ds = create_dataset_with_time(data, years)

        start = PaleoDateTime(-250_000_000, 1, 1)
        end = PaleoDateTime(-150_000_000, 1, 1)
        sliced = time_slice(ds, start, end)

        assert len(sliced.time) == 1

    def test_time_slice_reversed_order(self):
        """Test that slicing handles reversed order."""
        years = [-300_000_000, -200_000_000, -100_000_000]
        data = {"temperature": [1.0, 2.0, 3.0]}
        ds = create_dataset_with_time(data, years)

        # Provide end before start - should still work
        sliced = time_slice(ds, -150_000_000, -250_000_000)

        assert len(sliced.time) == 1


@pytest.mark.skipif(not XARRAY_AVAILABLE, reason="xarray not installed")
class TestIntegration:
    """Test realistic integration scenarios."""

    def test_paleo_climate_workflow(self):
        """Test a complete paleo-climate workflow."""
        # Create geological timescale
        years = np.linspace(-500_000_000, 0, 100)

        # Create synthetic climate data
        temperature = 15 + 5 * np.sin(years / 100_000_000)
        co2 = 280 + 100 * np.sin(years / 100_000_000)

        # Create dataset
        ds = create_dataset_with_time(
            {
                "temperature": (temperature, {"units": "degC", "long_name": "Global Temperature"}),
                "co2": (co2, {"units": "ppm", "long_name": "Atmospheric CO2"}),
            },
            years,
            attrs={"title": "Synthetic Phanerozoic Climate Data"},
        )

        # Check structure
        assert "time" in ds.dims
        assert "time_label" in ds.coords
        assert "temperature" in ds.data_vars
        assert "co2" in ds.data_vars

        # Slice to Mesozoic era
        mesozoic_start = PaleoDateTime(-252_000_000, 1, 1)
        mesozoic_end = PaleoDateTime(-66_000_000, 1, 1)
        mesozoic_data = time_slice(ds, mesozoic_start, mesozoic_end)

        assert len(mesozoic_data.time) > 0
        assert all(mesozoic_data.time.values >= -252_000_000)
        assert all(mesozoic_data.time.values <= -66_000_000)

    def test_convert_existing_dataset(self):
        """Test converting an existing xarray dataset to use PaleoDateTime labels."""
        # Create a standard xarray dataset
        years = np.array([-66_000_000, -252_000_000, -445_000_000])
        ds = xr.Dataset(
            {"extinction_severity": (["time"], [76, 96, 85])},
            coords={"time": years},
        )

        # Add PaleoDateTime labels
        ds_labeled = xr.Dataset(
            ds.data_vars,
            coords=ds.coords,
        )
        for var in ds_labeled.data_vars:
            ds_labeled[var] = add_paleodatetime_labels(ds_labeled[var])

        assert "time_label" in ds_labeled.extinction_severity.coords

    def test_encoding_for_netcdf(self):
        """Test preparing data for NetCDF export."""
        years = [-66_000_000, -252_000_000]
        dates = years_to_paleodatetime(years)

        # Encode to Ma for storage
        ma_values = encode_paleodatetime_coord(dates, units="Ma")

        # Create dataset with Ma values
        ds = xr.Dataset(
            {"temperature": (["time"], [5.0, 10.0])},
            coords={"time": ma_values},
        )

        ds["time"].attrs["units"] = "Ma"
        ds["time"].attrs["long_name"] = "Time before present"

        assert ds.time.values[0] == 66.0
        assert ds.time.attrs["units"] == "Ma"
