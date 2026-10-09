"""Build, check and render a deck in one command (Windows, macOS, Linux).

    python scripts/run_deck.py output/build_<slug>.py --source <outline.docx> [--source ...]
    python scripts/run_deck.py output/build_<slug>.py --no-render      # skip the previews
    python scripts/run_deck.py output/build_<slug>.py --deck output/<slug>.pptx

1. build  - runs the build script with this Python; prints its WARNING lines.
2. check  - runs deck_check.py on the .pptx the build wrote (with the sources).
3. render - .pptx -> PDF with LibreOffice (found on PATH or in the usual install
            folders), waits for the PDF, then PDF -> PNG with pdftoppm or PyMuPDF,
            plus contact_sheet.png (all slides on one image) in
            <deck folder>/preview_<slug>/.

Exit status 0 = build clean and checker clean; 1 = something to fix (see the
summary at the end). A render that cannot run is reported but does not change the
exit status - the .pptx itself is fine.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent

_SOFFICE_CANDIDATES = [
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "/usr/bin/soffice", "/usr/local/bin/soffice", "/opt/libreoffice/program/soffice",
    "/snap/bin/libreoffice",
]


# ---------------------------------------------------------------- build

def run_build(script: Path):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    t0 = time.time()
    p = subprocess.run([sys.executable, str(script)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    if p.stdout.strip():
        print(p.stdout.rstrip())
    if p.stderr.strip():
        print(p.stderr.rstrip())
    warnings = [l for l in (p.stdout + "\n" + p.stderr).splitlines() if "WARNING" in l]
    return p.returncode, warnings, t0


def _pptx_files(root: Path, depth: int):
    """*.pptx under root, at most `depth` folders down (never a whole disk)."""
    try:
        entries = list(root.iterdir())
    except OSError:
        return
    for p in entries:
        if p.is_file() and p.suffix.lower() == ".pptx" and not p.name.startswith("~$"):
            yield p
        elif depth > 0 and p.is_dir() and not p.name.startswith((".", "preview_")) \
                and p.name not in ("node_modules", "__pycache__", "venv", ".venv"):
            yield from _pptx_files(p, depth - 1)


def find_deck(script: Path, since: float):
    """The .pptx written by the build: newest file modified since the build began,
    next to the script (2 levels down) or in the working directory / its output/."""
    places = [(script.resolve().parent, 2), (Path.cwd(), 0), (Path.cwd() / "output", 1)]
    hits = set()
    for root, depth in places:
        for p in _pptx_files(root, depth):
            try:
                if p.stat().st_mtime >= since - 1:
                    hits.add(p.resolve())
            except OSError:
                pass
    return sorted(hits, key=lambda p: p.stat().st_mtime, reverse=True)


# ---------------------------------------------------------------- render

def find_soffice():
    for name in ("soffice", "libreoffice", "soffice.exe"):
        w = shutil.which(name)
        if w:
            return w
    for c in _SOFFICE_CANDIDATES:
        if Path(c).exists():
            return c
    return None


def _wait_for(path: Path, timeout: float = 60.0) -> bool:
    """True once `path` exists, is non-empty and has stopped growing."""
    end, last = time.time() + timeout, -1
    while time.time() < end:
        if path.exists():
            size = path.stat().st_size
            if size > 0 and size == last:
                return True
            last = size
        time.sleep(1.0)
    return path.exists() and path.stat().st_size > 0


def to_pdf(deck: Path, outdir: Path):
    soffice = find_soffice()
    if not soffice:
        return None, ("LibreOffice not found (install it, or add soffice to PATH; on Windows "
                      r"it is usually C:\Program Files\LibreOffice\program\soffice.exe)")
    pdf = outdir / (deck.stem + ".pdf")
    if pdf.exists():
        pdf.unlink()
    # A private profile lets the conversion run while LibreOffice is open elsewhere.
    profile = Path(tempfile.gettempdir()) / "mckinsey_pptx_lo_profile"
    cmd = [soffice, f"-env:UserInstallation={profile.as_uri()}", "--headless",
           "--convert-to", "pdf", "--outdir", str(outdir), str(deck)]
    for attempt in (1, 2):
        try:
            subprocess.run(cmd, capture_output=True, timeout=300)
        except subprocess.TimeoutExpired:
            pass
        if _wait_for(pdf, 60 if attempt == 1 else 90):
            return pdf, None
    return None, f"LibreOffice produced no PDF ({soffice})"


def to_pngs(pdf: Path, outdir: Path, dpi: int):
    pdftoppm = shutil.which("pdftoppm")
    if pdftoppm:
        subprocess.run([pdftoppm, "-png", "-r", str(dpi), str(pdf), str(outdir / "slide")],
                       capture_output=True, timeout=300)
        pngs = sorted(outdir.glob("slide-*.png"))
        if pngs:
            return pngs, None
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return [], ("no PDF rasteriser: install poppler (pdftoppm) or run "
                    f"'{Path(sys.executable).name} -m pip install pymupdf'. The PDF is at {pdf}")
    doc = fitz.open(str(pdf))
    width = len(str(doc.page_count))
    pngs = []
    for i, page in enumerate(doc, start=1):
        p = outdir / f"slide-{i:0{max(width, 2)}d}.png"
        page.get_pixmap(dpi=dpi).save(str(p))
        pngs.append(p)
    return pngs, None


def contact_sheet(pngs, out: Path, cols: int = 3, thumb_w: int = 640):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return None
    ims = [Image.open(p).convert("RGB") for p in pngs]
    if not ims:
        return None
    th = int(thumb_w * ims[0].height / ims[0].width)
    rows = (len(ims) + cols - 1) // cols
    pad = 12
    sheet = Image.new("RGB", (cols * (thumb_w + pad) + pad, rows * (th + pad + 22) + pad),
                      "white")
    draw = ImageDraw.Draw(sheet)
    for k, im in enumerate(ims):
        r, c = divmod(k, cols)
        x, y = pad + c * (thumb_w + pad), pad + r * (th + pad + 22)
        draw.text((x, y), f"Slide {k + 1}", fill=(40, 40, 40))
        im = im.resize((thumb_w, th))
        sheet.paste(im, (x, y + 18))
        draw.rectangle([x - 1, y + 17, x + thumb_w, y + 18 + th], outline=(190, 190, 190))
    sheet.save(out)
    return out


def render(deck: Path, dpi: int):
    outdir = deck.parent / f"preview_{deck.stem}"
    outdir.mkdir(parents=True, exist_ok=True)
    for old in list(outdir.glob("slide-*.png")) + [outdir / "contact_sheet.png"]:
        try:
            old.unlink()
        except OSError:
            pass
    pdf, err = to_pdf(deck, outdir)
    if err:
        return outdir, [], None, err
    pngs, err = to_pngs(pdf, outdir, dpi)
    sheet = contact_sheet(pngs, outdir / "contact_sheet.png") if pngs else None
    return outdir, pngs, sheet, err


# ---------------------------------------------------------------- main

def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("build_script")
    ap.add_argument("--source", action="append", default=[],
                    help="source file the deck is built from (repeatable)")
    ap.add_argument("--deck", help="the .pptx the build writes (found automatically if omitted)")
    ap.add_argument("--no-render", action="store_true", help="skip PDF / PNG previews")
    ap.add_argument("--dpi", type=int, default=80)
    args = ap.parse_args(argv)

    script = Path(args.build_script)
    if not script.exists():
        print(f"[run_deck] build script not found: {script}")
        return 1
    missing = [s for s in args.source if not Path(s).exists()]
    if missing:
        print(f"[run_deck] source file(s) not found: {', '.join(missing)} — pass the real path "
              "of the attached file (do not retype it).")
        return 1

    print("== 1. build " + "=" * 60)
    code, warnings, t0 = run_build(script)
    if code != 0:
        print(f"\n== summary ==\nbuild : FAILED (exit {code}) — read the traceback above")
        return 1
    if args.deck:
        deck = Path(args.deck)
    else:
        decks = find_deck(script, t0)
        if not decks:
            print("\n== summary ==\nbuild : ran, but no new .pptx was found — pass --deck")
            return 1
        deck = decks[0]
        if len(decks) > 1:
            print(f"[run_deck] several decks written; checking the newest: {deck}")

    print("\n== 2. check " + "=" * 60)
    sys.path.insert(0, str(HERE))
    import deck_check
    check_argv = [str(deck)] + sum((["--source", s] for s in args.source), [])
    flagged = deck_check.main(check_argv)

    render_line = "skipped (--no-render)"
    if not args.no_render:
        print("\n== 3. render " + "=" * 59)
        outdir, pngs, sheet, err = render(deck, args.dpi)
        if pngs:
            render_line = (f"{len(pngs)} PNG(s) in {outdir}"
                           + (f"\n        contact sheet: {sheet}" if sheet else ""))
        else:
            render_line = f"not done — {err}. The deck itself is fine; say it was not visually verified."
        print(render_line)

    print("\n== summary " + "=" * 61)
    print(f"deck  : {deck}")
    print("build : " + ("ok, no warnings" if not warnings else
                        f"{len(warnings)} WARNING(s) — fix each (see above)"))
    print("check : " + ("clean" if not flagged else
                        "items to fix — see sections [1] [4] [5a/b] [6]-[10] above") +
          "  ([2] [3] [5c] [11] are advisory)")
    print(f"render: {render_line}")
    return 1 if (warnings or flagged) else 0


if __name__ == "__main__":
    sys.exit(main())
