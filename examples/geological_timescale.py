"""Example: Working with geological timescales and extinction events."""

from paleodatetime import PaleoDateTime, PaleoTimeDelta


def main():
    print("=== Geological Timescale: The Big Five Mass Extinctions ===\n")

    # Define the Big Five mass extinctions
    extinctions = [
        ("Ordovician-Silurian", -445_000_000, "~85% of species"),
        ("Late Devonian", -375_000_000, "~75% of species"),
        ("Permian-Triassic", -252_000_000, "~96% of species (The Great Dying)"),
        ("Triassic-Jurassic", -201_000_000, "~80% of species"),
        ("Cretaceous-Paleogene", -66_000_000, "~76% of species (dinosaurs)"),
    ]

    # Create PaleoDateTime objects
    extinction_dates = []
    for name, year, impact in extinctions:
        dt = PaleoDateTime(year, 1, 1)
        extinction_dates.append((name, dt, impact))

    # Display extinctions
    print("The Big Five Mass Extinctions:\n")
    for name, date, impact in extinction_dates:
        ma = abs(date.year) / 1_000_000
        print(f"{name:25} {ma:>6.1f} Ma   {impact}")

    # Calculate intervals between extinctions
    print("\n\nTime Intervals Between Extinctions:\n")
    for i in range(len(extinction_dates) - 1):
        name1, date1, _ = extinction_dates[i]
        name2, date2, _ = extinction_dates[i + 1]

        interval = date2 - date1
        my = interval.years / 1_000_000

        print(f"{name1:25} -> {name2:25}: {my:>6.1f} My")

    # Calculate time since K-Pg extinction
    print("\n\nTime Since K-Pg Extinction (End of Dinosaurs):\n")
    kt_date = extinction_dates[-1][1]
    present = PaleoDateTime.now()
    time_since = present - kt_date
    my = time_since.years / 1_000_000

    print(f"K-Pg extinction occurred {my:.2f} million years ago")
    print(f"That's {time_since.years:,} years")

    # Simulate future events
    print("\n\nProjecting Into The Future:\n")
    future_projections = [
        ("Next 1,000 years", PaleoTimeDelta(years=1_000)),
        ("Next 100,000 years", PaleoTimeDelta(years=100_000)),
        ("Next 1 million years", PaleoTimeDelta(years=1_000_000)),
        ("Next 10 million years", PaleoTimeDelta(years=10_000_000)),
    ]

    for name, delta in future_projections:
        future_date = present + delta
        print(f"{name:25}: Year {future_date.year:,}")

    # Compare to Earth's age
    print("\n\nEarth's History:\n")
    earth_formation = PaleoDateTime(-4_540_000_000, 1, 1)
    earth_age = present - earth_formation
    earth_age_my = earth_age.years / 1_000_000

    print(f"Earth formed: ~{earth_age_my:.1f} Ma ago")

    # Calculate what percentage of Earth's history each extinction represents
    print("\n\nExtinctions as Percentage of Earth's History:\n")
    for name, date, _ in extinction_dates:
        time_from_formation = date - earth_formation
        percentage = (time_from_formation.years / earth_age.years) * 100
        print(f"{name:25}: {percentage:>5.1f}% through Earth's history")

    # Mesozoic Era (Age of Dinosaurs)
    print("\n\nThe Mesozoic Era (Age of Dinosaurs):\n")
    mesozoic_start = PaleoDateTime(-252_000_000, 1, 1)  # Start of Triassic
    mesozoic_end = PaleoDateTime(-66_000_000, 1, 1)  # End of Cretaceous

    mesozoic_duration = mesozoic_end - mesozoic_start
    mesozoic_my = mesozoic_duration.years / 1_000_000

    print(f"Start (Triassic): {abs(mesozoic_start.year) / 1_000_000:.1f} Ma")
    print(f"End (K-Pg): {abs(mesozoic_end.year) / 1_000_000:.1f} Ma")
    print(f"Duration: {mesozoic_my:.1f} million years")

    # Compare to mammal dominance
    mammal_dominance = present - mesozoic_end
    mammal_my = mammal_dominance.years / 1_000_000

    print(f"\nMammals have dominated for: {mammal_my:.2f} million years")
    print(f"Dinosaurs dominated for: {mesozoic_my:.1f} million years")

    ratio = mesozoic_my / mammal_my
    print(f"Dinosaurs reigned {ratio:.1f}x longer than mammals (so far)")


if __name__ == "__main__":
    main()
