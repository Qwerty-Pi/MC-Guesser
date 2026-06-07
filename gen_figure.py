import fitz  # PyMuPDF
import os
import json

def crop_pdf_to_svg(pdf_path, page_num, bound_box, output_svg_path):
    """
    Extracts a page from a PDF as an SVG and crops it using pure vector manipulation.
    Remove white background.
    
    :param pdf_path: Path to the source PDF file
    :param page_num: 0-indexed page number (e.g., 0 is the first page)
    :param crop_box: A tuple or list containing (x_min, y_min, x_max, y_max) coordinates
    :param output_svg_path: The file path to save the final cropped vector SVG
    """
    doc = fitz.open(pdf_path)
    if page_num < 0 or page_num >= len(doc):
        raise ValueError(f"Page number {page_num} out-of-bound")
        
    page = doc[page_num]
    page_svg = page.get_svg_image()
    
    x_min, y_min, x_max, y_max = bound_box
    width = x_max - x_min
    height = y_max - y_min
    
    lines = page_svg.splitlines()
    
    cropped_svg_lines = [
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}pt" height="{height}pt" viewBox="0 0 {width} {height}">',
        '  <defs>',
        f'    <clipPath id="crop-clip">',
        f'      <rect x="{x_min}" y="{y_min}" width="{width}" height="{height}" />',
        '    </clipPath>',
        '  </defs>',
        # The translate transform shifts the coordinate plane up and left, bringing your crop window to (0,0)
        f'  <g clip-path="url(#crop-clip)" transform="translate({-x_min}, {-y_min})">'
    ]
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("<?xml") or stripped.startswith("<!DOCTYPE") or stripped.startswith("<svg") or stripped.startswith("</svg>"):
            continue
        is_white_fill = 'fill="#ffffff"' in stripped or 'fill="rgb(255,255,255)"' in stripped or 'fill="white"' in stripped
        if is_white_fill:
            continue
        cropped_svg_lines.append(line)
        
    # 4. Close the clipping groups and the root SVG tag safely
    cropped_svg_lines.append('  </g>')
    cropped_svg_lines.append('</svg>')

    with open(output_svg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(cropped_svg_lines))

def scale_svg(input_path, output_path, scale):
    cmd = f"rsvg-convert -x {scale} -y {scale} -f svg {input_path} -o {output_path}"
    os.system(cmd)

if __name__ == "__main__":

    with open("crop.json", "r") as f:
        data = f.read()
    data = json.loads(data)

    pdf_name = "PP-DSE-MATH-CP-1.pdf" 
    if not os.path.exists(pdf_name):
        raise ValueError(f"File '{pdf_name}' does not exists")
    
    for figure in data:
        page, rect, label = figure['page'], figure['rect'], figure['label']
        crop_pdf_to_svg(
            pdf_path=pdf_name,
            page_num=page,
            bound_box=rect,
            output_svg_path=f"figures/{label}.svg"
        )
        scale_svg(
            input_path=f"figures/{label}.svg",
            output_path=f"figures/{label}.svg",
            scale=1.5
        )
        print(f"Generated figure {label}")