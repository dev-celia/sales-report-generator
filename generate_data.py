import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

categories = ["Electronics", "Clothing", "Home", "Sports", "Books"]
products = {
    "Electronics": ["Headphones", "Smartphone", "Laptop", "Charger"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers"],
    "Home": ["Lamp", "Pillow", "Rug", "Mug"],
    "Sports": ["Yoga Mat", "Dumbbells", "Running Shoes", "Water Bottle"],
    "Books": ["Novel", "Cookbook", "Comic", "Biography"]
}

start_date = datetime(2026, 1, 1)
rows = []

for _ in range(300):
    category = random.choice(categories)
    product = random.choice(products[category])
    date = start_date + timedelta(days=random.randint(0, 269))
    amount = round(random.uniform(5, 200), 2)
    rows.append([date.strftime("%Y-%m-%d"), category, product, amount])

df = pd.DataFrame(rows, columns=["Date", "Category", "Product", "Amount"])
df.to_excel("sales_data.xlsx", index=False)

print("sales_data.xlsx generated successfully!")