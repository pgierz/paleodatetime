"""Example: Using PaleoDateTime with matplotlib for geological time plotting."""

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

from paleodatetime import (
    PaleoDateTime,
    format_geological,
    matplotlib_ticker_formatter,
    matplotlib_ordinal_formatter,
)


def example_1_mass_extinctions_timeline():
    """Plot the Big Five mass extinctions on a timeline."""
    print("Example 1: Mass Extinctions Timeline")

    # Define mass extinctions
    extinctions = [
        ("Ordovician-Silurian", -445_000_000, 85),
        ("Late Devonian", -375_000_000, 75),
        ("Permian-Triassic", -252_000_000, 96),
        ("Triassic-Jurassic", -201_000_000, 80),
        ("K-Pg", -66_000_000, 76),
    ]

    # Extract data
    names = [e[0] for e in extinctions]
    years = [e[1] for e in extinctions]
    extinctions_pct = [e[2] for e in extinctions]

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot extinctions
    colors = plt.cm.Reds(np.linspace(0.4, 0.9, len(extinctions)))
    bars = ax.barh(range(len(names)), extinctions_pct, color=colors)

    # Format y-axis with event names
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names)

    # Format x-axis
    ax.set_xlabel("Species Extinction (%)", fontsize=12)
    ax.set_title("The Big Five Mass Extinctions", fontsize=14, fontweight="bold")

    # Add extinction dates as text labels
    for i, (name, year, pct) in enumerate(extinctions):
        dt = PaleoDateTime(year, 1, 1)
        label = dt.format_ma(precision=0)
        ax.text(pct + 1, i, f"  {label}", va="center", fontsize=10)

    ax.set_xlim(0, 105)
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()
    plt.savefig("mass_extinctions_timeline.png", dpi=150, bbox_inches="tight")
    print("  Saved: mass_extinctions_timeline.png\n")
    plt.close()


def example_2_temperature_over_time():
    """Plot temperature anomaly over geological time."""
    print("Example 2: Temperature Over Geological Time")

    # Simulated temperature data (relative to pre-industrial baseline)
    time_ma = np.array([500, 400, 300, 200, 100, 50, 20, 10, 5, 2, 1, 0.5, 0])
    temp_anomaly = np.array([2, 1, 3, 0, -1, 2, -2, -3, -1, 1, 0, 0.5, 1])

    # Convert Ma to years for plotting
    years = -time_ma * 1_000_000

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6))

    # Plot temperature
    ax.plot(years, temp_anomaly, "b-", linewidth=2, label="Temperature Anomaly")
    ax.fill_between(years, 0, temp_anomaly, alpha=0.3)
    ax.axhline(y=0, color="k", linestyle="--", alpha=0.5, linewidth=1)

    # Format x-axis with geological time
    formatter = matplotlib_ticker_formatter(precision=0)
    ax.xaxis.set_major_formatter(FuncFormatter(formatter))

    # Labels and title
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Temperature Anomaly (°C)", fontsize=12)
    ax.set_title(
        "Global Temperature Over Geological Time (Simulated Data)",
        fontsize=14,
        fontweight="bold",
    )

    # Add grid
    ax.grid(True, alpha=0.3)

    # Invert x-axis so time goes left (past) to right (present)
    ax.invert_xaxis()

    plt.tight_layout()
    plt.savefig("temperature_over_time.png", dpi=150, bbox_inches="tight")
    print("  Saved: temperature_over_time.png\n")
    plt.close()


def example_3_stratigraphic_column():
    """Plot a stratigraphic column with geological periods."""
    print("Example 3: Stratigraphic Column")

    # Geological periods (simplified)
    periods = [
        ("Quaternary", 0, 2.6, "#F9F97F"),
        ("Neogene", 2.6, 23.0, "#FFE619"),
        ("Paleogene", 23.0, 66.0, "#FD9A52"),
        ("Cretaceous", 66.0, 145.0, "#7FC64E"),
        ("Jurassic", 145.0, 201.0, "#34B2C9"),
        ("Triassic", 201.0, 252.0, "#812B92"),
        ("Permian", 252.0, 299.0, "#F04028"),
    ]

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 10))

    # Plot each period as a rectangle (using bar for vertical stacking)
    for i, (name, start_ma, end_ma, color) in enumerate(periods):
        duration = end_ma - start_ma
        ax.bar(
            0, duration, bottom=start_ma, width=1, color=color, edgecolor="black", linewidth=2
        )

        # Add period name
        mid_point = (start_ma + end_ma) / 2
        ax.text(
            0,
            mid_point,
            name,
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold",
        )

    # Format y-axis with Ma values
    formatter = matplotlib_ordinal_formatter(ascending=True)
    ax.yaxis.set_major_formatter(FuncFormatter(formatter))

    # Invert y-axis so oldest is at bottom
    ax.invert_yaxis()

    # Remove x-axis and set limits
    ax.set_xlim(-0.5, 0.5)
    ax.set_xticks([])

    # Labels and title
    ax.set_ylabel("Age", fontsize=12)
    ax.set_title("Geological Time Scale (Simplified)", fontsize=14, fontweight="bold")

    # Set y-axis limits
    ax.set_ylim(0, max(end for _, _, end, _ in periods) * 1.05)

    plt.tight_layout()
    plt.savefig("stratigraphic_column.png", dpi=150, bbox_inches="tight")
    print("  Saved: stratigraphic_column.png\n")
    plt.close()


def example_4_climate_cycles():
    """Plot ice age cycles over the past 800,000 years."""
    print("Example 4: Ice Age Cycles")

    # Simulated ice volume data
    years_ago = np.linspace(-800_000, 0, 1000)
    # Simulate glacial-interglacial cycles (roughly 100ka periodicity)
    ice_volume = 50 + 30 * np.sin(2 * np.pi * years_ago / 100_000) + 10 * np.random.randn(
        1000
    )

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6))

    # Plot ice volume
    ax.plot(years_ago, ice_volume, "b-", linewidth=1.5, alpha=0.7)
    ax.fill_between(years_ago, ice_volume.min(), ice_volume, alpha=0.3, color="lightblue")

    # Mark glacial maxima
    glacial_periods = [-20_000, -140_000, -260_000, -380_000, -500_000, -620_000, -740_000]
    for gp in glacial_periods:
        ax.axvline(x=gp, color="gray", linestyle="--", alpha=0.3)

    # Format x-axis with ka values
    formatter = matplotlib_ticker_formatter(precision=0)
    ax.xaxis.set_major_formatter(FuncFormatter(formatter))

    # Labels and title
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Ice Volume (arbitrary units)", fontsize=12)
    ax.set_title(
        "Glacial-Interglacial Cycles (Simulated Data)", fontsize=14, fontweight="bold"
    )

    # Add grid
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("ice_age_cycles.png", dpi=150, bbox_inches="tight")
    print("  Saved: ice_age_cycles.png\n")
    plt.close()


def example_5_multiple_timescales():
    """Demonstrate different formatting on different subplots."""
    print("Example 5: Multiple Timescales")

    fig, axes = plt.subplots(3, 1, figsize=(12, 10))

    # Subplot 1: Deep time (hundreds of millions of years)
    ax1 = axes[0]
    years_1 = np.array([-500_000_000, -400_000_000, -300_000_000, -200_000_000, -100_000_000])
    values_1 = np.array([20, 22, 18, 21, 19])
    ax1.plot(years_1, values_1, "o-", linewidth=2, markersize=8)
    ax1.xaxis.set_major_formatter(FuncFormatter(matplotlib_ticker_formatter(precision=0)))
    ax1.set_ylabel("Biodiversity Index", fontsize=10)
    ax1.set_title("Deep Time (Phanerozoic Eon)", fontsize=12, fontweight="bold")
    ax1.grid(True, alpha=0.3)
    ax1.invert_xaxis()

    # Subplot 2: Quaternary period (millions of years)
    ax2 = axes[1]
    years_2 = np.array([-2_600_000, -2_000_000, -1_500_000, -1_000_000, -500_000])
    values_2 = np.array([15, 17, 16, 18, 17])
    ax2.plot(years_2, values_2, "s-", linewidth=2, markersize=8, color="orange")
    ax2.xaxis.set_major_formatter(FuncFormatter(matplotlib_ticker_formatter(precision=1)))
    ax2.set_ylabel("Sea Level (m)", fontsize=10)
    ax2.set_title("Quaternary Period", fontsize=12, fontweight="bold")
    ax2.grid(True, alpha=0.3)
    ax2.invert_xaxis()

    # Subplot 3: Recent history (thousands of years)
    ax3 = axes[2]
    years_3 = np.array([-50_000, -40_000, -30_000, -20_000, -10_000])
    values_3 = np.array([100, 200, 500, 1000, 5000])
    ax3.plot(years_3, values_3, "^-", linewidth=2, markersize=8, color="green")
    ax3.xaxis.set_major_formatter(FuncFormatter(matplotlib_ticker_formatter(precision=0)))
    ax3.set_ylabel("Population (thousands)", fontsize=10)
    ax3.set_xlabel("Time", fontsize=11)
    ax3.set_title("Late Pleistocene to Holocene", fontsize=12, fontweight="bold")
    ax3.grid(True, alpha=0.3)
    ax3.invert_xaxis()

    plt.tight_layout()
    plt.savefig("multiple_timescales.png", dpi=150, bbox_inches="tight")
    print("  Saved: multiple_timescales.png\n")
    plt.close()


def main():
    """Run all examples."""
    print("=" * 60)
    print("PaleoDateTime Matplotlib Examples")
    print("=" * 60)
    print()

    try:
        example_1_mass_extinctions_timeline()
        example_2_temperature_over_time()
        example_3_stratigraphic_column()
        example_4_climate_cycles()
        example_5_multiple_timescales()

        print("=" * 60)
        print("All examples completed successfully!")
        print("Check the generated PNG files in the current directory.")
        print("=" * 60)

    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
