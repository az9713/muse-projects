// MIGRATED test: ESM + node:test. Run: node --test test/test-migrated.test.mjs
import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { add, sub, mul, div } from "../src/calc.mjs";
import { slugify, truncate, countWords } from "../src/strings.mjs";
import { mean, clamp, pctChange } from "../src/stats.mjs";

describe("calc", () => {
  it("adds", () => assert.equal(add(2, 3), 5));
  it("subtracts", () => assert.equal(sub(5, 3), 2));
  it("multiplies", () => assert.equal(mul(3, 4), 12));
  it("divides", () => assert.equal(div(7, 2), 3.5));
  it("rejects division by zero", () => assert.throws(() => div(1, 0), /division by zero/));
});

describe("strings", () => {
  it("slugifies", () => assert.equal(slugify("Hello World"), "hello-world"));
  it("keeps short text", () => assert.equal(truncate("abc", 10), "abc"));
  it("truncates long text", () => assert.ok(truncate("x".repeat(30), 20).endsWith("...")));
  it("counts words", () => assert.equal(countWords("a b c"), 3));
});

describe("stats", () => {
  it("means", () => assert.equal(mean([1, 2, 3, 4]), 2.5));
  it("rejects empty mean", () => assert.throws(() => mean([]), /empty/));
  it("clamps", () => {
    assert.equal(clamp(10, 0, 5), 5);
    assert.equal(clamp(-1, 0, 5), 0);
  });
  it("computes pct change", () => assert.equal(pctChange(100, 120), 20));
});
