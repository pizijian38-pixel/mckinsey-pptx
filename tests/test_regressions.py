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


def test_table_decimals_survive_numbering_strip():
    """A docx table cell holding only "24.4" sits on its own line; the regex that
    strips list numbering ("3. Market") ate "24." and left "4", so every decimal
    in a source table was reported as invented (Crest deck, slide 3)."""
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "outline.docx"
        cells = "".join(f"<w:tc><w:p><w:r><w:t>{v}</w:t></w:r></w:p></w:tc>"
                        for v in ["YNBY", "24.4", "24.6", "8.0", "1.", "2)"])
        xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
               '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
               '<w:body><w:p><w:r><w:t>3. Market share</w:t></w:r></w:p>'
               f'<w:tbl><w:tr>{cells}</w:tr></w:tbl></w:body></w:document>')
        with zipfile.ZipFile(src, "w") as z:
            z.writestr("word/document.xml", xml)
        nums = deck_check.numbers(deck_check.source_text(src))
        assert {"24.4", "24.6", "8"} <= nums or {"24.4", "24.6", "8.0"} <= nums, nums
        assert "4" not in nums and "6" not in nums, nums
        assert "3" not in nums, "heading numbering must still be stripped"


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
            # every example must also pass the checker's readable-size rule [7]:
            # a template whose own example fails it fails every deck that uses it
            prs = Presentation("output/all_examples.pptx")
            for i, sl in enumerate(prs.slides, start=1):
                bs = deck_check.body_size(sl, prs.slide_height)
                tpl = deck_check.template_of(sl)
                floor = (deck_check.LABEL_MIN_PT if tpl in deck_check._LABEL_TEMPLATES
                         else deck_check.BODY_MIN_PT)
                if bs is not None and bs < floor and i > 1:
                    failures.append(f"[7] {tpl}: {bs:g}pt < {floor}pt")
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
    # several items named = no single focal claim: no nudge to highlight the first
    assert not _warnings(title="Batteries and Cables both lose share", bus=bus)


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


def test_heatmap_shade_orders_with_value():
    """Darker cell = larger value, on one ramp for the whole grid."""
    vals = [[1, 9, 4], [7, 2, 5]]
    b = PresentationBuilder()
    b.add("heatmap", title="t", rows=["r1", "r2"], columns=["a", "b", "c"], values=vals)
    m = _marks(b.prs.slides[0], "heatmap:")
    lum = {}
    for i, r in enumerate(["r1", "r2"]):
        for j, c in enumerate(["a", "b", "c"]):
            rgb = m[f"{r} / {c}"].fill.fore_color.rgb
            lum[vals[i][j]] = sum(rgb)
    ordered = [lum[v] for v in sorted(lum)]
    assert ordered == sorted(ordered, reverse=True), lum


def test_bump_ranks_sit_on_fixed_rows():
    series = [{"name": "a", "ranks": [1, 2, 3]}, {"name": "b", "ranks": [2, 1, 1]},
              {"name": "c", "ranks": [3, 3, 2]}]
    b = PresentationBuilder()
    b.add("bump", title="t", snapshots=["Q1", "Q2", "Q3"], series=series)
    m = _marks(b.prs.slides[0], "bump:")
    y = {}
    for sr in series:
        for k in range(2):
            ln = m[f"{sr['name']}|{k}"]
            for rank, yy in ((sr["ranks"][k], ln.begin_y), (sr["ranks"][k + 1], ln.end_y)):
                y.setdefault(rank, set()).add(round(yy / 1000))
    assert all(len(v) == 1 for v in y.values()), y           # one row per rank
    rows = [y[r].pop() for r in sorted(y)]
    steps = {rows[i + 1] - rows[i] for i in range(len(rows) - 1)}
    assert len(steps) == 1 and steps.pop() > 0, rows          # equal pitch, rank 1 on top
    try:
        PresentationBuilder().add("bump", title="t", snapshots=["a", "b", "c"],
                                  series=[{"name": "x", "ranks": [1, 1, 1]},
                                          {"name": "y", "ranks": [1, 2, 2]}])
    except ValueError:
        return
    raise AssertionError("duplicate rank accepted")


def test_radar_is_native_and_on_one_scale():
    b = PresentationBuilder()
    b.add("radar", title="t", criteria=["a", "b", "c"], scale_max=5,
          series=[{"name": "x", "values": [1, 5, 3]}, {"name": "y", "values": [4, 2, 2]}])
    gf = [sh for sh in b.prs.slides[0].shapes if sh.has_chart][0]
    assert [list(s.values) for s in gf.chart.plots[0].series] == [[1, 5, 3], [4, 2, 2]]
    assert gf.chart.value_axis.maximum_scale == 5
    try:
        PresentationBuilder().add("radar", title="t", criteria=["a", "b", "c"], scale_max=5,
                                  series=[{"name": "x", "values": [1, 50, 3]}])
    except ValueError:
        return
    raise AssertionError("value off the shared scale accepted")


# ---------- agent ergonomics (found on a Gemini / Antigravity run) ----------

def test_chart_highlight_is_accent_not_red():
    """Highlight is emphasis, so it uses the accent; red only when asked."""
    from mckinsey_pptx.theme import DEFAULT_THEME
    pal = DEFAULT_THEME.palette

    def colours(chart_type, highlight):
        b = PresentationBuilder()
        b.add("chart", title="t", chart_type=chart_type, categories=["a", "b", "c"],
              series=[{"name": "S1", "values": [1, 2, 3]}, {"name": "S2", "values": [3, 2, 1]}]
              if chart_type == "line" else [{"name": "S1", "values": [1, 2, 3]}],
              highlight=highlight, source="")
        gf = [sh for sh in b.prs.slides[0].shapes if sh.has_chart][0]
        ser = gf.chart.plots[0].series
        if chart_type == "line":
            return [str(s.format.line.color.rgb) for s in ser]
        return [str(pt.format.fill.fore_color.rgb) for pt in [ser[0].points[1]]]

    assert colours("line", {"series": "S2"})[1] == str(pal.bright_blue)
    assert colours("line", {"series": "S2", "tone": "red"})[1] == str(pal.status_red)
    assert colours("column", {"point": 1}) == [str(pal.bright_blue)]
    assert colours("column", {"point": 1, "tone": "red"}) == [str(pal.status_red)]


def test_catalog_lookup():
    """scripts/catalog.py prints only the asked-for entries (by name, alias or
    number), an index of every template, and near matches for typos."""
    import catalog
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        assert catalog.main(["sankey", "mekko", "77"]) == 0
    text = out.getvalue()
    assert "## 70. Sankey" in text and "## 68. Marimekko" in text and "## 77. Venn" in text
    assert "## 71." not in text and "## 1. " not in text
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        catalog.main([])
    rows = [l for l in out.getvalue().splitlines() if l[:3].strip().rstrip(".").isdigit()]
    _, templates, _ = catalog.load()
    assert len(rows) == len(templates) >= 80, len(rows)
    err = io.StringIO()
    with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
        assert catalog.main(["sankee"]) == 1
    assert "sankey" in err.getvalue()
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        catalog.main(["--icons"])
    assert "`trend_up`" in out.getvalue() and "{red|" in out.getvalue()


def _check(path, *sources):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = deck_check.main([str(path)] + sum((["--source", str(s)] for s in sources), []))
    return code, out.getvalue()


def test_text_layout_share_is_advisory():
    """[11] reminds when text layouts fill most content slides, but never fails
    the check (text is right for lists) - and stays quiet for a mixed deck."""
    items = [{"title": f"Point {k}", "body": "Short supporting line"} for k in "ABC"]
    with tempfile.TemporaryDirectory() as d:
        b = PresentationBuilder()
        b.add("cover_slide", title="Deck", subtitle="s", date="")
        for i in range(3):
            b.add("card_grid", title=f"Slide {i} makes a point", cards=items, source="")
        b.add("chart", title="One chart", categories=["a", "b"],
              series=[{"name": "s", "values": [1, 2]}], source="")
        path = Path(d) / "t.pptx"
        b.save(str(path))
        code, text = _check(path)
        assert "[11]" in text and "reminder: text layouts on 3 of 4" in text, text[-400:]
        assert code == 0, "the advisory section must not flag the deck"
        b = PresentationBuilder()
        b.add("card_grid", title="One", cards=items, source="")
        b.add("chart", title="Two", categories=["a", "b"],
              series=[{"name": "s", "values": [1, 2]}], source="")
        b.save(str(path))
        assert "ok (1 of 2" in _check(path)[1]


def test_step_numbers_are_not_data():
    """Sequence numbers (01 ... 05, Step 03, L4) are layout: the checker must
    not report them as numbers missing from the source."""
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "src.md"
        src.write_text("Plan, build, test, launch, scale. Five steps.", encoding="utf-8")
        b = PresentationBuilder()
        b.add("process_flow", title="Five steps take the product to scale", focus=[],
              steps=[{"name": n, "items": [n]} for n in ["Plan", "Build", "Test", "Launch", "Scale"]],
              source="")
        b.add("cycle", title="The loop", steps=["Plan", "Build", "Test", "Launch", "Scale"],
              center="Scale", focus=[], source="")
        path = Path(d) / "t.pptx"
        b.save(str(path))
        text = _check(path, src)[1]
        block = text.split("[1]")[1].split("[2]")[0]
        assert block.strip().endswith("none"), block


def test_run_deck_builds_checks_and_renders():
    """One command: build script -> deck found -> checker -> previews."""
    import shutil
    import run_deck
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "output"
        out.mkdir()
        script = out / "build_demo.py"
        script.write_text(
            "import sys\nfrom pathlib import Path\n"
            f"sys.path.insert(0, r'{ROOT}')\n"
            "from mckinsey_pptx import PresentationBuilder\n"
            "b = PresentationBuilder()\n"
            "b.add('chart', title='Revenue doubled in two years', categories=['2023', '2025'],\n"
            "      series=[{'name': 'Revenue', 'values': [10, 20]}], source='')\n"
            "b.save(str(Path(__file__).resolve().parent / 'demo.pptx'))\n", encoding="utf-8")
        render = shutil.which("soffice") or shutil.which("libreoffice")
        log = io.StringIO()
        with contextlib.redirect_stdout(log):
            code = run_deck.main([str(script)] + ([] if render else ["--no-render"]))
        text = log.getvalue()
        assert code == 0, text[-800:]
        assert "demo.pptx" in text and "build : ok" in text and "check : clean" in text
        if render:
            prev = out / "preview_demo"
            assert (prev / "contact_sheet.png").exists() and list(prev.glob("slide-*.png")), text[-600:]
        # a failing build is reported, not hidden
        script.write_text("raise SystemExit(3)\n", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()) as log:
            assert run_deck.main([str(script), "--no-render"]) == 1
        assert "FAILED" in log.getvalue()


_SHARE = {"YNBY": [24.4, 24.6, 25.1, 25.0], "DARLIE": [19.4, 18.6, 18.0, 17.2],
          "Crest": [8.8, 8.9, 8.5, 8.0], "LSL": [7.3, 8.0, 8.6, 9.0]}


def test_players_by_period_table_gets_a_reminder():
    """Players x years copied as a table (Crest deck, slide 3): [11] reminds that a
    line chart shows the trend - advisory only, the check still passes."""
    with tempfile.TemporaryDirectory() as d:
        b = PresentationBuilder()
        b.add("data_table", title="Crest has slipped to 8.0% share",
              columns=["Brand", "2022", "2023", "2024", "2025 Est"],
              rows=[[k] + [f"{v:.1f}" for v in vals] for k, vals in _SHARE.items()], source="")
        b.add("chart", chart_type="line", title="Same data as a chart",
              categories=["2022", "2023", "2024", "2025E"],
              series=[{"name": k, "values": v} for k, v in _SHARE.items()],
              highlight={"series": "Crest"}, number_format="0.0", source="")
        path = Path(d) / "t.pptx"
        b.save(str(path))
        code, text = _check(path)
        block = text.split("[11]")[1]
        assert "slide(s) 1 show numbers by period" in block, block
        assert code == 0


def test_multi_line_chart_names_lines_at_the_end():
    """3+ lines: no legend to decode; each line is named at its last point, the
    focal line with its value."""
    b = PresentationBuilder()
    b.add("chart", chart_type="line", title="Crest slipped as LSL rose",
          categories=["2022", "2023", "2024", "2025E"],
          series=[{"name": k, "values": v, **({"tone": "navy"} if k == "LSL" else {})}
                  for k, v in _SHARE.items()],
          highlight={"series": "Crest"}, number_format="0.0", source="")
    gf = [sh for sh in b.prs.slides[0].shapes if sh.has_chart][0]
    assert not gf.chart.has_legend
    ends = {}
    for ser in gf.chart.plots[0].series:
        dl = ser.points[3].data_label
        ends[ser.name] = dl.text_frame.text if dl.has_text_frame else ""
    assert ends["Crest"] == "Crest 8.0" and ends["LSL"] == "LSL 9.0", ends
    assert ends["YNBY"] == "YNBY", ends



def test_line_end_names_do_not_collide():
    """Lines that finish close together (Saky 5.5 / Colgate 4.9 on a 0-25 axis)
    get their end names moved below the point instead of printing on top of each
    other - without landing on the next line's name (Crest 8.0 vs Saky 5.5)."""
    from pptx.enum.chart import XL_LABEL_POSITION as P
    data = dict(_SHARE, Saky=[5.1, 5.2, 5.2, 5.5], Colgate=[5.2, 5.0, 4.9, 4.9])
    b = PresentationBuilder()
    b.add("chart", chart_type="line", title="Crest slipped as LSL rose",
          categories=["2022", "2023", "2024", "2025E"],
          series=[{"name": k, "values": v} for k, v in data.items()],
          highlight={"series": "Crest"}, number_format="0.0", source="")
    gf = [sh for sh in b.prs.slides[0].shapes if sh.has_chart][0]
    pos = {ser.name: ser.points[3].data_label.position for ser in gf.chart.plots[0].series}
    assert pos["YNBY"] == P.RIGHT and pos["DARLIE"] == P.RIGHT, pos
    assert pos["LSL"] == P.RIGHT and pos["Crest"] == P.BELOW, pos      # 9.0 / 8.0
    assert pos["Saky"] == P.RIGHT and pos["Colgate"] == P.BELOW, pos    # 5.5 / 4.9


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
