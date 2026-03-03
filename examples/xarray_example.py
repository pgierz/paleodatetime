"""Example: Using PaleoDateTime with xarray for paleoclimate data analysis."""

import numpy as np
import matplotlib.pyplot as plt

try:
    import xarray as xr
except ImportError:
    print("xarray is required for this example.")
    print("Install with: pip install paleodatetime[xarray]")
    exit(1)

from paleodatetime import (
    PaleoDateTime,
    create_dataset_with_time,
    add_paleodatetime_labels,
    time_slice,
    encode_paleodatetime_coord,
    decode_paleodatetime_coord,
    years_to_paleodatetime,
)


def example_1_create_paleo_dataset():
    """Create a synthetic paleoclimate dataset spanning the Phanerozoic."""
    print("Example 1: Creating Paleoclimate Dataset")
    print("-" * 60)

    # Time axis: Last 540 million years (Phanerozoic Eon)
    years = np.linspace(-540_000_000, 0, 1000)

    # Synthetic data with long-term trends and cycles
    # Temperature varies between 12-22°C
    base_temp = 17.0
    long_term_trend = -2.0 * np.cos(years / 200_000_000)  # Long-term oscillation
    ice_age_cycles = 3.0 * np.sin(years / 100_000_000)  # Shorter cycles
    temperature = base_temp + long_term_trend + ice_age_cycles

    # CO2 varies between 200-2000 ppm
    base_co2 = 600
    co2_variation = 700 * np.sin(years / 150_000_000)
    co2 = base_co2 + co2_variation

    # Sea level relative to present (-120m to +80m)
    sea_level = 30 * np.sin(years / 120_000_000) + 20 * np.cos(years / 80_000_000)

    # Create dataset with metadata
    ds = create_dataset_with_time(
        {
            "temperature": (
                temperature,
                {
                    "units": "degC",
                    "long_name": "Global Mean Surface Temperature",
                    "description": "Synthetic Phanerozoic temperature reconstruction",
                },
            ),
            "co2": (
                co2,
                {
                    "units": "ppm",
                    "long_name": "Atmospheric CO2 Concentration",
                    "description": "Synthetic CO2 levels",
                },
            ),
            "sea_level": (
                sea_level,
                {
                    "units": "m",
                    "long_name": "Sea Level Relative to Present",
                    "description": "Synthetic sea level reconstruction",
                },
            ),
        },
        years,
        attrs={
            "title": "Synthetic Phanerozoic Climate Data",
            "source": "PaleoDateTime Example",
            "time_period": "540 Ma to Present",
            "calendar": "proleptic_gregorian",
        },
    )

    # Display dataset info
    print("\nDataset created successfully!")
    print(f"Time range: {ds.time.values[0]:,} to {ds.time.values[-1]:,} years")
    print(f"Number of time steps: {len(ds.time)}")
    print(f"Variables: {list(ds.data_vars)}")
    print(f"\nFirst few time labels: {ds.time_label.values[:3]}")
    print(f"Last few time labels: {ds.time_label.values[-3:]}")

    return ds


def example_2_time_slicing(ds):
    """Demonstrate time slicing for different geological periods."""
    print("\n\nExample 2: Slicing by Geological Period")
    print("-" * 60)

    # Define geological periods
    periods = {
        "Mesozoic": (PaleoDateTime(-252_000_000, 1, 1), PaleoDateTime(-66_000_000, 1, 1)),
        "Paleozoic": (PaleoDateTime(-541_000_000, 1, 1), PaleoDateTime(-252_000_000, 1, 1)),
        "Cenozoic": (PaleoDateTime(-66_000_000, 1, 1), PaleoDateTime(2024, 1, 1)),
    }

    for period_name, (start, end) in periods.items():
        sliced = time_slice(ds, start, end)

        avg_temp = float(sliced.temperature.mean())
        avg_co2 = float(sliced.co2.mean())

        print(f"\n{period_name} Era ({start.format_ma(0)} - {end.format_ma(0)}):")
        print(f"  Average Temperature: {avg_temp:.1f}°C")
        print(f"  Average CO2: {avg_co2:.0f} ppm")
        print(f"  Data points: {len(sliced.time)}")


def example_3_plotting_with_labels(ds):
    """Create plots using geological time labels."""
    print("\n\nExample 3: Plotting with Geological Time Labels")
    print("-" * 60)

    fig, axes = plt.subplots(3, 1, figsize=(14, 10))

    # Plot 1: Temperature
    ax1 = axes[0]
    ds.temperature.plot(ax=ax1, color="red", linewidth=1.5)
    ax1.set_title("Global Temperature Over Phanerozoic", fontsize=14, fontweight="bold")
    ax1.set_ylabel("Temperature (°C)", fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.invert_xaxis()

    # Plot 2: CO2
    ax2 = axes[1]
    ds.co2.plot(ax=ax2, color="blue", linewidth=1.5)
    ax2.set_title("Atmospheric CO2 Concentration", fontsize=14, fontweight="bold")
    ax2.set_ylabel("CO2 (ppm)", fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.invert_xaxis()

    # Plot 3: Sea Level
    ax3 = axes[2]
    ds.sea_level.plot(ax=ax3, color="green", linewidth=1.5)
    ax3.axhline(y=0, color="k", linestyle="--", alpha=0.5)
    ax3.set_title("Sea Level Relative to Present", fontsize=14, fontweight="bold")
    ax3.set_ylabel("Sea Level (m)", fontsize=11)
    ax3.set_xlabel("Time", fontsize=11)
    ax3.grid(True, alpha=0.3)
    ax3.invert_xaxis()

    # Apply geological time formatting to all axes
    from matplotlib.ticker import FuncFormatter
    from paleodatetime import matplotlib_ticker_formatter

    formatter = matplotlib_ticker_formatter(precision=0)
    for ax in axes:
        ax.xaxis.set_major_formatter(FuncFormatter(formatter))

    plt.tight_layout()
    plt.savefig("xarray_phanerozoic_climate.png", dpi=150, bbox_inches="tight")
    print("  Saved: xarray_phanerozoic_climate.png")
    plt.close()


def example_4_mass_extinctions_analysis(ds):
    """Analyze climate around mass extinction events."""
    print("\n\nExample 4: Climate During Mass Extinctions")
    print("-" * 60)

    # Big Five mass extinctions
    extinctions = {
        "Ordovician-Silurian": PaleoDateTime(-445_000_000, 1, 1),
        "Late Devonian": PaleoDateTime(-375_000_000, 1, 1),
        "Permian-Triassic": PaleoDateTime(-252_000_000, 1, 1),
        "Triassic-Jurassic": PaleoDateTime(-201_000_000, 1, 1),
        "K-Pg": PaleoDateTime(-66_000_000, 1, 1),
    }

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    # Plot temperature with extinction markers
    ds.temperature.plot(ax=ax1, color="red", linewidth=2, alpha=0.7)
    ax1.set_ylabel("Temperature (°C)", fontsize=11)
    ax1.set_title(
        "Climate Conditions During Mass Extinctions", fontsize=14, fontweight="bold"
    )
    ax1.grid(True, alpha=0.3)

    # Plot CO2 with extinction markers
    ds.co2.plot(ax=ax2, color="blue", linewidth=2, alpha=0.7)
    ax2.set_ylabel("CO2 (ppm)", fontsize=11)
    ax2.set_xlabel("Time", fontsize=11)
    ax2.grid(True, alpha=0.3)

    # Mark extinctions on both plots
    for name, date in extinctions.items():
        year = date.year

        # Find nearest data point
        nearest_idx = np.argmin(np.abs(ds.time.values - year))
        nearest_year = ds.time.values[nearest_idx]
        temp = float(ds.temperature.values[nearest_idx])
        co2 = float(ds.co2.values[nearest_idx])

        # Add vertical lines and annotations
        for ax in [ax1, ax2]:
            ax.axvline(x=nearest_year, color="black", linestyle="--", alpha=0.5, linewidth=1)

        # Annotate on temperature plot
        ax1.plot(nearest_year, temp, "ro", markersize=8, zorder=5)
        ax1.annotate(
            name,
            xy=(nearest_year, temp),
            xytext=(10, 10),
            textcoords="offset points",
            fontsize=8,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
        )

        # Annotate on CO2 plot
        ax2.plot(nearest_year, co2, "bo", markersize=8, zorder=5)

        print(f"\n{name} ({date.format_ma(0)}):")
        print(f"  Temperature: {temp:.1f}°C")
        print(f"  CO2: {co2:.0f} ppm")

    # Format time axes
    from matplotlib.ticker import FuncFormatter
    from paleodatetime import matplotlib_ticker_formatter

    formatter = matplotlib_ticker_formatter(precision=0)
    ax2.xaxis.set_major_formatter(FuncFormatter(formatter))
    ax1.invert_xaxis()
    ax2.invert_xaxis()

    plt.tight_layout()
    plt.savefig("xarray_mass_extinctions.png", dpi=150, bbox_inches="tight")
    print("\n  Saved: xarray_mass_extinctions.png")
    plt.close()


def example_5_encoding_for_netcdf():
    """Demonstrate encoding data for NetCDF export."""
    print("\n\nExample 5: Encoding for NetCDF Export")
    print("-" * 60)

    # Create a smaller dataset
    years = np.array([-252_000_000, -201_000_000, -145_000_000, -66_000_000, -23_000_000])
    dates = years_to_paleodatetime(years)

    # Encode as Ma for storage
    ma_values = encode_paleodatetime_coord(dates, units="Ma")

    print(f"\nOriginal years: {years}")
    print(f"Encoded as Ma: {ma_values}")

    # Create dataset with Ma values
    ds_ma = xr.Dataset(
        {
            "temperature": (["time"], [22.0, 18.0, 20.0, 15.0, 14.0]),
            "co2": (["time"], [1200.0, 1000.0, 800.0, 500.0, 300.0]),
        },
        coords={"time": ma_values},
    )

    # Add proper metadata
    ds_ma["time"].attrs = {
        "units": "Ma",
        "long_name": "Time before present",
        "calendar": "proleptic_gregorian",
        "description": "Millions of years ago",
    }

    ds_ma.attrs = {
        "title": "Mesozoic to Cenozoic Climate",
        "encoding_note": "Time encoded as Ma (millions of years before 2024)",
        "source": "PaleoDateTime xarray example",
    }

    print("\nDataset with Ma encoding:")
    print(ds_ma)

    # Save to NetCDF
    output_file = "paleoclimate_ma_encoded.nc"
    ds_ma.to_netcdf(output_file)
    print(f"\n  Saved to: {output_file}")

    # Demonstrate reading back
    ds_loaded = xr.open_dataset(output_file)
    print("\nLoaded dataset from NetCDF:")
    print(f"  Time values (Ma): {ds_loaded.time.values}")

    # Decode back to PaleoDateTime
    decoded_dates = decode_paleodatetime_coord(ds_loaded.time.values, units="Ma")
    print(f"  Decoded to years: {[d.year for d in decoded_dates]}")

    ds_loaded.close()


def example_6_statistical_analysis():
    """Perform statistical analysis on paleoclimate data."""
    print("\n\nExample 6: Statistical Analysis")
    print("-" * 60)

    # Create dataset
    years = np.linspace(-100_000_000, 0, 500)
    temp = 15 + 3 * np.sin(years / 20_000_000) + np.random.randn(500) * 0.5

    ds = create_dataset_with_time({"temperature": temp}, years)

    # Calculate statistics for different periods
    cenozoic = time_slice(ds, -66_000_000, 0)
    late_cretaceous = time_slice(ds, -100_000_000, -66_000_000)

    print("\nCenozoic (0-66 Ma):")
    print(f"  Mean temperature: {float(cenozoic.temperature.mean()):.2f}°C")
    print(f"  Std deviation: {float(cenozoic.temperature.std()):.2f}°C")
    print(f"  Min: {float(cenozoic.temperature.min()):.2f}°C")
    print(f"  Max: {float(cenozoic.temperature.max()):.2f}°C")

    print("\nLate Cretaceous (66-100 Ma):")
    print(f"  Mean temperature: {float(late_cretaceous.temperature.mean()):.2f}°C")
    print(f"  Std deviation: {float(late_cretaceous.temperature.std()):.2f}°C")
    print(f"  Min: {float(late_cretaceous.temperature.min()):.2f}°C")
    print(f"  Max: {float(late_cretaceous.temperature.max()):.2f}°C")

    # Calculate long-term trend
    print("\nLong-term trend analysis:")
    print(f"  Temperature change over 100 Ma: {float(ds.temperature.values[-1] - ds.temperature.values[0]):.2f}°C")


def main():
    """Run all examples."""
    print("=" * 60)
    print("PaleoDateTime xarray Integration Examples")
    print("=" * 60)
    print()

    try:
        # Example 1: Create dataset
        ds = example_1_create_paleo_dataset()

        # Example 2: Time slicing
        example_2_time_slicing(ds)

        # Example 3: Plotting
        example_3_plotting_with_labels(ds)

        # Example 4: Mass extinctions
        example_4_mass_extinctions_analysis(ds)

        # Example 5: NetCDF encoding
        example_5_encoding_for_netcdf()

        # Example 6: Statistical analysis
        example_6_statistical_analysis()

        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("Check the generated files in the current directory.")
        print("=" * 60)

    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
