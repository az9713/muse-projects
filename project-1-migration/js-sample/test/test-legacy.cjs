// LEGACY test: CommonJS + plain asserts. Run: node test/test-legacy.cjs
const assert = require("node:assert");
const { add, sub, mul, div } = require("../src/calc.cjs");
const { slugify, truncate, countWords } = require("../src/strings.cjs");
const { mean, clamp, pctChange } = require("../src/stats.cjs");

assert.strictEqual(add(2, 3), 5);
assert.strictEqual(sub(5, 3), 2);
assert.strictEqual(mul(3, 4), 12);
assert.strictEqual(div(7, 2), 3.5);
assert.throws(() => div(1, 0), /division by zero/);
assert.strictEqual(slugify("Hello World"), "hello-world");
assert.strictEqual(truncate("abc", 10), "abc");
assert.strictEqual(countWords("a b c"), 3);
assert.strictEqual(mean([1, 2, 3]), 2);
assert.throws(() => mean([]), /empty/);
assert.strictEqual(clamp(10, 0, 5), 5);
assert.strictEqual(pctChange(100, 120), 20);
console.log("LEGACY OK: 12 asserts passed");
