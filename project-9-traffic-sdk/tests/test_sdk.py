"""Tests: inference coverage + generated client behavior via fake transport."""
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "out"))
sys.path.insert(0, os.path.join(ROOT, "gen"))

from build_sdk import fold, infer
from client import ShopClient

with open(os.path.join(ROOT, "traffic", "samples.json"), encoding="utf-8") as fh:
    SAMPLES = json.load(fh)


def fake_transport(calls):
    def call(method, path, body=None):
        calls.append((method, path, body))
        key = f"{method} {path}"
        if key in SAMPLES:
            return 200, SAMPLES[key]
        if key == "GET /orders/1001":
            return 200, {"id": 1001}
        return 404, {"error": "not found"}

    return call


class SdkTest(unittest.TestCase):
    def test_fold_numeric_segments(self):
        self.assertEqual(fold("/products/42"), "/products/{id}")
        self.assertEqual(fold("/health"), "/health")

    def test_inference_finds_five_endpoints(self):
        endpoints = infer()
        self.assertEqual(len(endpoints), 5)
        self.assertIn(("GET", "/health"), endpoints)
        self.assertIn(("POST", "/orders"), endpoints)

    def test_numeric_ids_folded(self):
        endpoints = infer()
        self.assertIn(("GET", "/products/{id}"), endpoints)
        self.assertNotIn(("GET", "/products/42"), endpoints)

    def test_status_codes_recorded(self):
        endpoints = infer()
        self.assertEqual(endpoints[("POST", "/orders")]["codes"], {201, 400})

    def test_client_health(self):
        calls = []
        client = ShopClient(fake_transport(calls))
        code, body = client.get_health()
        self.assertEqual((code, body["ok"]), (200, True))
        self.assertEqual(calls[-1][:2], ("GET", "/health"))

    def test_client_lists_products(self):
        client = ShopClient(fake_transport([]))
        code, items = client.list_products()
        self.assertEqual(code, 200)
        self.assertEqual(len(items), 2)

    def test_client_get_product_path(self):
        calls = []
        ShopClient(fake_transport(calls)).get_product(42)
        self.assertEqual(calls[-1][:2], ("GET", "/products/42"))

    def test_client_create_order_payload(self):
        calls = []
        ShopClient(fake_transport(calls)).create_order("widget", 2)
        self.assertEqual(calls[-1], ("POST", "/orders", {"sku": "widget", "qty": 2}))

    def test_client_get_order_path(self):
        calls = []
        ShopClient(fake_transport(calls)).get_order(1001)
        self.assertEqual(calls[-1][:2], ("GET", "/orders/1001"))

    def test_samples_cover_all_endpoints(self):
        endpoints = infer()
        for method, template in endpoints:
            sample = template.replace("{id}", "42" if "products" in template else "1001")
            self.assertIn(f"{method} {sample}", SAMPLES)


if __name__ == "__main__":
    unittest.main()
