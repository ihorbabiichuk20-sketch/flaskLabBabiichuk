import unittest

from app import app


class ProductsBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_products_list_page(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Products", response.data)
        self.assertIn(b"Flask Course", response.data)


if __name__ == "__main__":
    unittest.main()
