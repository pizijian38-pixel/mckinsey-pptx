"""Check a generated deck against its source material.

    python scripts/deck_check.py output/deck.pptx --source inputs/outline.docx [--source more.xlsx ...]

Reports, per deck:
  1. Numbers on slides that never appear in the sources  -> possible fabrication
  2. Share of source numbers that made it into the deck  -> data coverage
  3. Slides whose text fills little of the slide          -> too sparse
  4. Leftover template placeholders ([...], xx, Lorem)    -> unfinished

Sources: .docx .pptx .md .txt .csv .xlsx (.pdf if pypdf is installed).
Exit code 1 if anything is flagged, so a build script can gate on it.
"""
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

from pptx import Presentation
from pptx.util import Emu

# A leading sign counts only when it isn't a range dash ("30%-50%", "12-18").
NUM = re.compile(r"(?:(?<![\w.%)])[-+−])?(?<![\w.])\d{1,3}(?:,\d{3})+(?:\.\d+)?"
                 r"|(?:(?<![\w.%)])[-+−])?(?<![\w.])\d+(?:\.\d+)?")
# Outline scaffolding ("Slide 13:", "Table 2") is not data.
SCAFFOLD = re.compile(r"\b(?:slide|table|chart|figure|page|section|第)\s*\d+\b", re.I)
PLACEHOLDER = re.compile(r"\[(?:insert|description|key takeaway|lorem)[^\]]*\]|\blorem ipsum\b|^xx$|\b1\. xx\b|Source: xx",
                         re.I)
CJK = re.compile(r"[⺀-鿿가-힯＀-￯]")


# ---------- text extraction ----------

def _docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf8")
    xml = re.sub(r"</w:p>|</w:tc>", "\n", xml)
    return re.sub(r"<[^>]+>", "", xml)


def _pptx_text(path: Path) -> str:
    return "\n".join(t for _, t in _slide_texts(Presentation(str(path))))


def _xlsx_text(path: Path) -> str:
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    out = []
    for ws in wb.worksheets:
        for row in ws.iter_rows(values_only=True):
            out.append(" ".join("" if v is None else str(v) for v in row))
    return "\n".join(out)


def _pdf_text(path: Path) -> str:
    try:
        import pypdf
    except ImportError:
        print(f"  ! skipped {path.name}: pip install pypdf to read PDFs")
        return ""
    return "\n".join(p.extract_text() or "" for p in pypdf.PdfReader(str(path)).pages)


def source_text(path: Path) -> str:
    return SCAFFOLD.sub(" ", _raw_source_text(path))


def _raw_source_text(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".docx":
        return _docx_text(path)
    if ext == ".pptx":
        return _pptx_text(path)
    if ext in (".xlsx", ".xlsm"):
        return _xlsx_text(path)
    if ext == ".pdf":
        return _pdf_text(path)
    return path.read_text(encoding="utf8", errors="ignore")


def _iter_shapes(shapes):
    for sh in shapes:
        if sh.shape_type == 6:  # group
            yield from _iter_shapes(sh.shapes)
        else:
            yield sh


def _frames(slide):
    """(text_frame, width_emu) for every text-bearing shape and table cell."""
    for sh in _iter_shapes(slide.shapes):
        if sh.has_text_frame:
            yield sh.text_frame, sh.width or 0
        if getattr(sh, "has_table", False) and sh.has_table:
            cols = sh.table.columns
            for row in sh.table.rows:
                for ci, cell in enumerate(row.cells):
                    yield cell.text_frame, cols[ci].width


def _chart_text(slide) -> str:
    """Category labels and values of native charts (they hold no text frames)."""
    out = []
    for sh in _iter_shapes(slide.shapes):
        if getattr(sh, "has_chart", False) and sh.has_chart:
            for plot in sh.chart.plots:
                out += [str(c) for c in plot.categories]
                for series in plot.series:
                    out += [str(v) for v in series.values if v is not None]
    return "\n".join(out)


def slide_text(slide) -> str:
    return "\n".join([tf.text for tf, _ in _frames(slide)] + [_chart_text(slide)])


def _slide_texts(prs):
    for i, slide in enumerate(prs.slides, start=1):
        yield i, slide_text(slide)


# ---------- checks ----------

def _norm(n: str) -> str:
    n = n.replace(",", "").replace("−", "-").lstrip("+")
    if "." in n:
        n = n.rstrip("0").rstrip(".")
    return n


def numbers(text: str) -> set[str]:
    return {_norm(m) for m in NUM.findall(text)}


def fill_ratio(slide, slide_w, slide_h) -> float:
    """Estimated share of the slide covered by text ink (0-1)."""
    ink = 0.0
    for tf, width in _frames(slide):
        for p in tf.paragraphs:
            for r in p.runs:
                size = r.font.size.pt if r.font.size else 12
                chars = sum(1.0 if CJK.match(c) else 0.55 for c in r.text)
                ink += chars * size * size * 1.25  # pt^2
    area = Emu(slide_w).pt * Emu(slide_h).pt
    return ink / area if area else 0.0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("deck")
    ap.add_argument("--source", action="append", default=[],
                    help="source file the deck was built from (repeatable)")
    ap.add_argument("--sparse", type=float, default=0.12,
                    help="flag slides whose text fill ratio is below this")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="print every slide's text fill ratio")
    args = ap.parse_args(argv)

    prs = Presentation(args.deck)
    sw, sh = prs.slide_width, prs.slide_height
    flagged = False

    src_nums: set[str] = set()
    for s in args.source:
        src_nums |= numbers(source_text(Path(s)))

    print(f"Deck: {args.deck}  ({len(prs.slides)} slides)")
    deck_nums_all: set[str] = set()
    sparse, leftovers, invented = [], [], []
    for i, slide in enumerate(prs.slides, start=1):
        text = slide_text(slide)
        nums = numbers(text)
        # page number and axis zero are chrome, not content
        nums.discard(str(i))
        nums.discard("0")
        deck_nums_all |= nums
        if args.source:
            new = sorted(n for n in nums if n not in src_nums)
            if new:
                invented.append((i, new))
        ratio = fill_ratio(slide, sw, sh)
        if args.verbose:
            print(f"  slide {i:>2}: fill {ratio:.1%}")
        if ratio < args.sparse and i > 1:
            sparse.append((i, ratio))
        hits = {m.group(0) for line in text.splitlines()
                for m in [PLACEHOLDER.search(line.strip())] if m}
        if hits:
            leftovers.append((i, sorted(hits)))

    if args.source:
        print("\n[1] Numbers not found in the sources (verify or remove):")
        if invented:
            flagged = True
            for i, ns in invented:
                print(f"  slide {i}: {', '.join(ns)}")
        else:
            print("  none")
        used = src_nums & deck_nums_all
        cov = len(used) / len(src_nums) if src_nums else 1.0
        print(f"\n[2] Source numbers used in the deck: {len(used)}/{len(src_nums)} ({cov:.0%})")
        missing = sorted(src_nums - deck_nums_all, key=lambda x: (len(x), x))
        if missing:
            print(f"  not used: {', '.join(missing[:60])}{' ...' if len(missing) > 60 else ''}")

    print(f"\n[3] Sparse slides (text fill < {args.sparse:.0%}; "
          "ignore cover / divider / closing slides):")
    if sparse:
        flagged = True
        for i, r in sparse:
            print(f"  slide {i}: {r:.1%}")
    else:
        print("  none")

    print("\n[4] Leftover placeholders:")
    if leftovers:
        flagged = True
        for i, hits in leftovers:
            print(f"  slide {i}: {hits}")
    else:
        print("  none")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
