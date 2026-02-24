#!/usr/bin/env python3
"""
Generate slide thumbnails as a grid image for visual review.
Usage: python thumbnails.py <file.pptx> [output_prefix] [--cols N] [--dpi N]
Requires: LibreOffice (for PDF conversion), Pillow
"""
import sys, argparse, subprocess, tempfile, os, math
from pathlib import Path


def generate_thumbnails(filepath, output_prefix="thumbnails", cols=4, dpi=150):
    from PIL import Image
    
    filepath = Path(filepath).absolute()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Convert PPTX to PDF via LibreOffice
        result = subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmpdir, str(filepath)],
            capture_output=True, text=True, timeout=60
        )
        
        pdf_path = Path(tmpdir) / filepath.with_suffix(".pdf").name
        if not pdf_path.exists():
            # Try alternate naming
            pdfs = list(Path(tmpdir).glob("*.pdf"))
            if not pdfs:
                return {"error": f"PDF conversion failed: {result.stderr}"}
            pdf_path = pdfs[0]
        
        # Convert PDF pages to images
        img_prefix = str(Path(tmpdir) / "slide")
        result = subprocess.run(
            ["pdftoppm", "-jpeg", "-r", str(dpi), str(pdf_path), img_prefix],
            capture_output=True, text=True, timeout=60
        )
        
        slide_images = sorted(Path(tmpdir).glob("slide-*.jpg"))
        if not slide_images:
            # Try png
            result = subprocess.run(
                ["pdftoppm", "-png", "-r", str(dpi), str(pdf_path), img_prefix],
                capture_output=True, text=True, timeout=60
            )
            slide_images = sorted(Path(tmpdir).glob("slide-*.png"))
        
        if not slide_images:
            return {"error": "Failed to convert PDF pages to images. Ensure pdftoppm (poppler) is installed."}
        
        # Build thumbnail grid
        images = [Image.open(str(p)) for p in slide_images]
        thumb_w = 400
        thumb_h = int(thumb_w * images[0].height / images[0].width)
        
        rows = math.ceil(len(images) / cols)
        padding = 10
        label_h = 20
        
        grid_w = cols * (thumb_w + padding) + padding
        grid_h = rows * (thumb_h + padding + label_h) + padding
        
        grid = Image.new("RGB", (grid_w, grid_h), "white")
        
        from PIL import ImageDraw
        draw = ImageDraw.Draw(grid)
        
        for i, img in enumerate(images):
            r = i // cols
            c = i % cols
            x = padding + c * (thumb_w + padding)
            y = padding + r * (thumb_h + padding + label_h)
            
            thumb = img.resize((thumb_w, thumb_h), Image.LANCZOS)
            grid.paste(thumb, (x, y + label_h))
            draw.text((x + 4, y + 2), f"Slide {i}", fill="black")
        
        output_path = f"{output_prefix}.jpg"
        grid.save(output_path, "JPEG", quality=90)
        
        for img in images:
            img.close()
        
        return {"output": output_path, "slides": len(images), "grid": f"{rows}x{cols}"}


def main():
    parser = argparse.ArgumentParser(description="Generate slide thumbnails")
    parser.add_argument("file", help="PowerPoint file path")
    parser.add_argument("output", nargs="?", default="thumbnails", help="Output prefix (default: thumbnails)")
    parser.add_argument("--cols", type=int, default=4, help="Columns in grid (default: 4)")
    parser.add_argument("--dpi", type=int, default=150, help="Resolution (default: 150)")
    args = parser.parse_args()
    
    if not Path(args.file).exists():
        print(f"Error: File not found: {args.file}")
        sys.exit(1)
    
    import json
    result = generate_thumbnails(args.file, args.output, args.cols, args.dpi)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
