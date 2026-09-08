"""Generate a deterministic synthetic access log (2000 lines, seed fixed)."""
import random

random.seed(20260907)

PATHS = ["/health", "/products", "/products/42", "/orders", "/orders/1001", "/search"]
WEIGHTS = [30, 25, 15, 15, 5, 10]
METHODS = {"/health": "GET", "/products": "GET", "/products/42": "GET",
           "/orders": "POST", "/orders/1001": "GET", "/search": "GET"}


def latency(path, error):
    base = {"/health": 3, "/products": 40, "/products/42": 35,
            "/orders": 120, "/orders/1001": 25, "/search": 300}[path]
    return max(1, int(random.gauss(base, base / 4)) + (2000 if error else 0))


with open("logs/access.log", "w", encoding="utf-8") as fh:
    for i in range(2000):
        path = random.choices(PATHS, WEIGHTS)[0]
        error = random.random() < (0.02 if path != "/search" else 0.08)
        status = 500 if error else 200
        fh.write(f"10.0.0.{i % 250} {1757200000 + i * 43} {METHODS[path]} {path} {status} {latency(path, error)}\n")
print("wrote logs/access.log (2000 lines)")
