"""Config drift doctor: envs/*.env -> findings.json + schema.json + .env.example.

Usage: python3 doctor.py
Findings use fixed severities; secrets are flagged, never printed in full
(the demo SECRET_KEY is an acknowledged fake — see envs/prod.env).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ENVS = os.path.join(HERE, "envs")

SCHEMA = {
    "required": ["APP_PORT", "TIMEOUT", "RETRIES", "DEBUG", "DB_HOST", "LOG_LEVEL"],
    "types": {
        "APP_PORT": "int",
        "TIMEOUT": "int",
        "RETRIES": "int",
        "DEBUG": "bool",
        "DB_HOST": "str",
        "LOG_LEVEL": "str",
    },
    "rules": [
        "TIMEOUT must be identical in every env",
        "RETRIES must be present in every env",
        "DEBUG must be false outside dev",
        "DB_HOST must not be localhost outside dev",
        "no SECRET_* keys may be committed",
    ],
}


def parse(path):
    values = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                values[key.strip()] = value.strip()
    return values


def cast(value, kind):
    if kind == "int":
        return int(value)
    if kind == "bool":
        return value.lower() == "true"
    return value


def validate(values):
    errors = []
    for key in SCHEMA["required"]:
        if key not in values:
            errors.append(f"missing {key}")
    for key, kind in SCHEMA["types"].items():
        if key in values:
            try:
                cast(values[key], kind)
            except ValueError:
                errors.append(f"{key} is not a {kind}")
    return errors


def doctor():
    envs = {name: parse(os.path.join(ENVS, name)) for name in ("dev.env", "staging.env", "prod.env")}
    findings = []

    timeouts = {name: values.get("TIMEOUT") for name, values in envs.items()}
    if len(set(timeouts.values())) > 1:
        findings.append({"id": "F1", "severity": "medium", "detail": f"TIMEOUT differs: {timeouts}"})

    missing = [name for name, values in envs.items() if "RETRIES" not in values]
    if missing:
        findings.append({"id": "F2", "severity": "high", "detail": f"RETRIES missing in: {missing}"})

    debug_on = [name for name, values in envs.items() if values.get("DEBUG") == "true" and name != "dev.env"]
    if debug_on:
        findings.append({"id": "F3", "severity": "medium", "detail": f"DEBUG on outside dev: {debug_on}"})

    leaked = [name for name, values in envs.items() for key in values if key.startswith("SECRET_")]
    if leaked:
        findings.append({"id": "F4", "severity": "critical", "detail": f"secret committed in: {sorted(set(leaked))}"})

    local_prod = [name for name, values in envs.items() if name != "dev.env" and values.get("DB_HOST") == "localhost"]
    if local_prod:
        findings.append({"id": "F5", "severity": "high", "detail": f"non-dev DB_HOST=localhost: {local_prod}"})

    all_keys = set().union(*[set(v) for v in envs.values()])
    single = sorted(k for k in all_keys if sum(k in v for v in envs.values()) == 1 and not k.startswith("SECRET_"))
    if single:
        findings.append({"id": "F6", "severity": "low", "detail": f"keys in one env only: {single}"})

    with open(os.path.join(HERE, "findings.json"), "w", encoding="utf-8") as fh:
        json.dump(findings, fh, indent=2)
    with open(os.path.join(HERE, "schema.json"), "w", encoding="utf-8") as fh:
        json.dump(SCHEMA, fh, indent=2)
    with open(os.path.join(HERE, ".env.example"), "w", encoding="utf-8") as fh:
        fh.writelines(f"{key}=<{'true/false' if SCHEMA['types'][key] == 'bool' else SCHEMA['types'][key]}>\n" for key in SCHEMA["required"])
    print(f"{len(findings)} findings: " + ", ".join(f"{f['id']}/{f['severity']}" for f in findings))
    return findings


if __name__ == "__main__":
    doctor()
