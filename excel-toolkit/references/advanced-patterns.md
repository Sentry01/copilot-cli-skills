# Advanced Excel Patterns Reference

## Table of Contents
1. [Dashboard Layout & Spacing](#dashboard-layout--spacing)
2. [Charts and Visualization](#charts-and-visualization)
3. [Conditional Formatting](#conditional-formatting)
4. [Pivot-Style Summaries](#pivot-style-summaries)
5. [Multi-Sheet Workbooks](#multi-sheet-workbooks)
6. [Data Validation](#data-validation)
7. [CSV/TSV Import](#csvtsv-import)
8. [Large File Handling](#large-file-handling)

## Dashboard Layout & Spacing

### CRITICAL: Layout Rules for Insights/Dashboard Sheets

When building dashboard or insights sheets with tables and charts, follow these rules
to prevent overlapping visuals and ensure a clean, professional layout.

### Row Counter Pattern (MANDATORY)
Always use a running `ROW` counter — never hardcode row positions:
```python
ROW = 1  # running row counter — increment as you go

# Title
ws.merge_cells(f'A{ROW}:I{ROW}')
ws.cell(row=ROW, column=1, value='Dashboard Title').font = title_font
ROW += 2  # blank row after title

# Section header
ws.cell(row=ROW, column=1, value='Section Name').font = section_font
ROW += 1

# Table header row
for i, h in enumerate(headers, 1):
    ws.cell(row=ROW, column=i, value=h)
style_header(ws, ROW, len(headers))
table_header_row = ROW  # save for chart references
ROW += 1

# Data rows
for item in data:
    # write data at ROW
    ROW += 1

# Spacing BEFORE chart
ROW += 2  # 2 blank rows between table and chart

# Place chart at current ROW
ws.add_chart(chart, f'A{ROW}')

# Spacing AFTER chart — reserve rows for chart height
ROW += 18  # charts need 15-18 rows of vertical space

# Next section starts here — guaranteed no overlap
```

### Spacing Constants
| Element | Rows to Reserve |
|---------|----------------|
| Title + blank line | 2 |
| Gap between table and chart | 2 blank rows |
| Standard chart (width ≤24, height ≤14) | 17 rows after anchor |
| Tall chart (height 15-16) | 18-20 rows after anchor |
| Wide chart (width 28-30) | 18 rows after anchor |
| Gap between sections (no chart) | 2-3 blank rows |
| Side-by-side charts | Place at same ROW, different columns (e.g., A{ROW} and F{ROW}) — both consume same vertical space |

### Chart Sizing Guide
| Chart Type | Recommended width × height |
|------------|---------------------------|
| Bar/Column (≤5 categories) | 20 × 13 |
| Bar/Column (6-10 categories) | 24 × 14 |
| Bar/Column (15-20 categories) | 28-30 × 15 |
| Horizontal bar (leaderboard) | 24 × 16 |
| Pie chart | 15 × 13-14 |
| Side-by-side pair | 20×13 + 15×13 |

### Styling Standards
```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Fonts
title_font = Font(bold=True, size=18, color='1F4E79')
section_font = Font(bold=True, size=14, color='2E75B6')
header_font = Font(bold=True, size=11, color='FFFFFF')

# Fills
header_fill = PatternFill('solid', fgColor='2E75B6')
alt_row_fill = PatternFill('solid', fgColor='D6E4F0')  # zebra striping

# Border
thin_border = Border(
    left=Side('thin', color='B4C6E7'), right=Side('thin', color='B4C6E7'),
    top=Side('thin', color='B4C6E7'), bottom=Side('thin', color='B4C6E7')
)

# Number formats
NUM_FMT = '#,##0'
PCT_FMT = '0.0%'
CURRENCY_FMT = '$#,##0'

# Chart colors (consistent palette)
BLUE = '2E75B6'    # primary / GHE / first series
ORANGE = 'ED7D31'  # secondary / CfB / second series
RED = 'C00000'     # negative / whitespace / warning
GREEN = '70AD47'   # positive / growth
```

### Column Width Defaults for Dashboards
```python
widths = {
    'A': 10,   # rank / short labels
    'B': 45,   # account names / long text
    'C': 24,   # owner names / categories
    'D': 22,   # manager names
    'E': 18,   # segment / medium text
    'F': 16,   # numbers
    'G': 16,   # numbers
    'H': 18,   # numbers / labels
    'I': 16,   # numbers
}
for col, w in widths.items():
    ws.column_dimensions[col].width = w
```

### Helper Functions (Reuse Across Dashboards)
```python
def style_header_row(ws, row, num_cols):
    """Apply header styling to a row."""
    for c in range(1, num_cols + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center', wrap_text=True)
        cell.border = thin_border

def style_data_cell(ws, row, col, fmt=None):
    """Apply data cell styling with zebra striping."""
    cell = ws.cell(row=row, column=col)
    cell.border = thin_border
    cell.alignment = Alignment(horizontal='center')
    if fmt:
        cell.number_format = fmt
    if row % 2 == 0:
        cell.fill = alt_row_fill
```

### Anti-Patterns to Avoid
- ❌ Hardcoding chart positions (e.g., `ws.add_chart(chart, 'A55')`)
- ❌ Placing charts immediately after tables with no gap
- ❌ Assuming chart height — always reserve 17-20 rows
- ❌ Using different color schemes per chart — stay consistent
- ❌ Forgetting to merge cells for section titles
- ❌ Skipping zebra striping on data rows

## Charts and Visualization

### openpyxl Charts
```python
from openpyxl.chart import BarChart, LineChart, PieChart, Reference

chart = BarChart()
chart.title = "Sales by Region"
chart.y_axis.title = "Revenue ($)"
chart.style = 10  # clean modern style
chart.width = 24
chart.height = 14
data = Reference(ws, min_col=2, min_row=1, max_col=4, max_row=10)
cats = Reference(ws, min_col=1, min_row=2, max_row=10)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
# Apply consistent colors
chart.series[0].graphicalProperties.solidFill = '2E75B6'
chart.series[1].graphicalProperties.solidFill = 'ED7D31'
ws.add_chart(chart, "F2")
```

### Pie Chart with Labels
```python
from openpyxl.chart.label import DataLabelList

pie = PieChart()
pie.title = "Distribution"
pie.style = 10
pie.width = 15
pie.height = 14
pie.add_data(data_ref, titles_from_data=True)
pie.set_categories(cat_ref)
pie.dataLabels = DataLabelList()
pie.dataLabels.showPercent = True
pie.dataLabels.showCatName = True
```

### matplotlib → Excel Image
```python
import matplotlib.pyplot as plt
from openpyxl.drawing.image import Image

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(categories, values)
ax.set_title("Chart Title")
fig.savefig("/tmp/chart.png", dpi=150, bbox_inches="tight")
plt.close()

img = Image("/tmp/chart.png")
ws.add_image(img, "F2")
```

## Conditional Formatting

```python
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, DataBarRule
from openpyxl.styles import PatternFill, Font

# Highlight cells > 1000
red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
ws.conditional_formatting.add("B2:B100", CellIsRule(operator="greaterThan", formula=["1000"], fill=red_fill))

# Color scale (green-yellow-red)
ws.conditional_formatting.add("C2:C100", ColorScaleRule(
    start_type="min", start_color="63BE7B",
    mid_type="percentile", mid_value=50, mid_color="FFEB84",
    end_type="max", end_color="F8696B"
))

# Data bars
ws.conditional_formatting.add("D2:D100", DataBarRule(
    start_type="min", end_type="max", color="638EC6"
))
```

## Pivot-Style Summaries

```python
import pandas as pd

df = pd.read_excel("data.xlsx")
pivot = pd.pivot_table(df, values="Revenue", index="Region", columns="Quarter", aggfunc="sum", margins=True)
pivot.to_excel("pivot_output.xlsx", sheet_name="Pivot")
```

## Multi-Sheet Workbooks

```python
with pd.ExcelWriter("multi.xlsx", engine="openpyxl") as writer:
    df_summary.to_excel(writer, sheet_name="Summary", index=False)
    df_detail.to_excel(writer, sheet_name="Detail", index=False)
    df_raw.to_excel(writer, sheet_name="Raw Data", index=False)
```

## Data Validation

```python
from openpyxl.worksheet.datavalidation import DataValidation

# Dropdown list
dv = DataValidation(type="list", formula1='"Yes,No,Maybe"', allow_blank=True)
dv.prompt = "Select an option"
ws.add_data_validation(dv)
dv.add("C2:C100")

# Number range
dv_num = DataValidation(type="whole", operator="between", formula1=0, formula2=100)
ws.add_data_validation(dv_num)
dv_num.add("D2:D100")
```

## CSV/TSV Import

```python
import pandas as pd

# CSV
df = pd.read_csv("data.csv")
df.to_excel("output.xlsx", index=False)

# TSV
df = pd.read_csv("data.tsv", sep="\t")
df.to_excel("output.xlsx", index=False)

# Multiple CSV → sheets
with pd.ExcelWriter("combined.xlsx") as writer:
    for f in csv_files:
        df = pd.read_csv(f)
        df.to_excel(writer, sheet_name=Path(f).stem[:31], index=False)
```

## Large File Handling

### Reading (read_only mode)
```python
wb = openpyxl.load_workbook("large.xlsx", read_only=True, data_only=True)
ws = wb.active
for row in ws.iter_rows(min_row=2, values_only=True):
    process(row)
wb.close()
```

### Writing (write_only mode)
```python
wb = openpyxl.Workbook(write_only=True)
ws = wb.create_sheet()
for chunk in data_chunks:
    for row in chunk:
        ws.append(row)
wb.save("large_output.xlsx")
```

### Chunked pandas
```python
chunks = pd.read_excel("large.xlsx", chunksize=10000)
for chunk in chunks:
    process(chunk)
```
