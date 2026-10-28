# Day 2: Sales Analytics Without Pandas

**Squad Python Specialization – Data Science, AI & Analytics**

## 1. Project Overview

This project analyzes electronics sales data for September 2026 using Python. The objective is to clean numeric data, calculate revenue, identify top-performing products, filter high-value transactions, calculate descriptive statistics, and verify the results using pandas.

Tasks 1–7 use Python's standard library. Pandas is used in Task 8 only to independently verify the calculations.

## 2. Dataset

The project uses `electronics_sales.csv`, located in the `data/` directory.

The dataset contains the following columns:

- `sale_id` – Unique identifier for each transaction.
- `sale_date` – Date of the sale.
- `store` – Store where the transaction occurred.
- `product` – Product sold.
- `quantity` – Number of units sold.
- `unit_price_kes` – Unit price in Kenyan shillings.
- `payment_method` – Payment method used.

## 3. Data Cleaning and Assumptions

The dataset contains inconsistent numeric values that must be cleaned before calculating revenue.

### Cleaning rules

| Input | Cleaning rule | Reason |
|---|---|---|
| `two` | Convert to `2.0` | The intended quantity is clear. |
| `38,999` | Remove the comma and convert to `38999.0` | The comma is a thousands separator. |
| `KES 18999` | Remove the currency prefix and convert to `18999.0` | The currency label is not part of the numeric value. |
| Empty values and `N/A` | Treat as missing (`None`) | A reliable numeric value is unavailable. |
| Other unrecognized numeric values | Treat as invalid | Guessing a value could distort the results. |

### Assumptions

- Revenue is calculated as quantity multiplied by unit price.
- Recognizable numeric formats are repaired only when their intended values are clear.
- Transactions with missing or invalid quantities or unit prices are excluded from revenue calculations.
- Skipped transactions are recorded with their sale IDs and reasons.
- Revenue calculations use valid transactions only.
- High-value transactions include revenue equal to or greater than KES 50,000.
- Revenue values are displayed in Kenyan shillings (KES), with two decimal places and thousands separators.

The `parse_number(value)` function handles numeric conversion, while `convert_rows(rows)` separates valid transactions into `clean_rows` and invalid transactions into `skipped_rows`.

## 4. Approach and Functions

### Reading and cleaning data

- `read_sales()` reads the CSV dataset.
- `parse_number(value)` converts recognizable numeric values and handles missing or invalid inputs.
- `convert_rows(rows)` validates the quantity and unit price, calculates transaction revenue, and records skipped transactions.

### Calculating total revenue

- `total_revenue(rows)` adds the revenue from all valid transactions.

### Grouping revenue

- `revenue_by(rows, field)` uses a plain dictionary to aggregate revenue by product, store, or payment method.
- Product revenue is sorted from highest to lowest.

### Identifying top products

- `top_n(totals, n)` uses `sorted()` with a key function to return the top `n` products as `(product, revenue)` tuples.
- Ties are broken alphabetically by product name.

### Filtering high-value transactions

- `high_value(rows, threshold)` uses a list comprehension to select transactions meeting the specified revenue threshold.
- A dictionary comprehension counts qualifying transactions for each store.

### Calculating statistics

The following functions operate on per-transaction revenue:

- `mean(values)` calculates the arithmetic average.
- `median(values)` calculates the middle value after sorting, or averages the two middle values when the number of observations is even.
- `minimum_maximum(values)` manually finds the smallest and largest values without using the built-in `min()` or `max()` functions.

Each statistical function raises a `ValueError` when given an empty list.

### Verifying results

`verify_with_pandas(path, my_results)` independently recalculates the headline results using pandas and compares them with the standard-library calculations.

The verification checks total revenue, revenue by product, the top three products, and mean and median transaction revenue.

## 5. Results

The analysis processed 50 rows, retained 47 valid transactions, and skipped 3 invalid transactions.

### Skipped transactions

| Sale ID | Reason |
|---|---|
| S-3030 | Missing Price |
| S-3035 | Missing Quantity |
| S-3039 | Missing Price |

### Total revenue

**KES 1,317,210.00**

### Top three products by revenue

| Rank | Product | Revenue (KES) |
|---:|---|---:|
| 1 | HP 15 Laptop | 389,994.00 |
| 2 | Hisense 43in Smart TV | 272,993.00 |
| 3 | Lenovo Tab M10 | 199,992.00 |

### Revenue statistics

| Statistic | Value (KES) |
|---|---:|
| Mean | 28,025.74 |
| Median | 10,998.00 |
| Minimum | 1,499.00 |
| Maximum | 259,996.00 |

### High-value transactions

Using a threshold of **KES 50,000**, the analysis identified **5 qualifying transactions**. The script also reports the number of qualifying transactions for each store.

## 6. Pandas Verification Results

All four verification checks returned `MATCH`:

- Total revenue: `MATCH`
- Revenue by product: `MATCH`
- Top three products: `MATCH`
- Mean and median: `MATCH`

The matching results confirm that the standard-library calculations agree with the independent pandas calculations for all four checks.

## 7. How to Run the Project

### Requirements

- Python 3 installed.
- The project files, including `sales_analysis.py` and `data/electronics_sales.csv`.
- pandas installed for Task 8 verification.

### Project structure

```text
sales-analytics-without-pandas/
├── sales_analysis.py
├── README.md
├── expected_report.txt
└── data/
    └── electronics_sales.csv
```

### Execution

1. Open a terminal in the project directory.
2. Install pandas if it is not already installed:

   ```bash
   python -m pip install pandas
   ```

3. Run the script:

   ```bash
   python sales_analysis.py
   ```

4. Review the printed sales report, skipped transactions, revenue breakdowns, high-value sales, statistical summaries, and pandas verification results.

**Note:** Tasks 1–7 use Python's standard library; pandas is required only for the final verification task.

## 8. Conclusion

This project demonstrates how Python's built-in data structures, functions, comprehensions, sorting, and basic arithmetic can be used to perform sales analysis without relying on pandas for the main calculations. Explicit cleaning rules and skipped-row reasons improve data quality, while pandas verification provides an independent check of the results.