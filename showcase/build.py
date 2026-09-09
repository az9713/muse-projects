"""Showcase builder: run all 17 projects, snapshot real outputs to showcase/.

Usage: python3 showcase/build.py
Writes showcase/index.html + showcase/<key>/results.html.
Generated artifacts touched by runs are restored via git afterwards
(see README note) so the tree only gains showcase/ files.
"""
import datetime
import html
import os
import subprocess

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "showcase")
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

CSS = """body{font-family:monospace;max-width:900px;margin:2rem auto;padding:0 1rem;line-height:1.55;color:#e8e8e8;background:#161616}
h1{font-size:1.4rem}h2{font-size:1.05rem;margin-top:1.8rem}
pre{background:#222;padding:.8rem;border-radius:6px;overflow-x:auto;font-size:.78rem;white-space:pre-wrap}
code{background:#2a2a2a;padding:.1rem .3rem;border-radius:3px}
.pass{color:#7dd87d;font-weight:bold}.fail{color:#ff7b7b;font-weight:bold}
table{border-collapse:collapse;width:100%;font-size:.84rem}
th,td{border:1px solid #444;padding:.35rem .5rem;text-align:left;vertical-align:top}
a{color:#8ab4ff}
footer{margin:2rem 0;font-size:.8rem;color:#999}"""

PROJECTS = [
    {"key": "01-migration", "title": "#1 Migration runner", "blurb": "unittest to pytest, CommonJS to ESM, parity-proven.", "cmds": [
        ("pytest migrated (15)", "project-1-migration/python-sample/.venv/bin/python -m pytest project-1-migration/python-sample/tests/test_migrated_pytest.py -q"),
        ("node migrated (13)", "node --test project-1-migration/js-sample/test/test-migrated.test.mjs"),
        ("parity script", "python3 project-1-migration/python-sample/check_parity.py")]},
    {"key": "02-coldstart", "title": "#2 Cold-start feature", "blurb": "Tags across store, service, CLI, docs from one TASK.md.", "cmds": [
        ("pytest tags (10)", "project-2-coldstart/python/.venv/bin/python -m pytest project-2-coldstart/python/tests -q"),
        ("node tags (10)", "node --test project-2-coldstart/js/test/tags.test.mjs")]},
    {"key": "03-test-swarm", "title": "#3 Test-and-fix swarm", "blurb": "2 thin tests expanded to 23 per language.", "cmds": [
        ("pytest full (23)", "project-3-test-swarm/python/.venv/bin/python -m pytest project-3-test-swarm/python/tests/test_full.py -q"),
        ("node full (23)", "node --test project-3-test-swarm/js/test/test-full.test.mjs")]},
    {"key": "04-polyglot", "title": "#4 Polyglot CLI", "blurb": "One Python CLI scaffolds TS, Go, Rust with tests.", "cmds": [
        ("pytest CLI (12)", "project-4-polyglot/.venv/bin/python -m pytest project-4-polyglot/tests -q"),
        ("e2e (real cargo + node)", "sh project-4-polyglot/e2e/check.sh")]},
    {"key": "05-docs-to-code", "title": "#5 Docs-to-code", "blurb": "Spec to server + client + mocks, contract-tested.", "cmds": [
        ("regenerate", "project-5-docs-to-code/.venv/bin/python project-5-docs-to-code/gen/generate.py"),
        ("pytest contract (10)", "project-5-docs-to-code/.venv/bin/python -m pytest project-5-docs-to-code/tests -q")]},
    {"key": "06-bughunt", "title": "#6 Bug-hunt marathon", "blurb": "10 injected bugs, repro to fix, proof logs kept.", "cmds": [
        ("python repro (5/5)", "project-6-bughunt/python/.venv/bin/python project-6-bughunt/python/repro/repro.py"),
        ("pytest regress (7)", "project-6-bughunt/python/.venv/bin/python -m pytest project-6-bughunt/python/tests -q"),
        ("node repro (5/5)", "node project-6-bughunt/js/repro/repro.mjs"),
        ("node regress (5)", "node --test project-6-bughunt/js/test/regress.test.mjs")]},
    {"key": "07-selfheal", "title": "#7 Self-healing CI", "blurb": "The whole repo, one command.", "cmds": [
        ("heal.sh", "sh heal.sh")]},
    {"key": "08-strict-typing", "title": "#8 Strict typing ascent", "blurb": "Untyped snapshot to mypy --strict clean.", "cmds": [
        ("pytest (10)", "project-8-strict-typing/.venv/bin/python -m pytest project-8-strict-typing/tests -q"),
        ("mypy strict", "project-8-strict-typing/.venv/bin/python -m mypy project-8-strict-typing/app")]},
    {"key": "09-traffic-sdk", "title": "#9 Traffic-to-SDK", "blurb": "17 log lines to 5 endpoints to tested client.", "cmds": [
        ("rebuild SDK", "project-9-traffic-sdk/.venv/bin/python project-9-traffic-sdk/gen/build_sdk.py"),
        ("pytest (10)", "project-9-traffic-sdk/.venv/bin/python -m pytest project-9-traffic-sdk/tests -q")]},
    {"key": "10-upgrade", "title": "#10 Upgrade cascade", "blurb": "v1 to v2 breakages chased across 3 packages.", "cmds": [
        ("pytest (8)", "project-10-upgrade/.venv/bin/python -m pytest project-10-upgrade/tests -q")]},
    {"key": "11-log-dashboard", "title": "#11 Log-to-dashboard", "blurb": "2000 lines to SQLite + offline HTML report.", "cmds": [
        ("generate + analyze", "project-11-log-dashboard/.venv/bin/python project-11-log-dashboard/gen_logs.py && project-11-log-dashboard/.venv/bin/python project-11-log-dashboard/analyze.py"),
        ("pytest (8)", "project-11-log-dashboard/.venv/bin/python -m pytest project-11-log-dashboard/tests -q")]},
    {"key": "12-config-drift", "title": "#12 Config drift doctor", "blurb": "6 findings incl. a committed (fake) secret.", "cmds": [
        ("doctor", "project-12-config-drift/.venv/bin/python project-12-config-drift/doctor.py"),
        ("pytest (8)", "project-12-config-drift/.venv/bin/python -m pytest project-12-config-drift/tests -q")]},
    {"key": "13-deadcode", "title": "#13 Dead-code census", "blurb": "AST census: src clean, fixtures flagged.", "cmds": [
        ("census src + fixtures", "project-13-deadcode/.venv/bin/python project-13-deadcode/census.py project-13-deadcode/src; project-13-deadcode/.venv/bin/python project-13-deadcode/census.py project-13-deadcode/fixtures"),
        ("pytest (8)", "project-13-deadcode/.venv/bin/python -m pytest project-13-deadcode/tests -q")]},
    {"key": "14-fuzz", "title": "#14 Fuzz farmer", "blurb": "5000-case round-trip fuzz on a CSV parser.", "cmds": [
        ("fuzz 5000", "project-14-fuzz/.venv/bin/python project-14-fuzz/fuzz.py 5000"),
        ("pytest (10)", "project-14-fuzz/.venv/bin/python -m pytest project-14-fuzz/tests -q")]},
    {"key": "15-i18n", "title": "#15 i18n extraction", "blurb": "Locales, fallback, CI guard.", "cmds": [
        ("guard", "project-15-i18n/.venv/bin/python project-15-i18n/tools/check.py"),
        ("pytest (8)", "project-15-i18n/.venv/bin/python -m pytest project-15-i18n/tests -q")]},
    {"key": "16-rehearsal", "title": "#16 Migration rehearsal", "blurb": "Migrate, verify, roll back, byte-identical.", "cmds": [
        ("rehearse", "project-16-rehearsal/.venv/bin/python project-16-rehearsal/rehearse.py"),
        ("pytest (8)", "project-16-rehearsal/.venv/bin/python -m pytest project-16-rehearsal/tests -q")]},
    {"key": "17-perf", "title": "#17 Perf tracker", "blurb": "Benchmarks, trend page, regression gate.", "cmds": [
        ("bench + gate + trend", "project-17-perf/.venv/bin/python project-17-perf/bench.py --repeat 2 && project-17-perf/.venv/bin/python project-17-perf/gate.py && project-17-perf/.venv/bin/python project-17-perf/trend.py"),
        ("pytest (8)", "project-17-perf/.venv/bin/python -m pytest project-17-perf/tests -q")]},
]


def run(cmd):
    try:
        proc = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True, timeout=280)
        return proc.returncode, (proc.stdout + proc.stderr)[-6000:]
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT after 280s"


def page(title, body):
    return f"<!DOCTYPE html>\n<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>{html.escape(title)}</title><style>{CSS}</style></head><body>{body}</body></html>"


def main():
    os.makedirs(OUT, exist_ok=True)
    summary = []
    for proj in PROJECTS:
        blocks = [f"<p><a href='index.html'>&larr; all projects</a></p><h1>{html.escape(proj['title'])}</h1><p>{html.escape(proj['blurb'])}</p>"]
        ok = True
        for label, cmd in proj["cmds"]:
            code, out = run(cmd)
            # census-on-src exits 1 when dead code exists; here src is clean (0).
            # fixtures census exits 1 by design; combined command exit reflects last part.
            passed = code == 0
            if proj["key"] == "13-deadcode" and label.startswith("census"):
                passed = "0 dead symbols" in out and "3 dead symbols" in out
            ok = ok and passed
            cls = "pass" if passed else "fail"
            blocks.append(f"<h2>$ {html.escape(label)} <span class='{cls}'>{'PASS' if passed else 'FAIL'} (exit {code})</span></h2><pre>{html.escape(out)}</pre>")
        summary.append((proj, ok))
        path = os.path.join(OUT, proj["key"])
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "results.html"), "w", encoding="utf-8") as fh:
            fh.write(page(proj["title"], "\n".join(blocks) + f"<footer>Captured {STAMP} by showcase/build.py</footer>"))
        print(("PASS " if ok else "FAIL ") + proj["key"])

    rows = "\n".join(
        f"<tr><td><a href='{p['key']}/results.html'>{p['title']}</a></td><td>{html.escape(p['blurb'])}</td>"
        f"<td class='{'pass' if ok else 'fail'}'>{'PASS' if ok else 'fail'}</td></tr>"
        for p, ok in summary
    )
    total_ok = sum(1 for _, ok in summary if ok)
    index = (f"<h1>Showcase — 17 projects, run live</h1><p>{total_ok}/{len(summary)} projects green. "
             f"Captured {STAMP}. Each page shows real command output.</p>"
             f"<table><tr><th>Project</th><th>What</th><th>Run</th></tr>{rows}</table>"
             f"<footer>Built by <code>showcase/build.py</code>. Regenerate any time: <code>python3 showcase/build.py</code></footer>")
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(page("Showcase — 17 projects", index))
    print(f"showcase/index.html: {total_ok}/{len(summary)} green")


if __name__ == "__main__":
    main()
