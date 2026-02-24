---
name: powerpoint-toolkit
description: "Build, edit, analyze, and improve PowerPoint presentations (.pptx). Use when a user asks to: (1) Create a new presentation from scratch, (2) Edit or modify slides, text, images, or layouts, (3) Analyze a presentation for quality, consistency, or content, (4) Improve an existing presentation's design, structure, or readability, (5) Extract text or speaker notes, (6) Add charts, tables, or media to slides, (7) Review or critique a presentation."
---

# PowerPoint Toolkit

## Setup (First Use)

```bash
python3 scripts/setup_deps.py
```
Installs: python-pptx, Pillow, pyyaml. Skip if already installed.

## Workflow Decision Tree

1. **Inspect structure** → Run `scripts/inspect_pptx.py`
2. **Extract text** → Run `scripts/extract_text.py`
3. **Analyze & get improvement suggestions** → Run `scripts/analyze_pptx.py`
4. **Generate visual thumbnails** → Run `scripts/thumbnails.py`
5. **Create new presentation** → Use python-pptx (see `references/design-and-creation.md`)
6. **Edit existing presentation** → Use python-pptx or OOXML (see `references/ooxml-editing.md`)

## Quick-Start Scripts

### Inspect File Structure
```bash
python3 scripts/inspect_pptx.py deck.pptx                    # Overview
python3 scripts/inspect_pptx.py deck.pptx --text              # With all text
python3 scripts/inspect_pptx.py deck.pptx --notes             # With speaker notes
python3 scripts/inspect_pptx.py deck.pptx --layouts           # With layout details
python3 scripts/inspect_pptx.py deck.pptx --slide 0           # Single slide
python3 scripts/inspect_pptx.py deck.pptx --text --notes      # Full content
```
Returns JSON: slide count, dimensions, shapes, text, images, charts, tables, notes.

### Extract Text
```bash
python3 scripts/extract_text.py deck.pptx                     # Markdown format
python3 scripts/extract_text.py deck.pptx --format json        # Structured JSON
python3 scripts/extract_text.py deck.pptx --format text        # Plain text
python3 scripts/extract_text.py deck.pptx --notes              # Include speaker notes
```

### Analyze & Improve
```bash
python3 scripts/analyze_pptx.py deck.pptx                     # Full analysis
python3 scripts/analyze_pptx.py deck.pptx --verbose            # Extra detail
```
Returns JSON with stats (fonts, sizes, layouts, text density) and issues (readability, consistency, missing notes, visual balance).

### Generate Thumbnails
```bash
python3 scripts/thumbnails.py deck.pptx                        # Default 4-col grid
python3 scripts/thumbnails.py deck.pptx preview --cols 3       # Custom layout
```
Requires LibreOffice + poppler (pdftoppm). Creates a JPEG grid for visual review.

## Creating Presentations

### Design Principles
Before writing code, always:
1. **Analyze content** — What topic, tone, audience?
2. **Choose palette** — See `references/design-and-creation.md` for 10 curated palettes
3. **Plan layout** — Decide slide types: title, content, section, closing
4. **State approach** — Explain design choices before implementation

### Key Rules
- Use **web-safe fonts only**: Arial, Verdana, Georgia, Tahoma, Trebuchet MS, Times New Roman, Courier New
- Create **clear visual hierarchy** through size, weight, and color
- Keep **text concise** — aim for ≤6 bullet points, ≤6 words per bullet
- Ensure **strong contrast** between text and backgrounds
- Use **consistent spacing** and alignment across all slides
- Add **speaker notes** for presentation delivery

### Quick Creation Template
```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Title slide
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Title"
slide.placeholders[1].text = "Subtitle"

# Content slide
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Section"
body = slide.placeholders[1].text_frame
body.text = "First point"
p = body.add_paragraph()
p.text = "Second point"
p.level = 0

prs.save("output.pptx")
```

For full creation reference (shapes, formatting, charts, tables, images, notes) → see `references/design-and-creation.md`.

## Editing Presentations

### Simple Edits (python-pptx)
```python
from pptx import Presentation

prs = Presentation("existing.pptx")
slide = prs.slides[0]

for shape in slide.shapes:
    if shape.has_text_frame:
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                run.text = run.text.replace("old", "new")

prs.save("modified.pptx")
```

### Advanced Edits (OOXML)
For operations beyond python-pptx (animations, complex formatting, raw XML manipulation) → see `references/ooxml-editing.md`.

## Providing Improvement Feedback

When asked to review or improve a presentation:

1. Run `scripts/inspect_pptx.py deck.pptx --text --notes`
2. Run `scripts/analyze_pptx.py deck.pptx`
3. Optionally generate thumbnails for visual review
4. Present findings in this order:
   - **Overview**: slide count, layout types, visual balance
   - **Content Issues**: text density, empty slides, missing titles
   - **Design Issues**: font consistency, size readability, color contrast
   - **Structure Issues**: flow, pacing, section organization
   - **Suggestions**: specific actionable improvements with slide references

## Common Slide Patterns

| Pattern | Layout | When to Use |
|---------|--------|-------------|
| Title Slide | Layout 0 | Opening, section dividers |
| Bullets | Layout 1 | Key points, agenda |
| Two-Column | Layout 3 | Comparison, before/after |
| Image + Text | Layout 5 + textbox | Visual storytelling |
| Chart Slide | Layout 5 + chart | Data presentation |
| Table Slide | Layout 5 + table | Structured data |
| Quote Slide | Layout 6 + textbox | Attribution, emphasis |
| Closing | Layout 0 or 6 | Thank you, contact info |
