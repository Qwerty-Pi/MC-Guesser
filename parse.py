import os
import ollama
from pdf2image import convert_from_path

# 1. 設定你的 PDF 路徑
pdf_path = "PP-DSE-MATH-CP-1.pdf"

# 2. 將 PDF 的每一頁轉成圖片
print("正在轉換 PDF 頁面...")
pages = convert_from_path(pdf_path, dpi=150)

# 3. 逐頁送給 Ollama GLM-OCR
for i, page in enumerate(pages):
    print(f"\n--- 正在辨識第 {i+1} 頁 ---")
    
    # 暫存為圖片檔案
    img = f"images/{i+1}.png"
    page.save(img, "PNG")
    
    os.system(f"lexoid parse -i images/{i+1}.png --parser-type STATIC_PARSE > output/{i+1}.txt")
