"""Traffic-driven SDK builder: access.log + samples.json -> out/client.py.

Usage: python3 gen/build_sdk.py  (writes out/client.py)
Infers endpoints from (method, path-template) pairs; numeric segments fold
to {id}. Emits a transport-injectable client so tests need no network.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TRAFFIC = os.path.join(HERE, "..", "traffic", "access.log")
SAMPLES = os.path.join(HERE, "..", "traffic", "samples.json")
OUT = os.path.join(HERE, "..", "out", "client.py")

HEADER = '"""GENERATED from traffic/access.log — do not edit by hand."""\n\n'


def fold(path):
    return re.sub(r"/\d+", "/{id}", path)


def infer():
    raw = {}
    with open(TRAFFIC, encoding="utf-8") as fh:
        for line in fh:
            parts = line.split(None, 2)
            if len(parts) < 3:
                continue
            method, path, rest = parts
            info = raw.setdefault((method, path), {"hits": 0, "codes": set(), "bodies": []})
            info["hits"] += 1
            status, _, body = rest.partition(" ")
            info["codes"].add(int(status))
            if body.strip():
                info["bodies"].append(json.loads(body))
    # Fold: a non-root parent with several distinct children means an id slot.
    children = {}
    for method, path in raw:
        parent, _, child = path.rpartition("/")
        children.setdefault((method, parent), []).append(child)
    endpoints = {}
    for (method, path), info in raw.items():
        parent, _, _child = path.rpartition("/")
        if parent and len(children[(method, parent)]) > 1:
            key = (method, f"{parent}/{{id}}")
        else:
            key = (method, path)
        agg = endpoints.setdefault(key, {"hits": 0, "codes": set(), "bodies": []})
        agg["hits"] += info["hits"]
        agg["codes"] |= info["codes"]
        agg["bodies"] += info["bodies"]
    return endpoints


def emit(endpoints):
    lines = [HEADER, "from __future__ import annotations", "", "", "class ShopClient:", "    def __init__(self, transport):", "        self.transport = transport", ""]
    if ("GET", "/health") in endpoints:
        lines += ["    def get_health(self):", '        return self.transport("GET", "/health")', ""]
    if ("GET", "/products") in endpoints:
        lines += ["    def list_products(self):", '        return self.transport("GET", "/products")', ""]
    if ("GET", "/products/{id}") in endpoints:
        lines += ["    def get_product(self, product_id):", '        return self.transport("GET", f"/products/{product_id}")', ""]
    if ("POST", "/orders") in endpoints:
        lines += [
            "    def create_order(self, sku, qty):",
            '        return self.transport("POST", "/orders", {"sku": sku, "qty": qty})',
            "",
        ]
    if ("GET", "/orders/{id}") in endpoints:
        lines += ["    def get_order(self, order_id):", '        return self.transport("GET", f"/orders/{order_id}")', ""]
    lines.append("")
    return "\n".join(lines)


def main():
    endpoints = infer()
    print(f"inferred {len(endpoints)} endpoints:")
    for (method, template), info in sorted(endpoints.items()):
        print(f"  {method} {template} hits={info['hits']} codes={sorted(info['codes'])}")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(emit(endpoints))
    print("wrote out/client.py")


if __name__ == "__main__":
    main()
