#!/usr/bin/env node
// CLI: add / list / done over the service layer.
import * as service from "./service.mjs";

const [cmd, ...rest] = process.argv.slice(2);

function flag(name) {
  const hit = rest.find((a) => a === name || a.startsWith(name + "="));
  if (!hit) return undefined;
  return hit.includes("=") ? hit.split("=").slice(1).join("=") : true;
}

let out;
if (cmd === "add") {
  const title = rest.find((a) => !a.startsWith("--"));
  const tags = (flag("--tags") || "").split(",").filter((t) => t.trim());
  out = service.createTask(title, tags);
} else if (cmd === "list") {
  const tag = flag("--tag") ?? null;
  out = flag("--open") ? service.openTasks(tag) : service.listTasks(tag);
} else if (cmd === "done") {
  out = service.completeTask(Number(rest[0]));
} else {
  console.error("usage: cli.mjs <add|list|done> [...]");
  process.exit(1);
}
console.log(JSON.stringify(out, null, 2));
