// Data layer: JSON-file backed task store.
import { readFileSync, writeFileSync, existsSync } from "node:fs";

export const DB_PATH = new URL("../tasks.json", import.meta.url).pathname;

export function load(dbPath = DB_PATH) {
  if (!existsSync(dbPath)) return [];
  return JSON.parse(readFileSync(dbPath, "utf-8"));
}

export function save(rows, dbPath = DB_PATH) {
  writeFileSync(dbPath, JSON.stringify(rows, null, 2));
}

export function addTask(title, tags = [], dbPath = DB_PATH) {
  const rows = load(dbPath);
  const task = {
    id: rows.reduce((m, r) => Math.max(m, r.id), 0) + 1,
    title,
    done: false,
    tags: [...new Set(tags)].sort(),
  };
  rows.push(task);
  save(rows, dbPath);
  return task;
}

export function listTasks(tag = null, dbPath = DB_PATH) {
  const rows = load(dbPath);
  if (tag === null) return rows;
  return rows.filter((r) => (r.tags ?? []).includes(tag));
}

export function getTask(id, dbPath = DB_PATH) {
  const found = load(dbPath).find((r) => r.id === id);
  if (!found) throw new Error(`no task ${id}`);
  return found;
}

export function setDone(id, done = true, dbPath = DB_PATH) {
  const rows = load(dbPath);
  const task = rows.find((r) => r.id === id);
  if (!task) throw new Error(`no task ${id}`);
  task.done = done;
  save(rows, dbPath);
  return task;
}
