
import unittest
import tempfile
from pathlib import Path
from tinydb import TinyDB

from app import app
from app.products import views


class ProductBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False

        self.client = app.test_client()

        self.original_products_table = views.products_table

        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_db = TinyDB(
            Path(self.temp_dir.name) / "test_products.json",
            encoding="utf-8"
        )

        views.products_table = self.test_db.table("products")

        views.products_table.insert_multiple([
            {
                "id": 1,
                "name": "Laptop",
                "price": 1200.0,
                "content": "Intel Core i7",
                "category": "electronics",
                "quantity": 5,
                "image": "",
                "created_at": "2026-11-15"
            },
            {
                "id": 2,
                "name": "Phone",
                "price": 800.0,
                "content": "OLED display",
                "category": "electronics",
                "quantity": 10,
                "image": "",
                "created_at": "2026-11-15"
            }
        ])

    def tearDown(self):
        views.products_table = self.original_products_table

        self.test_db.close()
        self.temp_dir.cleanup()

    def test_products_list_page(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"Phone", response.data)

    def test_product_detail_page(self):
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Intel Core i7", response.data)

    def test_product_not_found(self):
        response = self.client.get("/products/999")
        self.assertEqual(response.status_code, 404)


    def test_add_product(self):
        response = self.client.post("/products/add", data={
            "name": "Tablet",
            "content": "Test tablet",
            "price": "500.00",
            "category": "electronics",
            "quantity": "4"
        })

        self.assertEqual(response.status_code, 302)

        product = views.products_table.get(
            lambda p: p["name"] == "Tablet"
        )

        self.assertIsNotNone(product)

    def test_edit_product(self):
        response = self.client.post("/products/1/edit", data={
            "name": "Updated Laptop",
            "content": "Updated description",
            "price": "1500.00",
            "category": "electronics",
            "quantity": "8"
        })

        self.assertEqual(response.status_code, 302)

        product = views.products_table.get(
            lambda p: p["id"] == 1
        )

        self.assertEqual(product["name"], "Updated Laptop")

    def test_delete_product(self):
        response = self.client.post("/products/1/delete")

        self.assertEqual(response.status_code, 302)

        product = views.products_table.get(
            lambda p: p["id"] == 1
        )

        self.assertIsNone(product)

if __name__ == "__main__":
    unittest.main()
