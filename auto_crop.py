import cv2
import layoutparser as lp
from pdf2image import convert_from_path

# 1. Convert scanned PDF pages to images
pages = convert_from_path('2011.pdf', dpi=200)

# 2. Load a pre-trained Deep Learning model for document layout
# This model recognizes paragraphs, tables, and figures/diagrams
model = lp.Detectron2LayoutModel(
    'lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
    extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.75],
    label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}
)

for page_idx, page in enumerate(pages):
    # Convert image to OpenCV format
    img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
    
    # 3. Detect layout elements
    layout = model.detect(img)
    
    # 4. Filter out everything except "Figures" (Diagrams)
    figures = [block for block in layout if block.type == 'Figure']
    
    # 5. Crop and save each detected diagram
    for fig_idx, fig in enumerate(figures):
        # Get coordinates of the diagram
        x1, y1, x2, y2 = fig.coordinates
        
        # Crop the image using numpy slicing
        cropped_diagram = img[int(y1):int(y2), int(x1):int(x2)]
        
        # Save to disk
        cv2.imwrite(f'test_images/{page_idx+1}_diagram_{fig_idx+1}.png', cropped_diagram)
        print(f"Cropped diagram {fig_idx+1} on page {page_idx+1}")