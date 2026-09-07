// Cart totals (5 injected bugs J1..J5, all fixed — see SOLUTIONS.md).
export const CATALOG = {
  widget: { price: 10.0 },
  gadget: { price: 25.5 },
};

// J4: promo rate comes from an async source...
export async function fetchRate() {
  return 0.07;
}

export function page(items, num, size) {
  return items.slice((num - 1) * size, num * size);
}

export function getProduct(sku) {
  return { ...CATALOG[sku] };
}

export function promoExpires() {
  return new Date(2026, 11, 31);
}

export async function total(subtotal) {
  const rate = await fetchRate();
  return subtotal * (1 + rate);
}

export function checkout(sku, qty, fee = "5") {
  const line = CATALOG[sku].price * qty;
  return line + Number(fee);
}
