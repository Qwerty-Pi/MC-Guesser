import os
import cv2
import numpy as np
import fitz  # PyMuPDF (Extremely memory efficient)
from PIL import Image
from paddlex import create_model
from pathlib import Path

from PyPDF2 import PdfMerger
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import os, glob

def extract_diagrams_low_ram(pdf_path, output_dir="extracted_diagrams"):
    os.makedirs(output_dir, exist_ok=True)
    
    local_model_path = os.path.expanduser("~/tools/paddlex_models/PP-DocLayout-L_infer")
    model = create_model(
        model_name="PP-DocLayout-L",
        model_dir=local_model_path
    )
    
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        print(f"*** Page {page_num + 1} ***")
        page = doc[page_num]
        svg_code = page.get_svg_image()
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        img_np = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        if pix.n == 4:
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGR)
        else:
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            
        pix = None 
        output = model.predict(img_bgr)
        
        bbox_tags = []
        for res in output:
            for box_info in res['boxes']:
                print(box_info)
                label = box_info.get('label', '').lower()
                print(label)
                    
                coordinate = box_info.get('coordinate')
                if not coordinate or len(coordinate) != 4:
                    continue
                    
                scale = 0.502
                x1, y1, x2, y2 = map(int, coordinate)
                bx1, by1, bx2, by2 = int(x1 * scale), int(y1 * scale), int(x2 * scale), int(y2 * scale)

                pad = 0
                bx1, by1 = max(0, bx1 - pad), max(0, by1 - pad)
                bx2, by2 = min(page.rect.width, bx2 + pad), min(page.rect.height, by2 + pad)
                b_width = bx2 - bx1
                b_height = by2 - by1
                
                important = label in ["image", "chart", "table"]
                colour = "#00000080" if important else "none"
                rect_tag = f'<rect x="{bx1}" y="{by1}" width="{b_width}" height="{b_height}" style="fill:{colour};stroke:#8f077f;stroke-width:2;stroke-dasharray:5,5" />'
                bbox_tags.append(rect_tag)
            
            closing_tag = "</svg>"
            injected_boxes_str = "\n".join(bbox_tags) + "\n" + closing_tag
            modified_svg_code = svg_code.replace(closing_tag, injected_boxes_str)
            
        # 4. Save the modified vector graphic file
        output_filepath = f"bounded/page_{page_num + 1}.svg"
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(modified_svg_code)

def svgs_to_pdf(file_paths=[r'C:\1.svg',r'C:\2.svg',r'C:\3.svg'], output_folder='tmp', pdf_name='test.pdf'):
    """
    Convert svg files into pdfs, save pdfs in output_folder, merge them in one pdf file.
    @param file_paths: full paths to svg files
    @param output_folder: path to folder for saving temporary pdfs
    @param pdf_name: name for resulting pdf file.
    """
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
    for n,f in enumerate(file_paths):
        drawing = svg2rlg(f)
        renderPDF.drawToFile(drawing, os.path.join('tmp', '%s.pdf' % n))
    pdfs = glob.glob(os.path.join(output_folder,'*.pdf'))
    pdfs.sort(key=os.path.getmtime)
    
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
        
    merger.write(pdf_name)
    merger.close()
    for pdf in pdfs:
        os.remove(pdf)

def parse_test(year):
    target_pdf = f"raw/paper-2/{year}.pdf" 
    os.system("rm bounded/*")
    extract_diagrams_low_ram(target_pdf)

    svgs = []
    for i in range(1, 20):
        if Path(f"bounded/page_{i}.svg").is_file():
            svgs.append(f"bounded/page_{i}.svg")
    svgs_to_pdf(svgs, "tmp", f"test/{year}.pdf")

# parse_test(2011)
for year in [2008, 2009, 2010, 2011]:
    parse_test(year)