// FULL suite (after the swarm): 23 tests. Run: node --test test/test-full.test.mjs
import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { lineTotal, discountRate, applyDiscount, withTax, invoice } from "../src/pricing.mjs";

describe("lineTotal", () => {
  it("basic", () => assert.equal(lineTotal(10, 3), 30));
  it("zero qty", () => assert.equal(lineTotal(10, 0), 0));
  it("rounding", () => assert.equal(lineTotal(2.333, 3), 7));
  it("rejects negative qty", () => assert.throws(() => lineTotal(10, -1), /qty/));
  it("rejects negative price", () => assert.throws(() => lineTotal(-5, 2), /price/));
});

describe("discountRate", () => {
  it("none below 10", () => assert.equal(discountRate(9), 0));
  it("5% at 10", () => assert.equal(discountRate(10), 0.05));
  it("5% at 49", () => assert.equal(discountRate(49), 0.05));
  it("10% at 50", () => assert.equal(discountRate(50), 0.1));
  it("10% at 99", () => assert.equal(discountRate(99), 0.1));
  it("20% at 100", () => assert.equal(discountRate(100), 0.2));
});

describe("applyDiscount", () => {
  it("no discount", () => assert.equal(applyDiscount(100, 5), 100));
  it("5%", () => assert.equal(applyDiscount(100, 10), 95));
  it("20%", () => assert.equal(applyDiscount(200, 100), 160));
});

describe("withTax", () => {
  it("default rate", () => assert.equal(withTax(100), 107));
  it("zero rate", () => assert.equal(withTax(100, 0), 100));
  it("rejects negative rate", () => assert.throws(() => withTax(100, -0.01), /rate/));
});

describe("invoice", () => {
  it("single unit", () => {
    assert.deepEqual(invoice(10, 1), { subtotal: 10, discount: 0, total: 10.7 });
  });
  it("bulk discount", () => {
    assert.deepEqual(invoice(10, 100), { subtotal: 1000, discount: 200, total: 856 });
  });
  it("zero qty", () => {
    assert.deepEqual(invoice(10, 0), { subtotal: 0, discount: 0, total: 0 });
  });
  it("custom tax", () => assert.equal(invoice(100, 1, 0).total, 100));
  it("mid tier", () => {
    const inv = invoice(20, 50);
    assert.equal(inv.subtotal, 1000);
    assert.equal(inv.discount, 100);
  });
  it("keys", () => {
    assert.deepEqual(Object.keys(invoice(5, 2)).sort(), ["discount", "subtotal", "total"]);
  });
});
