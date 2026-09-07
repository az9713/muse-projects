// LEGACY: CommonJS (before migration)
function slugify(text) { return text.trim().toLowerCase().split(/\s+/).join("-"); }
function truncate(text, limit = 20) {
  if (text.length <= limit) return text;
  return text.slice(0, limit).trimEnd() + "...";
}
function countWords(text) { return text.split(/\s+/).filter(Boolean).length; }
module.exports = { slugify, truncate, countWords };
