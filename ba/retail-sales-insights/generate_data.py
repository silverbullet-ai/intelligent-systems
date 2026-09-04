"""
generate_data.py
-----------------
Creates a synthetic but realistic retail transactions dataset for the
Retail Sales Performance & Business Insights project.

Produces three CSVs in ./data:
    customers.csv  - customer_id, signup_date, region, segment
    products.csv   - product_id, category, unit_cost, unit_price
    orders.csv     - order_id, customer_id, product_id, order_date, quantity

Run: python generate_data.py
"""

import csv
import os
import random
from datetime import date, timedelta

random.seed(42)

OUT_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUT_DIR, exist_ok=True)

REGIONS = ["North", "South", "East", "West"]
SEGMENTS = ["Consumer", "Corporate", "Small Business"]
CATEGORIES = {
    "Electronics": (40, 120),
    "Home & Kitchen": (15, 60),
    "Apparel": (10, 45),
    "Office Supplies": (5, 25),
    "Sports & Outdoors": (20, 80),
}

N_CUSTOMERS = 300
N_PRODUCTS = 60
N_ORDERS = 4000

START_DATE = date(2025, 1, 1)
END_DATE = date(2026, 8, 31)


def random_date(start: date, end: date) -> date:
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))


def build_customers():
    rows = []
    for cid in range(1, N_CUSTOMERS + 1):
        rows.append(
            {
                "customer_id": cid,
                "signup_date": random_date(START_DATE, END_DATE).isoformat(),
                "region": random.choice(REGIONS),
                "segment": random.choice(SEGMENTS),
            }
        )
    return rows


def build_products():
    rows = []
    for pid in range(1, N_PRODUCTS + 1):
        category = random.choice(list(CATEGORIES.keys()))
        low, high = CATEGORIES[category]
        unit_cost = round(random.uniform(low, high) * 0.6, 2)
        unit_price = round(unit_cost * random.uniform(1.3, 2.2), 2)
        rows.append(
            {
                "product_id": pid,
                "category": category,
                "unit_cost": unit_cost,
                "unit_price": unit_price,
            }
        )
    return rows


def build_orders(customers, products):
    rows = []
    for oid in range(1, N_ORDERS + 1):
        customer = random.choice(customers)
        product = random.choice(products)
        signup = date.fromisoformat(customer["signup_date"])
        order_date = random_date(max(signup, START_DATE), END_DATE)
        rows.append(
            {
                "order_id": oid,
                "customer_id": customer["customer_id"],
                "product_id": product["product_id"],
                "order_date": order_date.isoformat(),
                "quantity": random.randint(1, 5),
            }
        )
    return rows


def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    customers = build_customers()
    products = build_products()
    orders = build_orders(customers, products)

    write_csv(os.path.join(OUT_DIR, "customers.csv"), customers,
              ["customer_id", "signup_date", "region", "segment"])
    write_csv(os.path.join(OUT_DIR, "products.csv"), products,
              ["product_id", "category", "unit_cost", "unit_price"])
    write_csv(os.path.join(OUT_DIR, "orders.csv"), orders,
              ["order_id", "customer_id", "product_id", "order_date", "quantity"])

    print(f"Generated {len(customers)} customers, {len(products)} products, "
          f"{len(orders)} orders in {OUT_DIR}")


if __name__ == "__main__":
    main()
