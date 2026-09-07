# #6 Bug-hunt — JS (`src/cart.mjs`, bugs J1..J5, all fixed)

## Verify

```sh
cd js
node repro/repro.mjs            # 5/5
node --test test/regress.test.mjs  # 5 passed
```

History: `proof/before-fix.log` (0/5 red) -> fixes -> `proof/after-fix.log`
(5/5 green). Fix details in `../SOLUTIONS.md`.
