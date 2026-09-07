// Acceptance tests for the tags feature. Run: node --test test/tags.test.mjs
import { describe, it, beforeEach } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import * as service from "../src/service.mjs";

let db;
beforeEach(() => {
  db = join(mkdtempSync(join(tmpdir(), "tasks-")), "t.json");
});

describe("tags", () => {
  it("creates with normalized tags", () => {
    assert.deepEqual(service.createTask("Write report", ["Work", "urgent"], db).tags, ["urgent", "work"]);
  });
  it("creates without tags", () => {
    assert.deepEqual(service.createTask("Plain", [], db).tags, []);
  });
  it("dedupes tags", () => {
    assert.deepEqual(service.createTask("Dup", ["a", "A ", "a"], db).tags, ["a"]);
  });
  it("rejects empty tags", () => {
    assert.throws(() => service.createTask("Bad", ["ok", "  "], db), /non-empty/);
  });
  it("filters by tag", () => {
    service.createTask("One", ["work"], db);
    service.createTask("Two", ["home"], db);
    assert.deepEqual(service.listTasks("work", db).map((t) => t.title), ["One"]);
  });
  it("filters case-insensitively", () => {
    service.createTask("One", ["Work"], db);
    assert.equal(service.listTasks("WORK", db).length, 1);
  });
  it("rejects empty tag filter", () => {
    assert.throws(() => service.listTasks("  ", db), /non-empty/);
  });
  it("opens with tag", () => {
    const t = service.createTask("One", ["work"], db);
    service.createTask("Two", ["work"], db);
    service.completeTask(t.id, db);
    assert.equal(service.openTasks("work", db).length, 1);
  });
  it("keeps title validation", () => {
    assert.throws(() => service.createTask("   ", ["work"], db), /title/);
  });
  it("keeps done flow", () => {
    const t = service.createTask("One", [], db);
    assert.equal(service.completeTask(t.id, db).done, true);
  });
});
