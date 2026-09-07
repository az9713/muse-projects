# SOLUTIONS — the 10 injected bugs and their fixes

All bugs were reproduced red (`proof/before-fix.log`, 0/5 each side) then
fixed green (`proof/after-fix.log`, 5/5) with regression tests.

## Python (`python/src/orders.py`)

| ID | Symptom | Root cause | Fix |
|----|---------|------------|-----|
| B1 | `bulk_rate(100)` gave 0.10, not 0.20 | `qty > 100` off-by-one on the tier boundary | `qty >= 100` |
| B2 | `add_note("b")` returned `["a", "b"]` | Mutable default arg `notes=[]` shared across calls | `notes=None`, copy before append |
| B3 | `line_total(0.1, 3)` was `0.30000000000000004` | Unrounded float arithmetic | `round(price * qty + 1e-9, 2)` |
| B4 | `receipt()` exposed internal `cost` with a clean env | `APP_DEBUG` defaulted to `"1"` (on) and gated a cost leak | Removed the debug branch entirely — receipts never carry cost |
| B5 | Promo reported live on `01/05/2027` | String `<=` on non-ISO `%m/%d/%Y` dates misorders across years | Parse with `strptime` and compare `date` objects |

## JS (`js/src/cart.mjs`)

| ID | Symptom | Root cause | Fix |
|----|---------|------------|-----|
| J1 | Page 1 of size 2 returned 1 item | `slice(start, end - 1)` dropped the last item | `slice((num-1)*size, num*size)` |
| J2 | Editing a fetched product corrupted the catalog | `getProduct` returned a live reference | Return a shallow copy `{ ...CATALOG[sku] }` |
| J3 | Promo "expired Dec 2026" was dated Jan 2027 | `new Date(2026, 12, 31)` — months are 0-indexed | `new Date(2026, 11, 31)` |
| J4 | `total(100)` was `NaN` | `fetchRate()` promise used without `await` | `total` is now `async` and awaits the rate |
| J5 | `checkout("widget", 2)` was `"205"` | String default fee `"5"` concatenated | `Number(fee)` before adding |

## Proof

- `python/proof/before-fix.log` — 0/5 (red)
- `python/proof/after-fix.log` — 5/5 (green)
- `js/proof/before-fix.log` — 0/5 (red)
- `js/proof/after-fix.log` — 5/5 (green)
- Regression suites: `python/tests/test_regress.py` (7 tests),
  `js/test/regress.test.mjs` (5 tests)
