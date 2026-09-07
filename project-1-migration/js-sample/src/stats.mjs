// MIGRATED: ESM (after migration)
export function mean(values) {
  if (values.length === 0) throw new Error("empty");
  return values.reduce((s, v) => s + v, 0) / values.length;
}
export function clamp(value, low, high) { return Math.max(low, Math.min(high, value)); }
export function pctChange(oldV, newV) {
  if (oldV === 0) throw new Error("old must be non-zero");
  return ((newV - oldV) / oldV) * 100;
}
