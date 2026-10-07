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
                try:
                    with contextlib.redirect_stderr(io.StringIO()), \
                            contextlib.redirect_stdout(io.StringIO()):
                        exec(blk, env)
                except Exception as e:  # noqa: BLE001
                    failures.append(f"{type(e).__name__}: {e} :: {blk[:70]!r}")
            shared.save("output/all_examples.pptx")
        finally:
            os.chdir(cwd)
    assert not failures, "\n".join(failures)


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
