// WEAK suite (before the swarm): 2 checks. Run: node test/test-weak.mjs
import assert from "node:assert/strict";
import { invoice } from "../src/pricing.mjs";

const inv = invoice(10, 1);
assert.equal(inv.subtotal, 10);
assert.ok(inv.total > 0);
console.log("WEAK OK: 2 checks passed (coverage deliberately thin)");
