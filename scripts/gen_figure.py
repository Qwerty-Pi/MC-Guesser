#!/bin/python3
import fitz  # PyMuPDF
import os, sys
import json
from utility import fetch_svg_dimensions

def crop_pdf_to_svg(doc, page_num, bbox):
    if page_num < 0 or page_num >= len(doc):
        raise ValueError(f"Page number {page_num} out-of-bound")
        
    page = doc[page_num]
    page_svg = page.get_svg_image()
    
    x1, y1, x2, y2 = bbox
    page_width, page_height = fetch_svg_dimensions(page_svg)

    width = (x2 - x1) * page_width
    height = (y2 - y1) * page_height
    x_min = x1 * page_width
    y_min = y1 * page_height
    
    lines = page_svg.splitlines()
    
    cropped_svg_lines = [
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}pt" height="{height}pt" viewBox="0 0 {width} {height}">',
        '  <defs>',
        f'    <clipPath id="crop-clip">',
        f'      <rect x="{x_min}" y="{y_min}" width="{width}" height="{height}" />',
        '    </clipPath>',
        '  </defs>',
        f'  <g clip-path="url(#crop-clip)" transform="translate({-x_min}, {-y_min})">'
    ]
    
    # Not necessary to remove background given the papers are scanned anyways
    # for line in lines:
    #     stripped = line.strip()
    #     if stripped.startswith("<?xml") or stripped.startswith("<!DOCTYPE") or stripped.startswith("<svg") or stripped.startswith("</svg>"):
    #         continue
    #     stripped = stripped.replace('fill="#ffffff"', 'fill=transparent')
    #     stripped = stripped.replace('fill="rgb(255,255,255)"', 'fill=transparent')
    #     stripped = stripped.replace('fill="white"', 'fill=transparent')
    #     cropped_svg_lines.append(line)
        
    cropped_svg_lines.append('  </g>')
    cropped_svg_lines.append('</svg>')

    return "\n".join(cropped_svg_lines)

def scale_svg(input_path, output_path, scale):
    cmd = f"rsvg-convert -x {scale} -y {scale} -f svg {input_path} -o {output_path}"
    os.system(cmd)

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Example Usage: ./gen_figure paper.pdf figures.json figures")
        exit()
    else:
        pdf_path, config_path, output_path = sys.argv[1], sys.argv[2], sys.argv[3]

    with open(config_path, "r") as f:
        data = f.read()
    data = json.loads(data)

    if not os.path.exists(pdf_path):
        raise ValueError(f"File '{pdf_path}' does not exists")
    
    os.makedirs(output_path, exist_ok = True)
    for figure in data:
        page, rect, label = figure['page'], figure['rect'], figure['label']
        crop_pdf_to_svg(
            pdf_path=pdf_path,
            page_num=page,
            bound_box=rect,
            output_svg_path=f"{output_path}/{label}.svg"
        )
        print(f"Generated figure {label}")