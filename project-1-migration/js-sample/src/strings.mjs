// MIGRATED: ESM (after migration)
export function slugify(text) { return text.trim().toLowerCase().split(/\s+/).join("-"); }
export function truncate(text, limit = 20) {
  if (text.length <= limit) return text;
  return text.slice(0, limit).trimEnd() + "...";
}
export function countWords(text) { return text.split(/\s+/).filter(Boolean).length; }
