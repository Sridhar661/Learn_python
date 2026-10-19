import tempfile
import unittest
from pathlib import Path

from inventory import Inventory
from storage import JsonStorage


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        storage = JsonStorage(Path(self.temp_dir.name) / "inventory.json")
        self.inventory = Inventory(storage)
        self.product = self.inventory.add_product(
            "Coffee", "CF001", 12.50, 10, 2
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_product(self):
        self.assertEqual(self.product["name"], "Coffee")
        self.assertEqual(self.product["quantity"], 10)

    def test_duplicate_sku_is_rejected(self):
        with self.assertRaises(ValueError):
            self.inventory.add_product("Another Coffee", "cf001", 9.0)

    def test_search_by_name(self):
        results = self.inventory.search_products("cof")
        self.assertEqual(len(results), 1)

    def test_restock_increases_quantity(self):
        result = self.inventory.restock(self.product["id"], 5)
        self.assertEqual(result["quantity"], 15)

    def test_sale_reduces_stock_and_records_revenue(self):
        sale = self.inventory.record_sale(self.product["id"], 3)
        self.assertEqual(sale["total"], 37.5)
        self.assertEqual(self.inventory.list_products()[0]["quantity"], 7)

    def test_sale_cannot_exceed_stock(self):
        with self.assertRaises(ValueError):
            self.inventory.record_sale(self.product["id"], 11)

    def test_zero_sale_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            self.inventory.record_sale(self.product["id"], 0)

    def test_low_stock_alert(self):
        self.inventory.record_sale(self.product["id"], 8)
        self.assertEqual(len(self.inventory.low_stock_products()), 1)

    def test_data_persists_after_reload(self):
        reloaded = Inventory(self.inventory.storage)
        self.assertEqual(len(reloaded.list_products()), 1)
        self.assertEqual(reloaded.list_products()[0]["quantity"], 10)

    def test_sales_summary(self):
        self.inventory.record_sale(self.product["id"], 2)
        summary = self.inventory.sales_summary()
        self.assertEqual(summary["sale_count"], 1)
        self.assertEqual(summary["units_sold"], 2)
        self.assertEqual(summary["revenue"], 25.0)


if __name__ == "__main__":
    unittest.main()
