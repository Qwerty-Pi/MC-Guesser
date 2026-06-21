import cv2
import numpy as np

class TopologicalDigitParser:
    def __init__(self):
        pass

    def _preprocess(self, cropped_image):
        """Converts input image formats to an optimized, upscaled binary matrix."""
        if not isinstance(cropped_image, np.ndarray):
            img_cv = np.array(cropped_image)
        else:
            img_cv = cropped_image.copy()

        if len(img_cv.shape) == 3:
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        else:
            gray = img_cv

        # Upscale 3x to smooth out jagged pixel steps on low-DPI scans
        gray = cv2.resize(gray, (0, 0), fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        return thresh

    def parse_string(self, cropped_image):
        """
        Segments any continuous line of digits and punctuation, analyzes their
        topological properties dynamically, and returns the reassembled string sequence.
        """
        thresh = self._preprocess(cropped_image)

        # Connected Component Labeling to isolate pixel islands
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)

        components = []
        for i in range(1, num_labels):
            x, y, w, h, area = stats[i]
            if area < 6: # Filter scanner dust noise
                continue
            components.append({
                'id': i,
                'box': (x, y, w, h),
                'area': area
            })

        if not components:
            return ""

        # Sort left-to-right by X position
        components = sorted(components, key=lambda c: c['box'][0])

        # Establish global text baseline metrics
        max_digit_h = max(c['box'][3] for c in components)
        global_baseline = max(y + h for c in components for x, y, w, h in [c['box']] if h >= max_digit_h * 0.7)

        final_output_string = ""

        for comp in components:
            x, y, w, h = comp['box']
            aspect_ratio = w / float(h)
            
            # Extract isolated snapshot of just this character
            roi_mask = (labels[y:y+h, x:x+w] == comp['id']).astype(np.uint8) * 255

            # --- 1. IDENTIFY PUNCTUATION ---
            if h < max_digit_h * 0.35:
                distance_to_baseline = abs((y + h) - global_baseline)
                if distance_to_baseline < (max_digit_h * 0.25) and (0.65 <= aspect_ratio <= 1.35):
                    final_output_string += "."
                else:
                    final_output_string += ","
                continue

            # --- 2. COUNT INTERNAL HOLES (RETR_TREE) ---
            # RETR_TREE establishes a hierarchy map to reveal trapped white spaces inside the ink
            contours, hierarchy = cv2.findContours(roi_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            # Total loops = (all contours found) minus (the 1 external outer boundary contour)
            hole_count = len(contours) - 1 if len(contours) > 1 else 0

            # --- 3. COMPUTE WEIGHT/MASS MATRIX DISTRIBUTION ---
            mid_y, mid_x = h // 2, w // 2
            top_pixels = np.sum(roi_mask[0:mid_y, :] == 255)
            bottom_pixels = np.sum(roi_mask[mid_y:, :] == 255)
            left_pixels = np.sum(roi_mask[:, 0:mid_x] == 255)
            right_pixels = np.sum(roi_mask[:, mid_x:] == 255)

            # --- 4. THE DECISION TREE MATRIX ---
            
            # CATEGORY A: 2 Holes
            if hole_count == 2:
                final_output_string += "8"
                
            # CATEGORY B: 1 Hole
            elif hole_count == 1:
                # Is the loop upstairs or downstairs?
                if top_pixels > bottom_pixels * 1.25:
                    final_output_string += "9"
                elif bottom_pixels > top_pixels * 1.25:
                    final_output_string += "6"
                elif right_pixels > left_pixels * 1.25:
                    final_output_string += "4"
                else:
                    final_output_string += "0"

            # CATEGORY C: Solid Shapes (0 Holes)
            else:
                if aspect_ratio < 0.42:
                    final_output_string += "1"
                elif top_pixels > bottom_pixels * 1.12:
                    # Top heavy: Could be a 7 or a 5
                    if right_pixels > left_pixels * 1.15:
                        final_output_string += "7"
                    else:
                        final_output_string += "5"
                elif bottom_pixels > top_pixels * 1.12:
                    final_output_string += "2"
                else:
                    # Vertically balanced solid shape leaning heavily to the right side
                    if right_pixels > left_pixels * 1.12:
                        final_output_string += "3"
                    else:
                        # Safety fallback for slight scanner distortion variations
                        final_output_string += "?" 

        return final_output_string