"""Regression tests for bugs found while building real decks.

    python tests/test_regressions.py      (or: pytest tests/test_regressions.py)
"""
import contextlib
import io
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from pptx import Presentation  # noqa: E402

from mckinsey_pptx import PresentationBuilder  # noqa: E402
import deck_check  # noqa: E402


def _body_sizes(slide):
    sizes = []
    for sh in slide.shapes:
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.size and len(r.text) > 15:
                        sizes.append(r.font.size.pt)
    return sizes


def test_cards_in_wide_short_region_stay_readable():
    """Three icon cards stacked in a wide composite column used to shrink the
    body to 10pt although each body is one short line (coal ESG deck, slide 5)."""
    b = PresentationBuilder()
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        b.add("composite", title="Wide, short cards",
              columns=[{"type": "chart", "chart_type": "bar", "heading": "Share, %",
                        "categories": ["Global", "EU", "US"],
                        "series": [{"name": "Share", "values": [70, 69, 59]}]},
                       {"type": "cards", "columns": 1, "cards": [
                           {"title": "Short-term reversals for energy security", "icon": "zap",
                            "body": "Gas price spikes, geopolitics and weather force grids back to "
                                    "coal — e.g. India ordered idle plants to full capacity in heatwaves"},
                           {"title": "Delayed decommissioning in mature markets", "icon": "clock",
                            "body": "EU retirements postponed amid the gas supply crisis; US delays "
                                    "driven by data-centre and electrification load growth"},
                           {"title": "Corporate greenhushing", "icon": "message",
                            "body": "Utilities say less about ESG and frame transition spending as "
                                    "operational resilience, cost efficiency and system reliability"}]}],
              widths=[0.9, 1.25], insight="Energy security frequently overrides near-term "
                                          "emission goals; commitments and execution drift apart")
    assert "WARNING" not in err.getvalue(), err.getvalue()
    sizes = _body_sizes(b.prs.slides[-1])
    assert sizes and min(sizes) >= 12, sizes


def test_card_grid_regular_layout_unchanged():
    """2x2 card grids keep the stacked layout (icon + header above the body)."""
    b = PresentationBuilder()
    b.add("card_grid", title="Four cards",
          cards=[{"title": f"Card {i}", "icon": "check", "bullets": ["One point", "Another point"]}
                 for i in range(4)])
    sizes = _body_sizes(b.prs.slides[-1])
    assert not sizes or min(sizes) >= 12


def _docx(path: Path, text: str):
    xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
           f'<w:body><w:p><w:r><w:t>{text}</w:t></w:r></w:p></w:body></w:document>')
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("word/document.xml", xml)


def test_docx_source_entities_are_decoded():
    """Quotes and ampersands in a .docx source are XML entities; the checker
    flagged “Greener & Smarter” as a quoted term not in the source."""
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "outline.docx"
        _docx(src, "Banpu executes &quot;Greener &amp; Smarter&quot; strategies")
        text = deck_check._docx_text(src)
        assert '"Greener & Smarter"' in text, text
        b = PresentationBuilder()
        b.add("card_grid", title="Banpu strategy",
              cards=[{"title": "Strategy", "body": "Banpu executes “Greener & Smarter” strategies"}],
              source="", footnote="")
        deck = Path(d) / "deck.pptx"
        b.save(str(deck))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            deck_check.main([str(deck), "--source", str(src)])
        report = out.getvalue()
        section = report.split("b) quoted terms")[1].split("c) vocabulary")[0]
        assert "Greener" not in section, section
        assert " amp" not in report, report


def test_catalog_examples_run():
    """Every python example in CATALOG.md must run as written: the agent copies
    them. Old examples used `...` as a placeholder (TypeError / AttributeError)."""
    import os
    import re
    cat = (ROOT / "mckinsey_pptx" / "agent" / "CATALOG.md").read_text(encoding="utf8")
    blocks = re.findall(r"```python\n(.*?)```", cat, re.S)
    assert len(blocks) > 50, len(blocks)
    bad = [blk[:80] for blk in blocks if re.search(r"(?<![.\w])\.\.\.(?![.\w])", blk)]
    assert not bad, f"'...' placeholder in catalog examples: {bad}"
    failures = []
    with tempfile.TemporaryDirectory() as d:
        cwd = os.getcwd()
        os.chdir(d)
        os.makedirs("output", exist_ok=True)
        try:
            shared = PresentationBuilder(nav=["Overview", "Situation"])
            for blk in blocks:
                if "b.add(" not in blk and "make_theme(" not in blk:
                    continue
                env = {"b": shared}
                err = io.StringIO()
                try:
                    with contextlib.redirect_stderr(err), \
                            contextlib.redirect_stdout(io.StringIO()):
                        exec(blk, env)
                except Exception as e:  # noqa: BLE001
                    failures.append(f"{type(e).__name__}: {e} :: {blk[:70]!r}")
                # examples are copied as-is: they must also build without warnings
                warns = [w for w in err.getvalue().splitlines() if "WARNING" in w]
                if warns:
                    failures.append(f"warning: {warns[0][:160]} :: {blk[:70]!r}")
            shared.save("output/all_examples.pptx")
        finally:
            os.chdir(cwd)
    assert not failures, "\n".join(failures)


def test_no_theme_shadows():
    """Connectors reference theme effect style 1, which python-pptx's default
    theme defines as an outer shadow: every rule and arrow had a drop shadow
    in PowerPoint. The saved deck must contain no shadow effect anywhere."""
    b = PresentationBuilder()
    b.add("cycle", title="Shadows", kind="vicious", steps=["A", "B", "C"], center="X")
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "s.pptx"
        b.save(str(path))
        with zipfile.ZipFile(path) as z:
            hits = [n for n in z.namelist() if n.endswith(".xml")
                    and b"outerShdw" in z.read(n)]
    assert not hits, f"shadow effects in: {hits}"


def _warnings(**kw):
    b = PresentationBuilder()
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        b.add("growth_share", **kw)
    return [w for w in err.getvalue().splitlines() if "WARNING" in w]


def test_focus_follows_title():
    """A title that names one diagram item should put the accent on it: the
    build warns when focus is missing, and when focus names no item."""
    bus = [{"name": "Batteries", "x": 12, "y": 37, "size": 4},
           {"name": "Cables", "x": 70, "y": 6, "size": 5}]
    t = "Batteries are the only question mark worth funding"
    w = _warnings(title=t, bus=bus)
    assert w and "focus='Batteries'" in w[0], w
    assert not _warnings(title=t, bus=bus, focus="Batteries")
    assert not _warnings(title=t, bus=bus, focus=[])          # deliberate opt-out
    assert not _warnings(title="Portfolio is balanced", bus=bus)
    w = _warnings(title=t, bus=bus, focus="Battery")
    assert w and "matches no item" in w[0], w


def test_focus_draws_one_accent():
    """With focus set, exactly the focal bubble is filled in the accent colour."""
    from mckinsey_pptx.theme import DEFAULT_THEME
    acc = str(DEFAULT_THEME.palette.bright_blue)
    bus = [{"name": n, "x": 10 + 15 * i, "y": 5 + 8 * i, "size": 1 + i}
           for i, n in enumerate(["A1", "B2", "C3", "D4"])]
    b = PresentationBuilder()
    b.add("growth_share", title="x", bus=bus, focus="C3")
    fills = [str(sh.fill.fore_color.rgb) for sh in b.prs.slides[0].shapes
             if sh.shape_type == 1 and sh.fill.type == 1 and sh.width == sh.height]
    # one accent bubble (+ one legend dot)
    assert fills.count(acc) == 2, fills


# ---------- data fidelity of the area / width / position charts ----------

def _marks(slide, prefix):
    return {sh.name[len(prefix):]: sh for sh in slide.shapes if sh.name.startswith(prefix)}


def _rel(a, b):
    return abs(a - b) / max(abs(b), 1e-9)


def test_marimekko_area_is_share_of_total():
    """Each segment's area must be its share of the grand total (column width =
    column share, height = share within column)."""
    series = ["A", "B", "C"]
    cols = [{"name": "X", "values": [10, 30, 0]}, {"name": "Y", "values": [5, 5, 5]},
            {"name": "Z", "values": [1, 2, 42]}]
    b = PresentationBuilder()
    b.add("marimekko", title="t", series=series, columns=cols)
    m = _marks(b.prs.slides[0], "mekko:")
    grand = sum(sum(c["values"]) for c in cols)
    assert "X|C" not in m, "zero segment must be omitted, not drawn"
    areas = {k: sh.width * sh.height for k, sh in m.items()}
    tot = sum(areas.values())
    for c in cols:
        for s_, v in zip(series, c["values"]):
            if v:
                assert _rel(areas[f"{c['name']}|{s_}"] / tot, v / grand) < 0.01, (c, s_)


def test_treemap_area_is_value():
    items = [{"name": n, "value": v} for n, v in
             [("a", 50), ("b", 20), ("c", 12), ("d", 9), ("e", 6), ("f", 3)]]
    b = PresentationBuilder()
    b.add("treemap", title="t", items=items)
    m = _marks(b.prs.slides[0], "treemap:")
    tot = sum(sh.width * sh.height for sh in m.values())
    for it in items:
        sh = m[it["name"]]
        assert _rel(sh.width * sh.height / tot, it["value"] / 100) < 0.01, it


def _ribbon_ends(shp):
    """Ribbon thickness at its source and target ends, in EMU."""
    from pptx.oxml.ns import qn
    path = shp._element.find(".//" + qn("a:path"))
    ys = [int(pt.get("y")) for pt in path.iter(qn("a:pt"))]
    sy = shp.height / int(path.get("h"))
    half = len(ys) // 2
    return (ys[-1] - ys[0]) * sy, (ys[half] - ys[half - 1]) * sy


def test_sankey_width_is_value_and_conserved():
    """Node height and ribbon width share one scale; a ribbon is equally thick at
    both ends; a node that loses volume is reported."""
    flows = [{"from": "In", "to": "A", "value": 60}, {"from": "In", "to": "B", "value": 40},
             {"from": "A", "to": "Win", "value": 45}, {"from": "A", "to": "Lose", "value": 15},
             {"from": "B", "to": "Win", "value": 10}, {"from": "B", "to": "Lose", "value": 30}]
    b = PresentationBuilder()
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        b.add("sankey", title="t", flows=flows)
    assert "WARNING" not in err.getvalue(), err.getvalue()
    s = b.prs.slides[0]
    nodes = _marks(s, "sankey-node:")
    k = nodes["In"].height / 100
    assert _rel(nodes["Win"].height, 55 * k) < 0.01 and _rel(nodes["A"].height, 60 * k) < 0.01
    ribbons = _marks(s, "sankey:")
    for f in flows:
        src, dst = _ribbon_ends(ribbons[f"{f['from']} → {f['to']}"])
        assert _rel(src, f["value"] * k) < 0.01 and _rel(dst, f["value"] * k) < 0.01, f
    leak = flows[:-1]                       # B sends on 10 of its 40
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        PresentationBuilder().add("sankey", title="t", flows=leak)
    assert "'B' takes in 40 but sends on 10" in err.getvalue(), err.getvalue()


def test_area_charts_reject_negative_values():
    for kind, kw in (("treemap", {"items": [{"name": "a", "value": 5},
                                             {"name": "b", "value": -1}]}),
                     ("marimekko", {"series": ["s", "t"],
                                    "columns": [{"name": "x", "values": [1, -2]}]}),
                     ("sankey", {"flows": [{"from": "a", "to": "b", "value": -3}]})):
        try:
            PresentationBuilder().add(kind, title="t", **kw)
        except ValueError:
            continue
        raise AssertionError(f"{kind} accepted a negative value")


def test_slopegraph_axes_share_one_scale():
    """Every endpoint, on either axis, sits on one linear value -> y mapping."""
    series = [{"name": n, "start": a, "end": e} for n, a, e in
              [("p", 512, 288), ("q", 376, 264), ("r", 238, 431), ("s", 164, 121)]]
    b = PresentationBuilder()
    b.add("slopegraph", title="t", series=series)
    lines = _marks(b.prs.slides[0], "slope:")
    pts = []
    for sr in series:
        ln = lines[sr["name"]]
        pts += [(sr["start"], ln.begin_y), (sr["end"], ln.end_y)]
    (v0, y0), (v1, y1) = pts[0], pts[2]
    slope = (y1 - y0) / (v1 - v0)
    assert all(abs(y - (y0 + (v - v0) * slope)) < 2000 for v, y in pts), pts  # < 0.002 in


if __name__ == "__main__":
    failed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS  {name}")
            except AssertionError as e:
                failed += 1
                print(f"FAIL  {name}: {str(e)[:300]}")
    sys.exit(1 if failed else 0)
