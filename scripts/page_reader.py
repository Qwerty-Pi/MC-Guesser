
import os
import cv2
import numpy as np
import pytesseract
from PIL import Image

class PageReader:
    def __init__(self):
        pass

    def page_to_png(page, dpi):
        pix = page.get_pixmap(alpha=False, dpi=dpi)
        height, width, num_channels = pix.h, pix.w, pix.n
        img = np.frombuffer(pix.samples, dtype=np.uint8) \
            .reshape(height, width, num_channels)
        assert num_channels == 3 # RGB
        return Image.fromarray(img)

    def read_label(self, image):
        gry = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gry, (5, 5), 0)
        _, thr = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        try:
            txt = pytesseract.image_to_string(thr, config="--psm 6 -c tessedit_char_whitelist=0l123456789][ABCD.,").strip()
        except:
            return "" # why?
        similar = [
            ["][IlL", "1"],
            [",", "."]
        ]
        for c_from, c_to in similar:
            for c in c_from:
                txt = txt.replace(c, c_to)
        return txt

    def read_text(self, image, label_mode=False):
        image = np.array(image)
        height, width = image.shape[:2]
        image = cv2.resize(image, (width * 3, height * 3), interpolation=cv2.INTER_CUBIC)
        gry = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        thr = 255 - cv2.threshold(gry, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        thr = cv2.GaussianBlur(thr, (3,3), 0)
        txt = pytesseract.image_to_string(thr, lang='eng', config='--psm 1').strip()
        similar = [
            ["][IlL", "1"],
            [",", "."]
        ]
        if label_mode:
            for c_from, c_to in similar:
                for c in c_from:
                    txt = txt.replace(c, c_to)
        return txt

    def read_text_lexoid(self, image):
        image.save(f"tmp/1.png")
        os.system(f"lexoid parse -i tmp/1.png --parser-type static_parse --verbose > tmp/1.txt")
        return open(f"tmp/1.txt").read()

    def is_figure(image):
        pass
