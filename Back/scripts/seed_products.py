import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from app.database.session import SessionLocal
from app.models.models import Product


def seed_products():
    with open("scripts/products.json", "r") as file:
        products = json.load(file)

    db = SessionLocal()

    for product_data in products:
        product = Product(**product_data)
        db.add(product)

    db.commit()
    db.close()
    print(f"{len(products)} produtos inseridos")

if __name__ == "__main__":
    seed_products()