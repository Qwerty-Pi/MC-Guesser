import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from sklearn.svm import SVC
import os
import random

class TNRDigitClassifier:
    def __init__(self):
        # 1. High-Resolution HOG Settings for Serif Fonts
        self.win_size = (32, 32)
        self.block_size = (16, 16)
        self.block_stride = (8, 8)
        self.cell_size = (4, 4) # Reduced cell size captures finer serif details
        self.nbins = 9
        
        self.hog = cv2.HOGDescriptor(
            self.win_size, 
            self.block_size, 
            self.block_stride, 
            self.cell_size, 
            self.nbins
        )
        
        # 2. Upgraded Classifier: RBF Kernel handles complex, non-linear image noise better
        self.clf = SVC(kernel='rbf', C=10.0, gamma='scale', probability=True)

    def _extract_hog(self, img_patch):
        """Standardizes inputs and extracts normalized gradient direction vectors."""
        if img_patch.shape[:2] != self.win_size:
            img_patch = cv2.resize(img_patch, self.win_size, interpolation=cv2.INTER_CUBIC)
            
        if len(img_patch.shape) == 3:
            img_patch = cv2.cvtColor(img_patch, cv2.COLOR_BGR2GRAY)
            
        return self.hog.compute(img_patch).flatten()

    def generate_synthetic_data(self):
        """Generates augmented TNR numbers simulating real-world document noise."""
        images = []
        labels = []
        
        # Locate standard system font paths
        font_paths = [
            "./times.ttf", # Linux
        ]
        
        font_path = next((path for path in font_paths if os.path.exists(path)), None)
        if font_path is None:
            raise FileNotFoundError("Times New Roman font file (.ttf) could not be located.")

        # Class 0-9 for digits, Class 10 for the period '.'
        vocabulary = [(str(i), i) for i in range(10)] + [(".", 10)]

        for size in range(24, 76, 4):
            try:
                font = ImageFont.truetype(font_path, size)
            except IOError:
                continue

            for char_str, class_idx in vocabulary:
                # Generate positional shifts to simulate cropping offsets
                for dx in [-3, 0, 3]:
                    for dy in [-3, 0, 3]:
                        pil_img = Image.new('L', (128, 128), 255)
                        draw = ImageDraw.Draw(pil_img)
                        draw.text((32 + dx, 32 + dy), char_str, font=font, fill=0)
                        
                        cv_img = np.array(pil_img)
                        thresh = cv2.threshold(cv_img, 127, 255, cv2.THRESH_BINARY_INV)[1]
                        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        
                        if contours:
                            c = max(contours, key=cv2.contourArea)
                            x, y, w, h = cv2.boundingRect(c)
                            pad = 4
                            
                            # Base Clean Crop
                            roi = thresh[max(0, y-pad):min(thresh.shape[0], y+h+pad), 
                                         max(0, x-pad):min(thresh.shape[1], x+w+pad)]
                            
                            images.append(roi)
                            labels.append(class_idx)
                            
                            # --- DATA AUGMENTATION ---
                            # Simulates heavy ink bleed (dilation)
                            kernel = np.ones((2,2), np.uint8)
                            dilated = cv2.dilate(roi, kernel, iterations=1)
                            images.append(dilated)
                            labels.append(class_idx)
                            
                            # Simulates faded/broken toner (erosion)
                            eroded = cv2.erode(roi, kernel, iterations=1)
                            images.append(eroded)
                            labels.append(class_idx)
                            
                            # Simulates low-DPI scanner blur
                            blurred = cv2.GaussianBlur(roi, (3,3), 0)
                            images.append(blurred)
                            labels.append(class_idx)
                            
        return images, labels

    def train(self):
        """Generates augmented profiles and trains the RBF model."""
        print("Model Phase 1: Generating augmented Times New Roman profiles...")
        images, labels = self.generate_synthetic_data()
        
        print(f"Model Phase 2: Computing High-Res HOG patterns for {len(images)} variations...")
        features = [self._extract_hog(img) for img in images]
        features = np.array(features, dtype=np.float32)
        labels = np.array(labels, dtype=np.int32)
        
        print("Model Phase 3: Fitting RBF Support Vector boundaries...")
        self.clf.fit(features, labels)
        print(f"Training complete! Model validated on {len(images)} synthetic samples.")

    def predict(self, cropped_image_patch):
        """Extracts structural indicators from a single isolated character crop."""
        if not isinstance(cropped_image_patch, np.ndarray):
            cropped_image_patch = np.array(cropped_image_patch)
            
        features = self._extract_hog(cropped_image_patch)
        prediction = self.clf.predict([features])[0]
        confidence = self.clf.predict_proba([features])[0][prediction]
        
        return int(prediction), float(confidence)

    def predict_string(self, cropped_string_image):
        """Segments and classifies a continuous string of digits and punctuation."""
        if not isinstance(cropped_string_image, np.ndarray):
            img_cv = np.array(cropped_string_image)
        else:
            img_cv = cropped_string_image.copy()

        if len(img_cv.shape) == 3:
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        else:
            gray = img_cv

        # Strict binarization logic for clean contouring
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        digit_boxes = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            
            # Skip tiny pixel noise (dust artifacts), but preserve small dots
            if w < 2 or h < 3:
                continue
            digit_boxes.append((x, y, w, h))

        if not digit_boxes:
            return "", 0.0

        # Sort strictly left-to-right
        digit_boxes = sorted(digit_boxes, key=lambda box: box[0])

        final_string_chars = []
        confidence_scores = []

        for x, y, w, h in digit_boxes:
            pad = 4
            y1, y2 = max(0, y - pad), min(thresh.shape[0], y + h + pad)
            x1, x2 = max(0, x - pad), min(thresh.shape[1], x + w + pad)
            
            # Pass the thresholded patch to match training inputs
            digit_roi = thresh[y1:y2, x1:x2]
            
            class_val, conf = self.predict(digit_roi)
            
            # Remap index 10 back to literal period
            if class_val == 10:
                final_string_chars.append(".")
            else:
                final_string_chars.append(str(class_val))
                
            confidence_scores.append(conf)

        detected_string = "".join(final_string_chars)
        average_confidence = sum(confidence_scores) / len(confidence_scores)

        return detected_string, average_confidence