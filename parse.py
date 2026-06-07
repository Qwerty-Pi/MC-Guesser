import os, sys
import ollama
from pdf2image import convert_from_path

def parse_texts(pdf_path, output_path):
    pages = convert_from_path(pdf_path, dpi=80)
    for i, page in enumerate(pages):
        print(f"\n--- Recognising Page #{i+1} ---")
        img_path = f"{output_path}/images/{i+1}.png"
        text_path = f"{output_path}/text/{i+1}.png"
        page.save(img_path, "PNG")
        os.system(f"lexoid parse -i {img_path} --parser-type static_parse --verbose > {text_path}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: ./parse pdf_path output_path")
    else:
        pdf_path, output_path = sys.argv[1], sys.argv[2]
        parse_texts(pdf_path, output_path)
