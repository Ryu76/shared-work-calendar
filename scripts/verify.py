"""Verify the calendar using a disposable database, key and upload directory."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".py", ".md", ".txt", ".yml", ".yaml", ".js", ".css", ".html"}


def isolated_environment(directory: Path) -> dict[str, str]:
    """Discard inherited product settings; never read a product key or database."""
    env = {key: value for key, value in os.environ.items() if not key.startswith("WORK_CALENDAR_")}
    env.update({
        "WORK_CALENDAR_DB": str(directory / "calendar.db"),
        "WORK_CALENDAR_DB_KEY_FILE": str(directory / "isolated.dpapi"),
        "WORK_CALENDAR_DB_KEY": secrets.token_hex(32),
        "WORK_CALENDAR_UPLOAD_DIR": str(directory / "uploads"),
        "WORK_CALENDAR_INITIAL_ADMIN_PASSWORD": secrets.token_urlsafe(24),
        "WORK_CALENDAR_LOG_LEVEL": "ERROR",
        "PYTHONNOUSERSITE": "1",
        "PYTHONUTF8": "1",
        "TMP": str(directory),
        "TEMP": str(directory),
        "TMPDIR": str(directory),
    })
    return env


def run(command: list[str], env: dict[str, str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command, cwd=cwd, env=env, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=600,
    )


def require_success(result: subprocess.CompletedProcess[str], label: str) -> None:
    if result.returncode:
        raise RuntimeError(f"{label} failed (exit {result.returncode})\n{result.stdout}{result.stderr}")
    print(f"{label}: PASS")


def verify_backend(env: dict[str, str]) -> None:
    result = run(
        [sys.executable, "-s", "-m", "unittest", "discover", "-s", ".", "-p", "test*.py", "-v"],
        env, ROOT / "backend",
    )
    require_success(result, "Backend API, performance and Chromium regression")
    output = result.stdout + result.stderr
    count = re.search(r"Ran (\d+) tests? in ([\d.]+)s", output)
    if count is None or int(count.group(1)) == 0:
        raise RuntimeError("Backend verification discovered no executed tests")
    if re.search(r"skipped=([1-9]\d*)", output):
        raise RuntimeError("Backend verification contains skipped tests")
    print(f"BACKEND_TESTS={count.group(1)} DURATION_SECONDS={count.group(2)}")
    require_success(run([sys.executable, "-s", "-m", "compileall", "-q", "backend", "scripts"], env), "Python compilation")


def verify_frontend(env: dict[str, str]) -> None:
    script = ROOT / "web" / "app.js"
    if not script.is_file():
        raise RuntimeError("Required web/app.js is missing")
    require_success(run(["node", "--check", str(script)], env), "web/app.js syntax")


def verify_whitespace(env: dict[str, str]) -> None:
    require_success(run(["git", "diff", "--check"], env), "Tracked whitespace")
    result = run(["git", "ls-files", "--others", "--exclude-standard", "-z"], env)
    require_success(result, "Untracked file inventory")
    checked = 0
    for relative in result.stdout.split("\0"):
        if not relative:
            continue
        path = ROOT / relative
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        checked += 1
        check = run(["git", "diff", "--no-index", "--check", "--", "/dev/null", str(path)], env)
        if check.returncode not in (0, 1) or check.stdout.strip():
            raise RuntimeError(f"Untracked whitespace failed: {relative}\n{check.stdout}{check.stderr}")
    print(f"Untracked text whitespace: PASS ({checked} files)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("all", "backend", "frontend"), default="all")
    args = parser.parse_args(argv)
    if Path(sys.prefix).name != "shared_calendar":
        print("Use: conda run --no-capture-output -n shared_calendar python -s scripts/verify.py", file=sys.stderr)
        return 2
    parent = Path(os.environ.get("TMPDIR") or tempfile.gettempdir())
    parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix="calendar-verify-", dir=parent) as temporary:
            env = isolated_environment(Path(temporary))
            if args.mode in ("all", "backend"):
                verify_backend(env)
            if args.mode in ("all", "frontend"):
                verify_frontend(env)
            verify_whitespace(env)
        print(f"VERIFICATION_PASS mode={args.mode}; disposable test resources removed")
        return 0
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        print(f"VERIFICATION_FAILED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
