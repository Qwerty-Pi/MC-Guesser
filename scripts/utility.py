from PyPDF2 import PdfMerger
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import os, glob

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

# Source - https://stackoverflow.com/a/78678557
# Posted by Edd
# Retrieved 2026-06-12, License - CC BY-SA 4.0

import xml.etree.ElementTree as ET

def fetch_svg_dimensions(svg_content) -> tuple:
    svg_tree = ET.ElementTree(ET.fromstring(svg_content))
    svg_root = svg_tree.getroot()

    width = svg_root.attrib.get('width')
    height = svg_root.attrib.get('height')

    if width is None or height is None:
        viewBox = svg_root.attrib.get('viewBox')
        if viewBox:
            _, _, width, height = viewBox.split()
            width = width.strip()
            height = height.strip()

    return float(width), float(height)
