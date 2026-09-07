// Repro script: one check per injected bug. Exit 1 if any FAIL.
import { page, getProduct, promoExpires, total, checkout, CATALOG } from "../src/cart.mjs";

const results = [];
function check(name, cond) {
  results.push([name, cond]);
  console.log(cond ? "PASS" : "FAIL", name);
}

check("J1 page has full size", page([1, 2, 3, 4, 5, 6], 1, 2).length === 2);
const p = getProduct("widget");
p.price = 999;
check("J2 catalog shielded", CATALOG.widget.price === 10.0);
check("J3 promo expires Dec 2026", promoExpires().getFullYear() === 2026 && promoExpires().getMonth() === 11);
check("J4 total is a number", (await total(100)) === 107);
check("J5 checkout adds fee", checkout("widget", 2) === 25);

const failed = results.filter(([, ok]) => !ok).length;
console.log(`${results.length - failed}/${results.length} passed`);
process.exit(failed ? 1 : 0);
