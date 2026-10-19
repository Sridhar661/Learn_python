"""Core inventory operations and sales recording."""

from storage import JsonStorage
from validators import clean_name, validate_non_negative, validate_positive_int


class Inventory:
    def __init__(self, storage=None):
        self.storage = storage or JsonStorage()
        saved = self.storage.load()
        self.products = saved.get("products", [])
        self.sales = saved.get("sales", [])

    def _save(self) -> None:
        self.storage.save({"products": self.products, "sales": self.sales})

    def _find_product(self, product_id: int) -> dict:
        for product in self.products:
            if product["id"] == product_id:
                return product
        raise KeyError(f"Product ID {product_id} was not found.")

    def add_product(
        self,
        name: str,
        sku: str,
        price: float,
        quantity: int = 0,
        low_stock_threshold: int = 5,
    ) -> dict:
        name = clean_name(name)
        sku = clean_name(sku).upper()
        price = validate_non_negative(price, "Price")
        quantity = validate_non_negative(quantity, "Quantity")
        low_stock_threshold = validate_non_negative(
            low_stock_threshold, "Low-stock threshold"
        )

        if not sku:
            raise ValueError("SKU cannot be empty.")
        if any(p["sku"].casefold() == sku.casefold() for p in self.products):
            raise ValueError(f"SKU {sku} already exists.")
        if int(quantity) != quantity or int(low_stock_threshold) != low_stock_threshold:
            raise ValueError("Quantities and thresholds must be whole numbers.")

        product_id = max((p["id"] for p in self.products), default=0) + 1
        product = {
            "id": product_id,
            "name": name,
            "sku": sku,
            "price": round(float(price), 2),
            "quantity": int(quantity),
            "low_stock_threshold": int(low_stock_threshold),
        }
        self.products.append(product)
        self._save()
        return product.copy()

    def list_products(self) -> list[dict]:
        return [product.copy() for product in self.products]

    def search_products(self, term: str) -> list[dict]:
        term = term.strip().casefold()
        if not term:
            return self.list_products()
        return [
            product.copy()
            for product in self.products
            if term in product["name"].casefold()
            or term in product["sku"].casefold()
        ]

    def restock(self, product_id: int, quantity: int) -> dict:
        product = self._find_product(product_id)
        quantity = validate_positive_int(quantity, "Restock quantity")
        product["quantity"] += quantity
        self._save()
        return product.copy()

    def record_sale(self, product_id: int, quantity: int) -> dict:
        product = self._find_product(product_id)
        quantity = validate_positive_int(quantity, "Sale quantity")
        if quantity > product["quantity"]:
            raise ValueError(
                f"Insufficient stock: only {product['quantity']} available."
            )

        total = round(product["price"] * quantity, 2)
        sale_id = max((sale["id"] for sale in self.sales), default=0) + 1
        sale = {
            "id": sale_id,
            "product_id": product["id"],
            "product_name": product["name"],
            "quantity": quantity,
            "unit_price": product["price"],
            "total": total,
        }
        product["quantity"] -= quantity
        self.sales.append(sale)
        self._save()
        return sale.copy()

    def low_stock_products(self) -> list[dict]:
        return [
            product.copy()
            for product in self.products
            if product["quantity"] <= product["low_stock_threshold"]
        ]

    def sales_summary(self) -> dict:
        total_units = sum(sale["quantity"] for sale in self.sales)
        revenue = round(sum(sale["total"] for sale in self.sales), 2)
        return {
            "sale_count": len(self.sales),
            "units_sold": total_units,
            "revenue": revenue,
            "sales": [sale.copy() for sale in self.sales],
        }
