"""Check a generated deck against its source material.

    python scripts/deck_check.py output/deck.pptx --source inputs/outline.docx [--source more.xlsx ...]

Reports, per deck:
  1. Numbers on slides that never appear in the sources  -> possible fabrication
  2. Share of source numbers that made it into the deck  -> data coverage
  3. Slides whose text fills little of the slide          -> too sparse
  4. Leftover template placeholders ([...], xx, Lorem)    -> unfinished
  5. Claims / quoted terms / vocabulary not in the sources -> possible invention
  6. Same template many slides in a row, or no chart      -> monotonous layout
  7. Body text below 12pt                                  -> hard to read
  8. Footer "Source:" misuse (caption as source, wrong language)

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


# ---------- invention, layout, readability, sources ----------

# Claim types the skill forbids adding; flagged when absent from the sources.
RISK_TERMS = (
    "#1", "no. 1", "number one", "market leader", "first-ever", "first ever",
    "partnership", "partner with", "alliance", "joint venture", "exclusive",
    "acquire", "acquisition", "patent", "certified", "certification",
    "clinical trial", "fda", "award", "multi-pack", "subscription",
    "flagship store", "pop-up", "guarantee", "official",
)
# Double / curly quotes, or single quotes not used as apostrophes (YNBY's).
_QUOTED = re.compile(r"[\"“]([^\"“”\n]{3,60})[\"”]"
                     r"|(?<![A-Za-z])[‘']([^‘’'\n]{3,60})[’'](?![A-Za-z])")
_WORD = re.compile(r"[A-Za-z][A-Za-z'-]{4,}")
_STOP = set("""
insight insights confidential presentation strengths weaknesses opportunities
threats target channel
about above across action active actual added after again against ahead allow
along already also although always among amount another around based basic
became because become becomes before behind being below best better between
beyond brand brands build building built business capture captures change
changes clear close common company complete content continue core create
creates current daily deeper deliver delivers despite develop direct directly
drive driven drives driving during early either enable enables ensure entire
establish every evolve expand expanding expected experience extend extends
fast focus focused follow force forces forward framework fully further gain
gains generate given going great greater growing growth heavy helps higher
highly immediate improve include including increase increasing inside instead
integrate intense issue issues key large largest later launch launches lead
leader leaders leading leads level leverage leveraging local long longer major
make makes making market markets means measure modern moment moments month more
most moving multiple needs never next north offer offers often online order
other others overall paired pairing performance place plan player players point
points position positioning positions power premium pressure primary priority
proof provide provides putting quality quickly range rapid rapidly reach ready
really reduce region remain replace requires result results right rising risk
rivals robust scale secure segment segments serve service shift shifts short
should shows signal since single slide small solid solution specific speed
stand standing start state still strategic strategy stream strong strongly
structural structure support sustained target targeted targets their there
these thing those three through throughout today toward towards track trend
trends under unique unlock until upgrade value values very visible where which
while whole wider winning within without works would years young youth
""".split())


def _stem(w: str) -> str:
    w = w.lower().strip("'-")
    for suf, rep in (("ies", "y"), ("ing", ""), ("ed", ""), ("es", ""),
                     ("s", ""), ("ly", "")):
        if len(w) > 5 and w.endswith(suf):
            return w[: -len(suf)] + rep
    return w


def _norm_text(t: str) -> str:
    return re.sub(r"[^a-z0-9#%\u2e80-\u9fff]+", " ", t.lower())


def new_content(text: str, src_norm: str, src_stems: set[str]):
    """(risk claims, quoted phrases, novel words) on a slide vs. the sources."""
    norm = _norm_text(text)
    risk = sorted({t for t in RISK_TERMS
                   if _norm_text(t).strip() in norm and _norm_text(t).strip() not in src_norm})
    def stemmed(t):
        return " ".join(_stem(w) for w in _norm_text(t).split())
    src_stemmed = stemmed(src_norm)
    found = [a or b for a, b in _QUOTED.findall(text)]
    quoted = sorted({q.strip() for q in found
                     if stemmed(q) and stemmed(q) not in src_stemmed})
    words = sorted({w.lower() for w in _WORD.findall(text)
                    if w.lower() not in _STOP and _stem(w) not in src_stems})
    return risk, quoted, words


_CHART_TEMPLATES = {"chart", "column_comparison", "column_simple_growth",
                    "column_split_growth", "column_historic_forecast",
                    "stacked_column_chart", "grouped_column_chart", "line_chart",
                    "bubble_chart", "bubble_chart_takeaways", "growth_share"}
_FAMILY = {"swot": "card_grid"}


def template_of(slide):
    name = slide._element.cSld.get("name") or ""
    return name[3:] if name.startswith("mp:") else None


def has_chart(slide) -> bool:
    return any(getattr(sh, "has_chart", False) and sh.has_chart
               for sh in _iter_shapes(slide.shapes)) or \
        template_of(slide) in _CHART_TEMPLATES


def body_size(slide, slide_h) -> float | None:
    """Dominant font size of body text (ignores title, footer, short labels)."""
    from collections import Counter
    sizes = Counter()
    top_cut, bottom_cut = Emu(int(slide_h * 0.14)), Emu(int(slide_h * 0.93))
    for sh in _iter_shapes(slide.shapes):
        if not sh.has_text_frame or sh.top is None:
            continue
        if sh.top < top_cut or sh.top > bottom_cut:
            continue
        for p in sh.text_frame.paragraphs:
            for r in p.runs:
                if r.font.size and len(r.text) > 15 and r.font.size.pt < 20:
                    sizes[r.font.size.pt] += len(r.text)
    return sizes.most_common(1)[0][0] if sizes else None


_SRC_LABEL = re.compile(r"^(Source:|Sources:|资料来源：|來源：|출처:|出典：)\s*(.*)$")


def source_issues(slide, deck_is_cjk: bool):
    out = []
    texts = [tf.text.strip() for tf, _ in _frames(slide) if tf.text.strip()]
    for t in texts:
        m = _SRC_LABEL.match(t)
        if not m:
            continue
        label, value = m.group(1), m.group(2).strip()
        if CJK.search(label) and not deck_is_cjk:
            out.append(f"label {label!r} in a non-CJK deck (use make_theme(lang='en'))")
        if value:
            others = [_norm_text(x) for x in texts if x != t]
            v = _norm_text(value).strip()
            if v and any(v in o for o in others):
                out.append(f"source {value!r} repeats a caption/title on the slide — "
                           "a table name is not a source; use source=\"\"")
    return out


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
    src_all = ""
    for s in args.source:
        t = source_text(Path(s))
        src_all += "\n" + t
        src_nums |= numbers(t)
    src_norm = _norm_text(src_all)
    src_stems = {_stem(w) for w in _WORD.findall(src_all)}
    all_text = "\n".join(slide_text(s) for s in prs.slides)
    deck_is_cjk = len(CJK.findall(all_text)) > 0.2 * max(len(re.findall(r"\w", all_text)), 1)

    print(f"Deck: {args.deck}  ({len(prs.slides)} slides)")
    deck_nums_all: set[str] = set()
    sparse, leftovers, invented = [], [], []
    risky, quoted_new, novel, small, src_bad = [], [], [], [], []
    templates = []
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
        if ratio < args.sparse and i > 1 and not has_chart(slide):
            sparse.append((i, ratio))
        if args.source:
            risk, quoted, words = new_content(text, src_norm, src_stems)
            if risk:
                risky.append((i, risk))
            if quoted:
                quoted_new.append((i, quoted))
            if words:
                novel.append((i, words))
        bs = body_size(slide, sh)
        if bs is not None and bs < 12 and i > 1:
            small.append((i, bs))
        issues = source_issues(slide, deck_is_cjk)
        if issues:
            src_bad.append((i, issues))
        templates.append(template_of(slide))
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

    print(f"\n[3] Sparse slides (text fill < {args.sparse:.0%}; chart slides exempt; "
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

    if args.source:
        print("\n[5] Content not in the sources:")
        print("  a) forbidden claim types (new targets / partners / formats ...) — remove or trace:")
        if risky:
            flagged = True
            for i, r in risky:
                print(f"     slide {i}: {', '.join(r)}")
        else:
            print("     none")
        print("  b) quoted terms not in the sources — remove or trace:")
        if quoted_new:
            flagged = True
            for i, q in quoted_new:
                print(f"     slide {i}: {'; '.join(q)}")
        else:
            print("     none")
        n_novel = sum(len(w) for _, w in novel)
        print(f"  c) vocabulary not in the sources ({n_novel} words) — review each slide;"
              " delete points that add facts, keep plain explanation:")
        for i, ws in novel:
            shown = ", ".join(ws[:14]) + (" ..." if len(ws) > 14 else "")
            print(f"     slide {i} ({len(ws)}): {shown}")

    print("\n[6] Layout variety:")
    known = [t for t in templates if t]
    if not known:
        print("  (deck has no template records — built outside PresentationBuilder)")
    else:
        run_t, run_n, start, runs = None, 0, 0, []
        for i, t in enumerate(templates + [None], start=1):
            fam = _FAMILY.get(t, t)
            if fam is not None and fam == run_t:
                run_n += 1
            else:
                if run_t and run_n > 3:
                    runs.append((run_t, start, start + run_n - 1))
                run_t, run_n, start = fam, 1, i
        for t, a, b in runs:
            flagged = True
            print(f"  slides {a}-{b}: {b - a + 1} x {t} in a row (max 3) — re-express one")
        n_charts = sum(has_chart(s) for s in prs.slides)
        if args.source and len(src_nums) >= 10 and n_charts == 0:
            flagged = True
            print("  no chart, although the sources contain numeric data — chart the numeric tables")
        if not runs and not (args.source and len(src_nums) >= 10 and n_charts == 0):
            print(f"  ok ({n_charts} chart slide(s))")

    print("\n[7] Small body text (< 12pt):")
    if small:
        flagged = True
        for i, bs in small:
            print(f"  slide {i}: {bs:g}pt — shorten bullets, drop subtitle/insight, or split")
    else:
        print("  none")

    print("\n[8] Footer source line:")
    if src_bad:
        flagged = True
        for i, iss in src_bad:
            for x in iss:
                print(f"  slide {i}: {x}")
    else:
        print("  ok")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
