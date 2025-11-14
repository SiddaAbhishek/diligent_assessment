import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker


NUM_USERS = 50
NUM_PRODUCTS = 30
NUM_ORDERS = 60
CURRENCY_PRECISION = 2

faker = Faker()
ROOT = Path(__file__).resolve().parent


def random_price(min_price: float = 10.0, max_price: float = 500.0) -> float:
    return round(random.uniform(min_price, max_price), CURRENCY_PRECISION)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]):
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_users() -> list[dict]:
    users = []
    for user_id in range(1, NUM_USERS + 1):
        name = faker.name()
        email = faker.email()
        users.append({
            "user_id": user_id,
            "name": name,
            "email": email,
        })
    return users


def generate_products() -> tuple[list[dict], dict[int, float]]:
    categories = [
        "Electronics",
        "Home",
        "Beauty",
        "Sports",
        "Toys",
        "Outdoors",
        "Fashion",
    ]
    descriptors = ["Pro", "Plus", "Lite", "Max", "Mini", "Prime"]

    products = []
    price_lookup: dict[int, float] = {}
    for product_id in range(1, NUM_PRODUCTS + 1):
        name = f"{faker.word().title()} {random.choice(descriptors)}"
        category = random.choice(categories)
        price = random_price()
        products.append({
            "product_id": product_id,
            "name": name,
            "category": category,
            "price": f"{price:.2f}",
        })
        price_lookup[product_id] = price
    return products, price_lookup


def generate_orders() -> list[dict]:
    orders = []
    now = datetime.now()
    for order_id in range(1, NUM_ORDERS + 1):
        user_id = random.randint(1, NUM_USERS)
        order_date = faker.date_time_between(start_date=now - timedelta(days=365), end_date=now)
        orders.append({
            "order_id": order_id,
            "user_id": user_id,
            "order_date": order_date.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return orders


def generate_order_items(orders: list[dict], price_lookup: dict[int, float]) -> tuple[list[dict], dict[int, float]]:
    order_totals: dict[int, float] = {int(order["order_id"]): 0.0 for order in orders}
    items: list[dict] = []
    item_id = 1

    for order in orders:
        num_items = random.randint(1, 5)
        order_id = int(order["order_id"])
        for _ in range(num_items):
            product_id = random.randint(1, NUM_PRODUCTS)
            quantity = random.randint(1, 4)
            line_total = price_lookup[product_id] * quantity
            order_totals[order_id] += line_total

            items.append({
                "item_id": item_id,
                "order_id": order_id,
                "product_id": product_id,
                "quantity": quantity,
            })
            item_id += 1

    return items, order_totals


def generate_payments(order_totals: dict[int, float]) -> list[dict]:
    statuses = ["paid", "pending", "failed"]
    payments = []
    payment_id = 1
    for order_id, total in order_totals.items():
        status = random.choices(statuses, weights=[0.8, 0.15, 0.05], k=1)[0]
        amount = round(total, CURRENCY_PRECISION)
        payments.append({
            "payment_id": payment_id,
            "order_id": order_id,
            "amount": f"{amount:.2f}",
            "status": status,
        })
        payment_id += 1
    return payments


def main() -> None:
    users = generate_users()
    products, price_lookup = generate_products()
    orders = generate_orders()
    order_items, order_totals = generate_order_items(orders, price_lookup)
    payments = generate_payments(order_totals)

    write_csv(ROOT / "users.csv", ["user_id", "name", "email"], users)
    write_csv(ROOT / "products.csv", ["product_id", "name", "category", "price"], products)
    write_csv(ROOT / "orders.csv", ["order_id", "user_id", "order_date"], orders)
    write_csv(ROOT / "order_items.csv", ["item_id", "order_id", "product_id", "quantity"], order_items)
    write_csv(ROOT / "payments.csv", ["payment_id", "order_id", "amount", "status"], payments)

    print("Synthetic e-commerce data generated successfully.")


if __name__ == "__main__":
    main()
