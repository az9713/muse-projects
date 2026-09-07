// Pricing helpers (test-swarm target). Mirrors the Python billing module.
export function lineTotal(price, qty) {
  if (qty < 0) throw new Error("qty must be >= 0");
  if (price < 0) throw new Error("price must be >= 0");
  return Math.round(price * qty * 100) / 100;
}
export function discountRate(qty) {
  if (qty >= 100) return 0.2;
  if (qty >= 50) return 0.1;
  if (qty >= 10) return 0.05;
  return 0;
}
export function applyDiscount(total, qty) {
  return Math.round(total * (1 - discountRate(qty)) * 100) / 100;
}
export function withTax(total, rate = 0.07) {
  if (rate < 0) throw new Error("rate must be >= 0");
  return Math.round(total * (1 + rate) * 100) / 100;
}
export function invoice(price, qty, rate = 0.07) {
  const subtotal = lineTotal(price, qty);
  const discounted = applyDiscount(subtotal, qty);
  return {
    subtotal,
    discount: Math.round((subtotal - discounted) * 100) / 100,
    total: withTax(discounted, rate),
  };
}
