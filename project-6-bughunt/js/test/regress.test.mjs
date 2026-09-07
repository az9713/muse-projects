// Regression tests: assert CORRECT behavior (fail on buggy code, pass fixed).
// Run: node --test test/regress.test.mjs
import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { page, getProduct, promoExpires, total, checkout, CATALOG } from "../src/cart.mjs";

describe("fixed", () => {
  it("J1 pages fully", () => {
    assert.deepEqual(page([1, 2, 3, 4, 5, 6], 1, 2), [1, 2]);
    assert.deepEqual(page([1, 2, 3, 4, 5, 6], 2, 2), [3, 4]);
    assert.deepEqual(page([1, 2, 3, 4, 5, 6], 3, 2), [5, 6]);
  });
  it("J2 catalog immutable via getter", () => {
    getProduct("widget").price = 999;
    assert.equal(CATALOG.widget.price, 10.0);
  });
  it("J3 promo expiry is Dec 2026", () => {
    const d = promoExpires();
    assert.equal(d.getFullYear(), 2026);
    assert.equal(d.getMonth(), 11);
    assert.equal(d.getDate(), 31);
  });
  it("J4 total awaits rate", async () => {
    assert.equal(await total(100), 107);
  });
  it("J5 checkout numeric", () => {
    assert.equal(checkout("widget", 2), 25);
    assert.equal(checkout("gadget", 1, 0), 25.5);
  });
});
