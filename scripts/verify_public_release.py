from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_REPOSITORY = "https://github.com/youta-01/anti-sleep-turret-demo"

CONTENT_RULES = {
    "local IPv4 address": re.compile(r"(?<![\d.])(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})(?![\d.])"),
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "local user path": re.compile(r"C:" + re.escape("\\") + r"Users" + re.escape("\\"), re.I),
    "cloud-sync path": re.compile("One" + "Drive", re.I),
    "authorization header": re.compile(r"Authoriz" + r"ation\s*:\s*\S+", re.I),
    "bearer credential": re.compile(r"\bbear" + r"er\s+[A-Za-z0-9._~+/-]{12,}", re.I),
    "credential query": re.compile(r"[?&](?:to" + r"ken|auth|api[_-]?key)=[^\s&#]+", re.I),
    "serialized QR content": re.compile(r"(?:qr[_-]?(?:payload|content)|shortcut[_-]?payload)\s*[:=]", re.I),
    "workspace URL": re.compile(r"https?://(?:www\.)?not" + r"ion\.(?:so|site)/\S+", re.I),
    "commit identifier": re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])", re.I),
    "health history field": re.compile(
        r"(?:diagnosis|medical_history|health_history|medication|prescription|blood_pressure|heart_rate|診断名|服薬歴|病歴|血圧)\s*[:=]",
        re.I,
    ),
}

FORBIDDEN_PATHS = {
    "config" + ".yaml",
    "data",
    "logs",
    "incoming" + "_media",
}


def candidate_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / item.decode("utf-8") for item in result.stdout.split(b"\0") if item]


def inspect(path: Path) -> list[str]:
    relative = path.relative_to(ROOT)
    if any(part.lower() in FORBIDDEN_PATHS for part in relative.parts):
        return [f"forbidden path: {relative}"]
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    findings = [f"{label}: {relative}" for label, pattern in CONTENT_RULES.items() if pattern.search(text)]
    for url in re.findall(r"https?://github\.com/[^\s)>]+", text, re.I):
        if not url.rstrip(".,`").startswith(ALLOWED_REPOSITORY):
            findings.append(f"non-public repository URL: {relative}")
    return findings


def main() -> int:
    files = candidate_files()
    findings = [finding for path in files for finding in inspect(path)]
    if findings:
        print("Public release scan failed:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        return 1
    print(f"Public release scan passed ({len(files)} files checked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
