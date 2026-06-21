import fitz
import matplotlib.pyplot as plt
from PIL import Image
import re
import numpy as np
import os, sys
from pathlib import Path
import math, json
import editdistance
from utility import svgs_to_pdf, fetch_svg_dimensions
from functools import cmp_to_key
import math
from dsu_2d import DSU_2D
from page_reader import PageReader
from boundbox import BoundBox
from nostril import nonsense

def is_nonsense(text):
    text = text.replace(" ", "").replace("+", "").replace("-", "").replace("=", "")
    if len(text) <= 20:
        return False
    return nonsense(text)

label_no = None

def repeat_rate(text):
    text = text.replace(" ", "")
    if len(text) <= 1: return 0
    cnt = 0
    for i in range(len(text) - 1):
        cnt += text[i] == text[i + 1]
    return cnt / (len(text) - 1)

def process_figures(year, doc, page_no, page_cnt = 1, verbal = False):
    global label_no
    print(f"Processing page #{page_no + 1}")
    
    print("Step #1")

    # lower dpi coz dsu time consuming
    # but cannot too low because otherwise the cropbox will be off by too much
    # which becomes ugly
    page = PageReader.page_to_png(doc[page_no], dpi = 80)
    a = np.asarray(page)
    b = np.sum(a[:, :, :3], axis=2) 
    a2 = np.where(b[:, :, np.newaxis] > 220 * 3, 255, 0).astype(np.uint8).reshape(a.shape[0], a.shape[1], 1)
    
    def inside_page(x, y):
        return 0 <= x < page.width and 0 <= y < page.height
    
    def is_black(x, y):
        if not inside_page(x, y):
            return False
        return a2[y][x].all() == 0

    def is_border(x, y):
        return not(is_black(x + 1, y) and is_black(x, y + 1) and is_black(x - 1, y) and is_black(x, y - 1))

    black_cells = []
    subwidth = page.width // page_cnt
    for p in range(page_cnt):
        for y in range(page.height):
            for x in range(subwidth):
                if is_black(x + p * subwidth, y):
                    black_cells.append([x + p * subwidth, y])
    
    dsu_weak = DSU_2D(page.width, page.height, black_cells)
    dsu_strong = DSU_2D(page.width, page.height, black_cells)

    
    for x, y in black_cells:
        D = 1
        for dy in range(0, D + 1):
            for dx in range(-D, D + 1):
                if (abs(dx) + abs(dy) > D):
                    continue
                nx, ny = x + dx, y + dy
                if is_black(nx, ny):
                    dsu_strong.join(y * page.width + x, ny * page.width + nx)

    for x, y in black_cells:
        if not is_border(x, y): continue
        D = 8
        for dy in range(0, D + 1):
            for dx in range(-D, D + 1):
                if (abs(dx) + abs(dy) > D):
                    continue
                nx, ny = x + dx, y + dy
                if is_black(nx, ny):
                    dsu_weak.join(y * page.width + x, ny * page.width + nx)
    
    bbox_tags = []
    svg_code = doc[page_no].get_svg_image()
    dim = fetch_svg_dimensions(svg_code)

    reader = PageReader()
    png = PageReader.page_to_png(doc[page_no], dpi=600)

    prv_bbox = BoundBox(page.width, page.height)

    os.makedirs(f"info/page-{page_no}", exist_ok=True)

    print("Step #2")

    figures = {}

    for x, y in black_cells:
        id = y * page.width + x
        if dsu_weak.find_root(id) != id:
            continue
        bbox = dsu_weak.bboxes[id]
        if bbox.width() < 0.002 or bbox.height() < 0.002:
            continue
        print("Bounding Box:", bbox.x1, bbox.y1, bbox.x2, bbox.y2)

        # slightly larger crop box
        crop_box = [
            max(0, bbox.x1 - 0.01) * png.width,
            max(0, bbox.y1 - 0.01) * png.height,
            min(1, bbox.x2 + 0.01) * png.width,
            min(1, bbox.y2 + 0.01) * png.height
        ]
        img = png.crop(crop_box)
        
        detected_text = reader.read_text(img)
        label_txt = reader.read_label(img)
        
        text_density = max(len(label_txt), len(detected_text.replace("|", "").replace("\n", "").replace(" ", ""))) / bbox.area()
        is_figure = (editdistance.eval("Go on to the next page", detected_text) > 5 and bbox.area() <= 0.5 and text_density < 1200 and 0.04 <= bbox.width() <= 0.9 and 0.04 <= bbox.height() <= 0.9)

        label = None
        if (prv_bbox.empty or bbox.x1 % (1.0 / page_cnt) < prv_bbox.x1 % (1.0 / page_cnt) + 0.05) and text_density > 5000 and bbox.width() < 0.1:
            label = re.fullmatch(r"(\d{1,2})\.?", reader.read_label(img))
            # label = re.fullmatch(str(year % 100) + "\n" + r"(\d{1,2})\.?", reader.read_label(img))
        print("Detected Text (Tesseract):", detected_text)
        print("Detected Text (Label):", label_txt)

        if verbal:
            plt.imshow(img)
            plt.show()

        stroke = "#0d10d1"
        fill = "none"
        text = ""

        # Figure should have higher prority
        if is_figure:
            stroke = "#8f077f"
            fill = "#32a89980"
        elif label:
            stroke = "blue"
            fill = "#8485b880"
            if label_no == None or abs(label_no - int(label.group(1))) <= 1 or len(str(label_no)) <= len(label.group(1)):
                label_no = int(label.group(1))
            else:
                label_no = label_no + 1 # override if OCR fked up
            prv_bbox = bbox
            text = f"Label {label_no}"
        
        if not is_figure:
            style = f"fill:{fill};stroke:{stroke};stroke-width:2;stroke-dasharray:5,5"
            bbox_tags.append(bbox.svg(dim, style, text))
        else:
            if label_no == None: continue
            if label_no not in figures:
                figures[label_no] = []
            bbox.density = text_density
            figures[label_no].append(bbox)
        print("Density:", text_density)

    figures_json = []
    for label_no, bboxes in figures.items():
        bboxes = sorted(bboxes, key=lambda bbox: (math.floor(bbox.y1 * 10), math.floor(bbox.x1 * 10)))
        for i in range(len(bboxes)):
            bboxes[i].x1 = max(0, bboxes[i].x1 - 0.005)
            bboxes[i].y1 = max(0, bboxes[i].y1 - 0.005)
            bboxes[i].x2 = min(1, bboxes[i].x2 + 0.005)
            bboxes[i].y2 = min(1, bboxes[i].y2 + 0.005)
        if len(bboxes) == 1:
            figures_json.append({"page": page_no, "label": label_no, "bbox": bboxes[0]})
        else:
            for i in range(len(bboxes)):
                figures_json.append({"page": page_no, "label": str(label_no) + chr(97 + i), "bbox": bboxes[i]})
    
    stroke = "#8f077f"
    fill = "#32a89980"
    style = f"fill:{fill};stroke:{stroke};stroke-width:2;stroke-dasharray:5,5"
    for figure in figures_json:
        bbox, label = figure['bbox'], figure['label']
        bbox_tags.append(bbox.svg(dim, style, f"Figure {label} Density {round(bbox.density)}"))
        figure['rect'] = bbox.relative(doc[page_no].rect.width, doc[page_no].rect.height)
        del figure['bbox']

    closing_tag = "</svg>"
    bboxes_str = "\n".join(bbox_tags) + "\n" + closing_tag
    svg_code = svg_code.replace(closing_tag, bboxes_str)
    output_path = f"bbox/page_{page_no}.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_code)
    
    return figures_json

def gen_year(year, page_cnt = 1, page_no = None, verbal = False):
    print(f"Generating Paper 2 for year {year}...")
    doc = fitz.open(f"../raw/paper-2/{year}.pdf")
    with open("../test.svg", "w") as f:
        f.write(doc[0].get_svg_image(text_as_path=False))
    global label_no
    label_no = None
    os.system("rm bbox/*.svg")

    figures = []
    for i in range(len(doc)):
        if page_no == i or page_no is None:
            page_figures = process_figures(year, doc, i, page_cnt, verbal)
            figures.extend(page_figures)
    if page_no is None:
        with open(f"../artifact/paper-2/{year}/figures.json", "w") as f:
            f.write(json.dumps(figures))
    svgs = []
    for i in range(0, 100):
        if Path(f"bbox/page_{i}.svg").is_file():
            svgs.append(f"bbox/page_{i}.svg")
    svgs_to_pdf(svgs, "tmp", f"../test-self/{year}.pdf")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 test.py year")
        sys.exit(1)
    gen_year(int(sys.argv[1]), 2)
