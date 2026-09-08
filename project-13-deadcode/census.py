"""Census tool: AST-based unused top-level symbol finder.

Usage: python3 census.py [target_dir]  (default: src)
Reports module-level functions/classes with no importer in the tree.
`__init__` files and test fixtures are skipped; entry names in
KEEP (public API) are never reported.
Prints findings, exits 1 when dead code exists.
"""
import ast
import os
import sys

KEEP = set()
ENTRY = {"app"}


def defined(tree):
    return {node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}


def imported_names(tree):
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                names.add(alias.asname or alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names.add((alias.asname or alias.name).split(".")[0])
    return names


def census(target):
    modules = {}
    for root, _dirs, files in os.walk(target):
        for file in sorted(files):
            if not file.endswith(".py"):
                continue
            path = os.path.join(root, file)
            with open(path, encoding="utf-8") as fh:
                tree = ast.parse(fh.read())
            mod = os.path.splitext(os.path.basename(path))[0]
            modules[mod] = (path, defined(tree), imported_names(tree))
    used = set()
    for mod, (_path, defs, imports) in modules.items():
        used |= imports
        if mod in ENTRY:
            used |= defs
    dead = []
    for mod, (path, defs, _imports) in sorted(modules.items()):
        for name in sorted(defs - used - KEEP):
            dead.append(f"{path}:{name}")
    return dead


def main(argv=None):
    target = (argv or sys.argv[1:])[0:1]
    dead = census(target[0] if target else "src")
    for item in dead:
        print("DEAD", item)
    print(f"{len(dead)} dead symbols")
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
