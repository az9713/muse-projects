"""Rehearsal: migrate -> verify -> rollback -> verify on a seeded db.

Usage: python3 rehearse.py  (writes REHEARSAL.log, exit 1 on any mismatch)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from migrate import connect, down, dump_users, up, version

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "rehearsal.db")
LOG = os.path.join(HERE, "REHEARSAL.log")

lines = []


def log(text):
    lines.append(text)
    print(text)


def main():
    if os.path.exists(DB):
        os.remove(DB)
    con = connect(DB)
    up(con, 1)
    con.executemany("INSERT INTO users (name) VALUES (?)", [("ann",), ("bo",), ("cy",)])
    con.commit()
    before = dump_users(con)
    log(f"seeded v1, users={before}")

    up(con, 3)
    assert version(con) == 3, "migrate to v3 failed"
    emails = [row[0] for row in con.execute("SELECT email FROM users")]
    assert all("@" in (email or "") for email in emails), "backfill failed"
    orders = con.execute("SELECT name FROM sqlite_master WHERE name='orders'").fetchone()
    assert orders, "orders table missing"
    log(f"migrated to v3, emails backfilled, orders table present, users={len(before)}")

    down(con, 1)
    assert version(con) == 1, "rollback to v1 failed"
    after = dump_users(con)
    assert after == before, f"data changed across rollback: {before} vs {after}"
    log(f"rolled back to v1, users byte-identical: {after == before}")
    con.close()
    log("REHEARSAL OK")
    with open(LOG, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
