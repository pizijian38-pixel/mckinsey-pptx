"""Build every smoke-test deck, run the checker on each, print a summary.

    python tests/smoke/run.py              # build + check
    python tests/smoke/run.py --render     # also render PNG contact sheets (needs soffice, pdftoppm)

Each scenario folder has build.py exposing build(out_dir), SOURCES and
DERIVED (numbers the build computes from the source on purpose). A scenario
passes when the build prints no warnings and the checker reports nothing
beyond DERIVED numbers.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import deck_check  # noqa: E402


def load(folder: Path):
    spec = importlib.util.spec_from_file_location(folder.name, folder / "build.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--out", default=str(HERE / "output"))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    failed = 0
    for folder in sorted(p for p in HERE.iterdir() if (p / "build.py").exists()):
        mod = load(folder)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            deck = mod.build(out)
        report = io.StringIO()
        argv = [str(deck)] + sum((["--source", str(s)] for s in mod.SOURCES), [])
        with contextlib.redirect_stdout(report):
            deck_check.main(argv)
        text = report.getvalue()
        # strip declared derived numbers from section [1]
        issues = []
        section = None
        for line in text.splitlines():
            if line.startswith("["):
                section = line.split("]")[0] + "]"
                continue
            line_s = line.strip()
            if not line_s or line_s in ("none", "ok") or line_s.startswith(
                    ("a)", "b)", "c)", "not used:", "->")):
                continue
            if section == "[5]" and "(" in line_s and line_s.startswith("slide") and ":" in line_s \
                    and "vocabulary" not in line_s and line_s.split(":")[0].endswith(")"):
                continue      # [5c] vocabulary listing is advisory
            if section == "[1]":
                nums = [n.strip() for n in line_s.split(":", 1)[1].split(",")]
                nums = [n for n in nums if n not in mod.DERIVED]
                if not nums:
                    continue
                line_s = line_s.split(":", 1)[0] + ": " + ", ".join(nums)
            if section in ("[2]", "[3]", "[11]") or line_s.startswith("Deck:") or line_s.startswith("("):
                continue          # [2] coverage is shown in the summary; [3] and [11] are advisory
            if section == "[6]" and line_s.startswith("ok"):
                continue
            issues.append(f"{section} {line_s}")
        warnings = [w for w in err.getvalue().splitlines() if "WARNING" in w]
        status = "PASS" if not issues and not warnings else "FAIL"
        failed += status == "FAIL"
        cov = next((l for l in text.splitlines() if l.startswith("[2]")), "[2] n/a (brief mode)")
        print(f"{status}  {folder.name:<16} {deck.name}  {cov[4:]}")
        for w in warnings:
            print(f"      build: {w}")
        for i in issues:
            print(f"      check: {i}")
        if args.render:
            subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(out), str(deck)],
                           capture_output=True)
            pdf = deck.with_suffix(".pdf")
            subprocess.run(["pdftoppm", "-jpeg", "-r", "50", str(pdf), str(out / deck.stem)], capture_output=True)
    # regression tests for bugs found on real decks
    reg = subprocess.run([sys.executable, str(ROOT / "tests" / "test_regressions.py")],
                         capture_output=True, text=True)
    for line in reg.stdout.splitlines():
        print(line)
    failed += reg.returncode != 0
    print(f"\n{'all passed' if not failed else f'{failed} scenario(s) failed'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
