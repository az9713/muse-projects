// Service layer: validation + business rules over the store.
import * as store from "./store.mjs";

export function cleanTags(tags) {
  const cleaned = [];
  for (const raw of tags ?? []) {
    const tag = raw.trim().toLowerCase();
    if (!tag) throw new Error("tags must be non-empty strings");
    if (!cleaned.includes(tag)) cleaned.push(tag);
  }
  return cleaned;
}

export function createTask(title, tags = [], dbPath) {
  title = title.trim();
  if (!title) throw new Error("title must be non-empty");
  return store.addTask(title, cleanTags(tags), dbPath);
}

export function listTasks(tag = null, dbPath) {
  if (tag !== null) {
    tag = tag.trim().toLowerCase();
    if (!tag) throw new Error("tag filter must be non-empty");
  }
  return store.listTasks(tag, dbPath);
}

export function completeTask(id, dbPath) {
  return store.setDone(id, true, dbPath);
}

export function openTasks(tag = null, dbPath) {
  return listTasks(tag, dbPath).filter((t) => !t.done);
}
