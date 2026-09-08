"""Stepped SQLite migration with per-step rollback.

v1: users(id, name) + schema_version=1
v2: users gets email (backfilled) + schema_version=2
v3: orders table + schema_version=3
"""
import sqlite3

STEPS = [1, 2, 3]


def connect(db_path):
    con = sqlite3.connect(db_path)
    con.execute("CREATE TABLE IF NOT EXISTS schema_version (v INTEGER)")
    if con.execute("SELECT COUNT(*) FROM schema_version").fetchone()[0] == 0:
        con.execute("INSERT INTO schema_version VALUES (0)")
    con.commit()
    return con


def version(con):
    return con.execute("SELECT v FROM schema_version").fetchone()[0]


def _set_version(con, value):
    con.execute("UPDATE schema_version SET v = ?", (value,))
    con.commit()


def up(con, target):
    while version(con) < target:
        current = version(con)
        if current == 0:
            con.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
            _set_version(con, 1)
        elif current == 1:
            con.execute("ALTER TABLE users ADD COLUMN email TEXT")
            con.execute("UPDATE users SET email = name || '@example.com'")
            _set_version(con, 2)
        elif current == 2:
            con.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, total REAL)")
            _set_version(con, 3)


def down(con, target):
    while version(con) > target:
        current = version(con)
        if current == 3:
            con.execute("DROP TABLE orders")
            _set_version(con, 2)
        elif current == 2:
            rows = con.execute("SELECT id, name FROM users").fetchall()
            con.execute("DROP TABLE users")
            con.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
            con.executemany("INSERT INTO users (id, name) VALUES (?, ?)", rows)
            _set_version(con, 1)
        elif current == 1:
            con.execute("DROP TABLE users")
            _set_version(con, 0)


def dump_users(con):
    return con.execute("SELECT id, name FROM users ORDER BY id").fetchall()
