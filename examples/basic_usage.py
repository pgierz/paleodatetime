"""Basic usage examples for paleodatetime library."""

from paleodatetime import PaleoDateTime, PaleoTimeDelta


def main():
    print("=== PaleoDateTime: Basic Usage Examples ===\n")

    # Example 1: Creating dates
    print("1. Creating dates:")
    kt_extinction = PaleoDateTime(-66_000_000, 1, 1)
    print(f"   K-Pg extinction event: {kt_extinction}")

    present = PaleoDateTime(2024, 1, 15, 12, 30, 0)
    print(f"   Present day: {present}")

    # Example 2: Date arithmetic
    print("\n2. Date arithmetic:")
    one_million_years = PaleoTimeDelta(years=1_000_000)
    future_date = kt_extinction + one_million_years
    print(f"   One million years after K-Pg: {future_date}")

    # Example 3: Time differences
    print("\n3. Calculating time differences:")
    pt_extinction = PaleoDateTime(-252_000_000, 1, 1)
    time_between = kt_extinction - pt_extinction
    print(f"   Time between P-T and K-Pg extinctions:")
    print(f"   {time_between.years:,} years ({time_between.years / 1_000_000:.1f} Ma)")

    # Example 4: Comparisons
    print("\n4. Comparing dates:")
    if pt_extinction < kt_extinction:
        print("   P-T extinction is older than K-Pg (as expected)")

    # Example 5: Formatting
    print("\n5. Formatting dates:")
    cambrian = PaleoDateTime(-541_000_000, 1, 1)
    print(f"   ISO format: {cambrian.isoformat()}")
    print(f"   String: {str(cambrian)}")

    # Example 6: Parsing
    print("\n6. Parsing dates:")
    date_string = "-66000000-01-01T00:00:00"
    parsed = PaleoDateTime.fromisoformat(date_string)
    print(f"   Parsed '{date_string}' -> {parsed.year}")

    # Example 7: Replace fields
    print("\n7. Replacing date fields:")
    original = PaleoDateTime(-100_000_000, 6, 15)
    modified = original.replace(month=12, day=25)
    print(f"   Original: {original}")
    print(f"   Modified: {modified}")

    # Example 8: Working with timedeltas
    print("\n8. Working with time deltas:")
    td1 = PaleoTimeDelta(years=1_000_000, days=100)
    td2 = PaleoTimeDelta(years=500_000, days=50)
    td_sum = td1 + td2
    print(f"   Delta 1: {td1.years:,} years, {td1.days} days")
    print(f"   Delta 2: {td2.years:,} years, {td2.days} days")
    print(f"   Sum: {td_sum.years:,} years")

    # Example 9: Timeline of life
    print("\n9. Timeline of major events:")
    events = [
        ("Earth formation", PaleoDateTime(-4_540_000_000, 1, 1)),
        ("First life", PaleoDateTime(-3_800_000_000, 1, 1)),
        ("Cambrian explosion", PaleoDateTime(-541_000_000, 1, 1)),
        ("First land plants", PaleoDateTime(-470_000_000, 1, 1)),
        ("First dinosaurs", PaleoDateTime(-230_000_000, 1, 1)),
        ("K-Pg extinction", kt_extinction),
        ("First humans", PaleoDateTime(-300_000, 1, 1)),
    ]

    now = PaleoDateTime.now()
    print(f"   Current date: {now}\n")

    for name, date in events:
        time_ago = now - date
        ma = time_ago.years / 1_000_000
        print(f"   {name:20} {ma:>10,.1f} Ma ago")


if __name__ == "__main__":
    main()
