# OOXML Editing Reference

For advanced PowerPoint editing that goes beyond python-pptx capabilities, work directly with the OOXML (Office Open XML) format.

## Table of Contents
1. [Unpack/Repack Workflow](#unpackrepack-workflow)
2. [Key File Paths](#key-file-paths)
3. [Common XML Patterns](#common-xml-patterns)
4. [Namespace Reference](#namespace-reference)

## Unpack/Repack Workflow

A .pptx file is a ZIP archive containing XML files.

```bash
# Unpack
mkdir unpacked && cd unpacked
unzip ../presentation.pptx

# Edit XML files as needed...

# Repack
zip -r ../modified.pptx . -x ".*"
```

Or use python:
```python
import zipfile, shutil
from pathlib import Path

# Unpack
def unpack(pptx_path, output_dir):
    with zipfile.ZipFile(pptx_path, 'r') as z:
        z.extractall(output_dir)

# Repack
def repack(input_dir, pptx_path):
    with zipfile.ZipFile(pptx_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in Path(input_dir).rglob('*'):
            if f.is_file():
                z.write(f, f.relative_to(input_dir))
```

## Key File Paths

| Path | Content |
|------|---------|
| `ppt/presentation.xml` | Main metadata, slide order |
| `ppt/slides/slide{N}.xml` | Individual slide content |
| `ppt/slides/_rels/slide{N}.xml.rels` | Slide relationships (images, layouts) |
| `ppt/slideMasters/slideMaster1.xml` | Master slide template |
| `ppt/slideLayouts/slideLayout{N}.xml` | Layout templates |
| `ppt/theme/theme1.xml` | Colors, fonts, theme info |
| `ppt/notesSlides/notesSlide{N}.xml` | Speaker notes |
| `ppt/media/` | Images and media files |
| `[Content_Types].xml` | MIME type declarations |

## Common XML Patterns

### Text Run
```xml
<a:r>
  <a:rPr lang="en-US" sz="1800" b="1" dirty="0"/>
  <a:t>Bold text at 18pt</a:t>
</a:r>
```
- `sz` = font size in hundredths of a point (1800 = 18pt)
- `b="1"` = bold, `i="1"` = italic, `u="sng"` = underline

### Color
```xml
<!-- Solid color fill -->
<a:solidFill>
  <a:srgbClr val="4472C4"/>
</a:solidFill>

<!-- Theme color -->
<a:solidFill>
  <a:schemeClr val="dk1"/>
</a:solidFill>
```

### Shape Position & Size
```xml
<a:xfrm>
  <a:off x="838200" y="365125"/>    <!-- Position in EMUs (1 inch = 914400 EMU) -->
  <a:ext cx="7772400" cy="1470025"/> <!-- Size in EMUs -->
</a:xfrm>
```

### Adding an Image
1. Copy image to `ppt/media/imageN.ext`
2. Add relationship in `ppt/slides/_rels/slideN.xml.rels`:
```xml
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image1.png"/>
```
3. Reference in slide XML:
```xml
<p:pic>
  <p:nvPicPr>
    <p:cNvPr id="4" name="Picture 3"/>
    <p:cNvPicPr/>
    <p:nvPr/>
  </p:nvPicPr>
  <p:blipFill>
    <a:blip r:embed="rId2"/>
    <a:stretch><a:fillRect/></a:stretch>
  </p:blipFill>
  <p:spPr>
    <a:xfrm>
      <a:off x="914400" y="914400"/>
      <a:ext cx="5486400" cy="3657600"/>
    </a:xfrm>
    <a:prstGeom prst="rect"/>
  </p:spPr>
</p:pic>
```

## Namespace Reference

```
xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
```

Common prefix usage:
- `a:` = DrawingML (text, shapes, colors, fonts)
- `p:` = PresentationML (slides, transitions, notes)
- `r:` = Relationships (links between parts)
