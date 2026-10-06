---
description: Build a McKinsey-style PPTX deck from a brief. Delegates to the mckinsey-slide-agent which picks the right template for each slide, explains its choice, and produces a real .pptx file.
argument-hint: <one-paragraph brief describing the deck you want>
---

You have been asked to build a McKinsey-style deck.

**Brief from the user:**

$ARGUMENTS

Delegate this to the `mckinsey-slide-agent` subagent. Pass the brief verbatim
and let the agent:

1. Decide source mode (an outline/document in the workspace) vs. brief mode
2. Write the slide plan, picking and defending a template per slide
3. Generate the Python build script under `output/` and build the `.pptx`
4. Check the deck against the source files with `scripts/deck_check.py`
5. Render PNG previews if `soffice` / `pdftoppm` are available
6. Report back with the output path, per-slide rationales, coverage and caveats

The agent follows `${CLAUDE_PLUGIN_ROOT}/SKILL.md`. Slide language follows the
source document (or the brief's language when there is no document) unless
the user asks for a translation; Chinese slides use the Chinese theme. If the
brief names a company, it goes into the footer attribution.
