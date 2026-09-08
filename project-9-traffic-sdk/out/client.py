"""GENERATED from traffic/access.log — do not edit by hand."""


from __future__ import annotations


class ShopClient:
    def __init__(self, transport):
        self.transport = transport

    def get_health(self):
        return self.transport("GET", "/health")

    def list_products(self):
        return self.transport("GET", "/products")

    def get_product(self, product_id):
        return self.transport("GET", f"/products/{product_id}")

    def create_order(self, sku, qty):
        return self.transport("POST", "/orders", {"sku": sku, "qty": qty})

    def get_order(self, order_id):
        return self.transport("GET", f"/orders/{order_id}")

