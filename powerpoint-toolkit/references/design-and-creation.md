# PowerPoint Design & Creation Reference

## Table of Contents
1. [Creating Slides with python-pptx](#creating-slides-with-python-pptx)
2. [Editing Existing Presentations](#editing-existing-presentations)
3. [Design Palettes](#design-palettes)
4. [Charts](#charts)
5. [Tables](#tables)
6. [Images & Media](#images--media)
7. [Layouts & Templates](#layouts--templates)
8. [Speaker Notes](#speaker-notes)
9. [Transitions & Animations](#transitions--animations)

## Creating Slides with python-pptx

### New Presentation
```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

prs = Presentation()
prs.slide_width = Inches(13.333)  # 16:9 widescreen
prs.slide_height = Inches(7.5)

# Title slide
layout = prs.slide_layouts[0]  # Title Slide
slide = prs.slides.add_slide(layout)
slide.shapes.title.text = "Presentation Title"
slide.placeholders[1].text = "Subtitle text"

prs.save("output.pptx")
```

### Text Formatting
```python
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

tf = shape.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Bold header"
p.font.bold = True
p.font.size = Pt(28)
p.font.color.rgb = RGBColor(0x1C, 0x28, 0x33)
p.alignment = PP_ALIGN.CENTER

# Add more paragraphs
p2 = tf.add_paragraph()
p2.text = "Body text"
p2.font.size = Pt(16)
p2.space_before = Pt(12)

# Bullet lists
p3 = tf.add_paragraph()
p3.text = "Bullet item"
p3.level = 0
p3.space_before = Pt(6)
```

### Adding Text Boxes
```python
from pptx.util import Inches, Pt

txBox = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(1.5))
tf = txBox.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Custom positioned text"
p.font.size = Pt(18)
```

### Adding Shapes
```python
from pptx.enum.shapes import MSO_SHAPE

# Rectangle
shape = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, Inches(1), Inches(1), Inches(3), Inches(2)
)
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0x44, 0x72, 0xC4)
shape.line.fill.background()  # No border

# Rounded rectangle
shape = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5), Inches(1), Inches(3), Inches(2)
)

# Circle
shape = slide.shapes.add_shape(
    MSO_SHAPE.OVAL, Inches(1), Inches(4), Inches(2), Inches(2)
)
```

## Editing Existing Presentations

### Modify Text
```python
prs = Presentation("existing.pptx")
slide = prs.slides[0]

for shape in slide.shapes:
    if shape.has_text_frame:
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                if "old text" in run.text:
                    run.text = run.text.replace("old text", "new text")

prs.save("modified.pptx")
```

### Delete Slides
```python
# Delete slide at index
def delete_slide(prs, index):
    rId = prs.slides._sldIdLst[index].rId
    prs.part.drop_rel(rId)
    del prs.slides._sldIdLst[index]

delete_slide(prs, 2)  # Remove 3rd slide
```

### Duplicate Slides
```python
import copy
from lxml import etree

def duplicate_slide(prs, slide_index):
    template = prs.slides[slide_index]
    layout = template.slide_layout
    new_slide = prs.slides.add_slide(layout)
    
    for shape in template.shapes:
        el = copy.deepcopy(shape._element)
        new_slide.shapes._spTree.append(el)
    
    return new_slide
```

### Reorder Slides
```python
def move_slide(prs, old_index, new_index):
    slides = list(prs.slides._sldIdLst)
    slides.insert(new_index, slides.pop(old_index))
    prs.slides._sldIdLst.clear()
    for s in slides:
        prs.slides._sldIdLst.append(s)
```

## Design Palettes

Choose based on content topic. Each has: primary, secondary, accent, background, text.

| Name | Primary | Secondary | Accent | Background | Text |
|------|---------|-----------|--------|------------|------|
| Corporate Blue | #1C2833 | #2E4053 | #3498DB | #F4F6F6 | #1C2833 |
| Teal & Coral | #277884 | #5EA8A7 | #FE4447 | #FFFFFF | #1C2833 |
| Forest Green | #1E5128 | #4E9F3D | #D8E9A8 | #FFFFFF | #191A19 |
| Burgundy | #5D1D2E | #951233 | #997929 | #FAF7F2 | #2C2C2C |
| Purple & Emerald | #3D2F68 | #B165FB | #40695B | #181B24 | #FFFFFF |
| Warm Sunset | #E07A5F | #F2CC8F | #81B29A | #F4F1DE | #2C2C2C |
| Charcoal & Red | #292929 | #555555 | #E33737 | #F2F2F2 | #292929 |
| Sage & Terracotta | #87A96B | #E07A5F | #F4F1DE | #FFFFFF | #2C2C2C |
| Black & Gold | #000000 | #333333 | #BF9A4A | #F4F6F6 | #000000 |
| Ocean | #16A085 | #1ABC9C | #2C3E50 | #ECF0F1 | #2C3E50 |

## Charts

```python
from pptx.chart.data import CategoryChartData, ChartData
from pptx.enum.chart import XL_CHART_TYPE

chart_data = CategoryChartData()
chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
chart_data.add_series('Revenue', (1200, 1500, 1800, 2100))

chart_frame = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(1), Inches(2), Inches(8), Inches(4),
    chart_data
)

chart = chart_frame.chart
chart.has_legend = False
chart.chart_title.has_text_frame = True
chart.chart_title.text_frame.text = "Quarterly Revenue"

# Style the series
series = chart.series[0]
series.format.fill.solid()
series.format.fill.fore_color.rgb = RGBColor(0x44, 0x72, 0xC4)

# Pie chart
pie_data = CategoryChartData()
pie_data.categories = ['Product A', 'Product B', 'Other']
pie_data.add_series('Share', (35, 45, 20))

slide.shapes.add_chart(
    XL_CHART_TYPE.PIE, Inches(2), Inches(2), Inches(6), Inches(4), pie_data
)

# Line chart
line_data = CategoryChartData()
line_data.categories = ['Jan', 'Feb', 'Mar', 'Apr']
line_data.add_series('2024', (32, 35, 42, 55))
line_data.add_series('2023', (28, 30, 38, 48))

slide.shapes.add_chart(
    XL_CHART_TYPE.LINE, Inches(1), Inches(2), Inches(8), Inches(4), line_data
)
```

## Tables

```python
rows, cols = 4, 3
table_shape = slide.shapes.add_table(rows, cols, Inches(1), Inches(2), Inches(8), Inches(3))
table = table_shape.table

# Set column widths
table.columns[0].width = Inches(3)
table.columns[1].width = Inches(2.5)
table.columns[2].width = Inches(2.5)

# Header row
for i, header in enumerate(["Product", "Revenue", "Growth"]):
    cell = table.cell(0, i)
    cell.text = header
    for para in cell.text_frame.paragraphs:
        para.font.bold = True
        para.font.size = Pt(14)
        para.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor(0x44, 0x72, 0xC4)

# Data rows
data = [["Product A", "$50M", "+15%"], ["Product B", "$35M", "+22%"], ["Product C", "$28M", "+8%"]]
for r, row_data in enumerate(data, 1):
    for c, val in enumerate(row_data):
        table.cell(r, c).text = val
```

## Images & Media

```python
# Add image with auto-sizing
slide.shapes.add_picture("photo.jpg", Inches(1), Inches(2), width=Inches(4))

# Add image with exact dimensions
slide.shapes.add_picture("logo.png", Inches(8), Inches(0.3), Inches(1.5), Inches(0.8))

# Add image from URL (download first)
import urllib.request
urllib.request.urlretrieve(url, "/tmp/image.jpg")
slide.shapes.add_picture("/tmp/image.jpg", Inches(1), Inches(1), Inches(6))
```

## Layouts & Templates

### Standard Layout Indices (blank presentation)
| Index | Name | Use For |
|-------|------|---------|
| 0 | Title Slide | Opening/title slides |
| 1 | Title and Content | Standard content slides |
| 2 | Section Header | Section dividers |
| 3 | Two Content | Two-column layouts |
| 4 | Comparison | Side-by-side comparison |
| 5 | Title Only | Slides with custom content |
| 6 | Blank | Full creative control |

### Using Specific Layouts
```python
# List available layouts
for i, layout in enumerate(prs.slide_layouts):
    print(f"{i}: {layout.name}")

# Use a specific layout
slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title Only
```

## Speaker Notes

```python
# Add notes
notes_slide = slide.notes_slide
notes_tf = notes_slide.notes_text_frame
notes_tf.text = "Key talking points for this slide..."

# Add more note paragraphs
p = notes_tf.add_paragraph()
p.text = "Remember to mention the Q4 results"
```

## Transitions & Animations

python-pptx has limited animation support. For advanced animations, use OOXML XML editing:

```python
from lxml import etree

# Add a fade transition
nsmap = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
transition = etree.SubElement(slide._element, '{http://schemas.openxmlformats.org/presentationml/2006/main}transition')
transition.set('spd', 'med')
fade = etree.SubElement(transition, '{http://schemas.openxmlformats.org/presentationml/2006/main}fade')
```
