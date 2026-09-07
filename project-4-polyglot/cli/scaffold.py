"""Polyglot scaffolder: generate minimal TS / Go / Rust projects.

Templates use @NAME@ placeholders (literal braces in TS/Go/Rust sources
make %- or f-string formatting unreadable, so plain replacement it is).
"""
import argparse
import os
import sys

LANGS = ("ts", "go", "rust")

TS_PACKAGE = """{
  "name": "@NAME@",
  "version": "0.1.0",
  "type": "module",
  "scripts": {"test": "node --test test/*.test.mjs"}
}
"""

TS_INDEX = """export function hello() {
  return `hello from @NAME@`;
}
"""

TS_TEST = """import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { hello } from "../src/index.mjs";

describe("hello", () => {
  it("greets", () => assert.equal(hello(), "hello from @NAME@"));
});
"""

GO_MOD = """module @NAME@

go 1.21
"""

GO_MAIN = """package main

import "fmt"

func Hello() string {
  return "hello from @NAME@"
}

func main() {
  fmt.Println(Hello())
}
"""

GO_TEST = """package main

import "testing"

func TestHello(t *testing.T) {
  if Hello() != "hello from @NAME@" {
    t.Fatal("bad greeting")
  }
}
"""

RUST_TOML = """[package]
name = "@NAME@"
version = "0.1.0"
edition = "2021"
"""

RUST_MAIN = """fn hello() -> String {
    format!("hello from {}", "@NAME@")
}

fn main() {
    println!("{}", hello());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn greets() {
        assert_eq!(hello(), "hello from @NAME@");
    }
}
"""


def files_for(lang, name):
    if lang == "ts":
        files = {
            "package.json": TS_PACKAGE,
            "src/index.mjs": TS_INDEX,
            "test/index.test.mjs": TS_TEST,
        }
    elif lang == "go":
        files = {"go.mod": GO_MOD, "main.go": GO_MAIN, "main_test.go": GO_TEST}
    elif lang == "rust":
        files = {"Cargo.toml": RUST_TOML, "src/main.rs": RUST_MAIN}
    else:
        raise ValueError(f"unknown lang: {lang}")
    return {rel: content.replace("@NAME@", name) for rel, content in files.items()}


def scaffold(lang, name, out):
    if lang not in LANGS:
        raise ValueError(f"lang must be one of {LANGS}")
    if not name or not name.strip():
        raise ValueError("name must be non-empty")
    target = os.path.join(out, f"{name.strip()}-{lang}")
    for rel, content in files_for(lang, name.strip()).items():
        path = os.path.join(target, rel)
        os.makedirs(os.path.dirname(path) or target, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
    return target


def main(argv=None):
    parser = argparse.ArgumentParser(prog="scaffold")
    parser.add_argument("--lang", required=True, choices=LANGS)
    parser.add_argument("--name", required=True)
    parser.add_argument("--out", default=".")
    args = parser.parse_args(argv)
    print(scaffold(args.lang, args.name, args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
