"""
Day 2 - Sales Analytics Without Pandas
Squad Python Specialization - Data Science, AI & Analytics
Tasks 1-7 use only the standard library. pandas is allowed in task 8, to check your work.
"""
import csv
from pathlib import Path
import pandas as pd
import math

DATA_PATH = Path("data") / "electronics_sales.csv"


def read_sales(path: Path = DATA_PATH) -> list[dict[str, str]]:
    """Read the CSV with the csv module and return the raw rows."""
    with open(path, mode='r',newline='', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = list(csv_reader)
        header = csv_reader.fieldnames

        # print(f"Number of rows: {len(rows)}")
        # print(f"Column names: {header}")
        # print(rows)

        return rows

    
# sales = read_sales()
# for row in sales:
#     print(
#         row["sale_id"],
#         "| Quantity:", repr(row["quantity"]),
#         "| Unit price:", repr(row["unit_price_kes"])
#     )


def parse_number(value: str) -> float | None:
    """Convert a messy numeric string to a float, or return None if it cannot be trusted."""
        # Step 1: handle missing values
    if value is None:
        return None
    
    cleaned = value.strip()

    if not cleaned or cleaned.upper() == "N/A":
        return None
    
    # convert the 'two" to numeric 2
    if cleaned.lower() == "two":
        return 2.0
    
    # replace comma separator in thousands to empty,remove prefix and whitespaces
    cleaned = cleaned.upper().removeprefix("KES").strip().replace(",", "")

    # convert the cleaned value to float
    try:
        return float(cleaned)
    except ValueError:
        return None

    
# Test parse_number() using the actual sales data
# print("\n--- Testing parse_number() with actual data ---")
# for row in sales:
#     quantity = row["quantity"]
#     price = row["unit_price_kes"]
#     parsed_quantity = parse_number(quantity)
#     parsed_price = parse_number(price)
#     if (
#         quantity.strip().lower() == "two"
#         or "," in price
#         or "KES" in price.upper()
#         or not price.strip()
#         or price.strip().upper() == "N/A"
#         or not quantity.strip()
#     ):
#         print(
#             f"{row['sale_id']} | "
#             f"Quantity: {quantity!r} -> {parsed_quantity} | "
#             f"Price: {price!r} -> {parsed_price}"
#         )


def convert_rows(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict]]:
    """Return (clean_rows, skipped_rows). Clean rows have numeric quantity, unit price and revenue."""
    # create empty list for valid and invalid sales
    clean_rows = []
    skipped_rows = []

    # loop through the raw rows and convert price and quantity columns using parce_number()
    for row in rows:
        quantity = parse_number(row["quantity"])
        price = parse_number(row["unit_price_kes"])

        # handle skipped rows
        if quantity is None or price is None:
            reasons = []

            if quantity is None:
                reasons.append("Missing Quantity")

            if price is None:
                reasons.append("Missing Price")

            skipped_rows.append({
                **row,
                "reason": " and ".join(reasons)
            })

            continue

        revenue = price * quantity

        clean_row = {
            **row,
            "quantity": quantity,
            "unit_price_kes": price,
            "revenue": revenue
        }

        clean_rows.append(clean_row)

    return clean_rows, skipped_rows


# sales = read_sales()
# clean_rows, skipped_rows = convert_rows(sales)
# print("\n--- Conversion Results ---")
# print(f"Rows read: {len(sales)}")
# print(f"Rows used: {len(clean_rows)}")
# print(f"Rows skipped: {len(skipped_rows)}")
# for row in skipped_rows:
#     print(row["sale_id"], "-", row["reason"])


def total_revenue(rows: list[dict]) -> float:
    # calculate total revenue
    total = 0

    for row in rows:
        total += row["revenue"]

    return total


# sales = read_sales()
# clean_rows, skipped_rows = convert_rows(sales)
# revenue = total_revenue(clean_rows)
# print(f"\nTotal revenue: KES {revenue:,.2f}")


def revenue_by(rows: list[dict], field: str) -> dict[str, float]:
    """Total revenue grouped by any column (product, store, payment_method...)."""
    totals = {}

    for row in rows:
        category = row[field]
        revenue = row["revenue"]

        if category in totals:
            totals[category] += revenue

        else:
            totals[category] = revenue

    return totals

# sales = read_sales()
# clean_rows, skipped_rows = convert_rows(sales)
# for field in ["product", "store", "payment_method"]:
#     totals = revenue_by(clean_rows, field)
#     print(f"\nRevenue by {field.replace('_', ' ')}:")
#     for name, amount in sorted(
#         totals.items(), key=lambda item: item[1], reverse=True
#     ):
#         print(f"{name}: KES {amount:,.2f}")


def top_n(totals: dict[str, float], n: int = 3) -> list[tuple[str, float]]:
    """Return the n highest (key, value) pairs, highest first."""
    # implement top_n() first
    ranked = sorted(
        totals.items(),
        key=lambda item: (-item[1], item[0])
    )

    return ranked[:n]


sales = read_sales()
clean_rows, skipped_rows = convert_rows(sales)
# product_totals = revenue_by(clean_rows, "product")
# top_products = top_n(product_totals, 3)
# print("\nTop 3 products:")
# for rank, (product, revenue) in enumerate(top_products, start=1):
#     print(f"{rank}. {product} - KES {revenue:,.2f}")


def high_value(rows: list[dict], threshold: float) -> list[dict]:
    """Transactions whose revenue is at or above threshold (use a comprehension)."""
    return [row for row in rows if row["revenue"] >= threshold]

high_value_sales = high_value(clean_rows, 50000)
# print("\nHigh-value transactions (>= KES 50,000):")
# print(f"Number of qualifying sales: {len(high_value_sales)}")
# for row in high_value_sales:
#     print(
#         f"{row['sale_id']} | {row['sale_date']} | "
#         f"{row['store']} | {row['product']} | "
#         f"KES {row['revenue']:,.2f}"
#     )
stores = {row["store"] for row in high_value_sales}
high_value_by_store = {
    store: sum(1 for row in high_value_sales if row["store"] == store)
    for store in stores
}

# print("\nHigh-value transactions by store:")
# for store, count in sorted(high_value_by_store.items()):
#     print(f"{store}: {count}")
# # Reusable statistics - implement these yourself, no statistics module.


def mean(values: list[float]) -> float:
    # check if values is a list  or just a value
    if not values:
        raise ValueError("Cannot calculate mean of an empty list")
    
    total = 0.0

    # mean = sum of values/number of values
    for value in values:
        total += value

    return total/len(values)


def median(values: list[float]) -> float:
    # check the number of values
    if not values:
        raise ValueError("Cannot calculate median of an empty list")
    
    ordered = sorted(values)
    middle = len(ordered) // 2

    if len(ordered) % 2 == 1:
        return ordered[middle]
    
    return (ordered[middle - 1] + ordered[middle]) / 2


def minimum_maximum(values: list[float]) -> tuple[float, float]:
    if not values:
            raise ValueError("Cannot calculate minimum and maximum of an empty list")
    
    smallest = values[0]
    largest = values[0]

    for value in values[1:]:
        if value < smallest:
            smallest = value

        if value > largest:
            largest = value

    return smallest, largest

revenues = [row["revenue"] for row in clean_rows]

smallest, largest = minimum_maximum(revenues)

my_results = {
    "valid_rows": len(clean_rows),
    "skipped_rows": len(skipped_rows),
    "total_revenue": total_revenue(clean_rows),
    "revenue_by_product": revenue_by(clean_rows, "product"),
    "revenue_by_store": revenue_by(clean_rows, "store"),
    "revenue_by_payment": revenue_by(clean_rows, "payment_method"),
    "high_value_count": len(high_value(clean_rows, 50000)),
    "mean": mean(revenues),
    "median": median(revenues),
    "minimum": smallest,
    "maximum": largest
}


def verify_with_pandas(path: Path, my_results: dict) -> None:
    """Recompute the headline numbers with pandas and print whether each one matches."""
    # 1. Read csv file
    df = pd.read_csv(path, dtype=str, keep_default_na=False)

    # 2. Apply the same cleaning rules as parse_number()
    df['quantity'] = df["quantity"].apply(parse_number)
    df['unit_price_kes'] = df["unit_price_kes"].apply(parse_number)

    # 3. Separate valid and skipped records
    valid = df.dropna(subset=['quantity', 'unit_price_kes']).copy()
    skipped_count = len(df) - len(valid)

    # 4. Calculate revenue using pandas
    valid['revenue'] = valid['quantity'] * valid['unit_price_kes']
    revenues = valid['revenue']

    # 5. Recalculate the headline results
    pandas_results = {
    "total_revenue": revenues.sum(),
    "valid_rows": len(valid),
    "skipped_rows": skipped_count,
    "revenue_by_product": valid.groupby("product")["revenue"].sum().to_dict(),
    "revenue_by_store": valid.groupby("store")["revenue"].sum().to_dict(),
    "revenue_by_payment": valid.groupby("payment_method")["revenue"].sum().to_dict(),
    "high_value_count": int((revenues >= 50000).sum()),
    "mean": revenues.mean(),
    "median": revenues.median(),
    "minimum": revenues.min(),
    "maximum": revenues.max()
}
    
    # 6. Compare pandas results with the standard-library results
    print("\n--- Pandas Verification ---")

    # Compare the results
    for name, expected in my_results.items():
        actual = pandas_results[name]

        # Comparing dictionaries
        if isinstance(expected, dict):
            matches = (
                expected.keys() == actual.keys()
                and all(
                    math.isclose(expected[key], actual[key], rel_tol=1e-9, abs_tol=0.01)
                    for key in expected
                )
            )

        # Comparing numeric values
        elif isinstance(expected, (int, float)):
            matches = math.isclose(
                expected, actual, rel_tol=1e-9, abs_tol=0.01
            )

        else:
            matches = expected == actual

        # Print the outcome
        status = "MATCH" if matches else "MISMATCH"
        print(f"{name}: {status}")
        if not matches:
            print(f"  Standard library: {expected}")
            print(f"  Pandas:           {actual}")


if __name__ == "__main__":
    # 1. Read and clean the sales data
    sales = read_sales()
    clean_rows, skipped_rows = convert_rows(sales)

    # 2. Calculate headline figures
    revenues = [row["revenue"] for row in clean_rows]
    total = total_revenue(clean_rows)
    product_totals = revenue_by(clean_rows, "product")
    top_products = top_n(product_totals, 3)
    threshold = 50000
    high_value_sales = high_value(clean_rows, threshold)
    smallest, largest = minimum_maximum(revenues)
    average = mean(revenues)
    middle_value = median(revenues)

    # 3. Build the report
    report = []

    report.append("=== Sales report: September 2026 ===")
    report.append(f"Rows read          : {len(sales)}")
    report.append(f"Rows used          : {len(clean_rows)}")

    skipped_details = ", ".join(
        f"{row['sale_id']}: {row['reason']}"
        for row in skipped_rows
    )
    report.append(
        f"Rows skipped       : {len(skipped_rows)}   ({skipped_details})"
    )
    report.append("")
    report.append(f"Total revenue (KES): {total:,.2f}")
    # Revenue by product, sorted from highest to lowest
    report.append("")
    report.append("Revenue by product (KES)")

    for product, amount in sorted(
        product_totals.items(),
        key=lambda item: (-item[1], item[0])
    ):
        report.append(f"  {product:<25} {amount:,.2f}")

    # Top three products
    report.append("")
    report.append("Top 3 products")
    for rank, (product, amount) in enumerate(top_products, start=1):
        report.append(f"  {rank}. {product} - KES {amount:,.2f}")

    # High-value transactions
    report.append("")
    report.append(
        f"High-value transactions (>= KES {threshold:,}): "
        f"{len(high_value_sales)}"
    )

    for row in high_value_sales:
        report.append(
            f"  {row['sale_id']}  {row['sale_date']}  "
            f"{row['store']}  {row['product']}  "
            f"KES {row['revenue']:,.2f}"
        )

    # Transaction revenue statistics
    report.append("")
    report.append("Transaction revenue statistics")
    report.append(f"  mean   : {average:,.2f}")
    report.append(f"  median : {middle_value:,.2f}")
    report.append(f"  min    : {smallest:,.2f}")
    report.append(f"  max    : {largest:,.2f}")

    # 4. Save and display the report
    output_path = Path("output") / "sales_report.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_text = "\n".join(report) + "\n"
    output_path.write_text(report_text, encoding="utf-8")
    print(report_text)
    print(f"Report saved to {output_path}")
    
    # 5. Verify the headline calculations with pandas
    my_results = {
        "total_revenue": total,
        "valid_rows": len(clean_rows),
        "skipped_rows": len(skipped_rows),
        "revenue_by_product": product_totals,
        "revenue_by_store": revenue_by(clean_rows, "store"),
        "revenue_by_payment": revenue_by(clean_rows, "payment_method"),
        "high_value_count": len(high_value_sales),
        "mean": average,
        "median": middle_value,
        "minimum": smallest,
        "maximum": largest,
    }

    verify_with_pandas(DATA_PATH, my_results)