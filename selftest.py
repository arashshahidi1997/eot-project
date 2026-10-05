"""Environment self-test — The Agentic Research Workflow (Days 1–2).

    pixi run selftest

Exit 0 = every required tool is present. WARN lines don't fail the run.
"""

import importlib
import shutil
import subprocess
import sys

fails = 0


def report(name, status, detail):
    global fails
    fails += status == "FAIL"
    print(f"  [{status}] {name:<10} {detail}")


def first_line(*cmd):
    out = subprocess.run(cmd, capture_output=True, text=True, check=False)
    lines = (out.stdout or out.stderr).strip().splitlines()
    return lines[0] if lines else ""


def check_cmd(name, *version_cmd):
    if shutil.which(version_cmd[0]):
        report(name, "PASS", first_line(*version_cmd))
    else:
        report(name, "FAIL", "not found - run `pixi install`, then `pixi run selftest`")


print("Agentic Research Workflow - self-test")

ok = sys.version_info >= (3, 11)
report("python", "PASS" if ok else "FAIL", sys.version.split()[0])

check_cmd("pixi", "pixi", "--version")
check_cmd("git", "git", "--version")
check_cmd("marimo", "marimo", "--version")
check_cmd("snakemake", "snakemake", "--version")

try:
    libs = [importlib.import_module(m) for m in ("numpy", "pandas", "altair")]
    importlib.import_module("matplotlib")
    importlib.import_module("vl_convert")  # altair → PNG export
    report("libs", "PASS", ", ".join(f"{m.__name__} {m.__version__}" for m in libs))
except ImportError as err:
    report("libs", "FAIL", str(err))

email = shutil.which("git") and first_line("git", "config", "--get", "user.email")
if email and "@" in email:
    report("git id", "PASS", email)
else:
    report("git id", "WARN", "unset - git config --global user.email you@example.com")

print()
print("All required tools present." if not fails else f"{fails} check(s) failed.")
sys.exit(1 if fails else 0)
