class BoundBox:
    def __init__(self, page_width: float, page_height: float, \
                 x1: float = 1 << 30, y1: float = 1 << 30, x2: float = -(1 << 30), y2: float = -(1 << 30)):
        self.page_width = page_width
        self.page_height = page_height
        self.density = 0
        self.empty = True
        if x1 < 1:
            self.empty = False
        self.x1, self.x2 = x1, x2
        self.y1, self.y2 = y1, y2
    
    
    def add(self, x: float, y: float, normalised: bool = False):
        """
            Add cell [x, x + 1] * [y, y + 1] to the bounding box.
            The value get stored is the relative position respective to the page.
        """
        self.empty = False
        if not normalised:
            x /= self.page_width
            y /= self.page_height
        self.x1, self.x2 = min(self.x1, x), max(self.x2, x + 1 / self.page_width)
        self.y1, self.y2 = min(self.y1, y), max(self.y2, y + 1 / self.page_height)
        assert(self.x1 >= 0 and self.x2 <= 1)

    def add_rect(self, bbox):
        """
            Add another bounding box to this bounding box.
        """
        if bbox.empty:
            return
        self.x1 = min(self.x1, bbox.x1)
        self.x2 = max(self.x2, bbox.x2)
        self.y1 = min(self.y1, bbox.y1)
        self.y2 = max(self.y2, bbox.y2)
    
    def height(self):
        """Return the height of the bounding box."""
        if self.empty:
            return 0
        return self.y2 - self.y1
    
    def width(self):
        """Return the width of the bounding box."""
        if self.empty:
            return 0
        return self.x2 - self.x1
    
    def area(self):
        """Return the relative area of the bounding box."""
        return self.height() * self.width()

    def relative(self, scale_width = 1, scale_height = 1):
        """Return the coordinates of the bounding box, normalised to [0, 1] x [0, 1]."""
        return [self.x1 * scale_width, self.y1 * scale_height, self.x2 * scale_width, self.y2 * scale_height]

    def svg(self, dimensions, style, content):
        """
            Return the svg code for the bounding box.

        dimensions: dimensions of the svg file.
        style: css style of the bounding box.
        content: stuff to be written.
        """
        if self.empty:
            return ""
        x1, x2 = self.x1 * dimensions[0], self.x2 * dimensions[0]
        y1, y2 = self.y1 * dimensions[1], self.y2 * dimensions[1]

        # Bounding Box Rectangle
        svg  = f"""
            <rect
                x="{x1}" y="{y1}"
                width="{x2 - x1}" height="{y2 - y1}"
                style="{style}"
            />
        """

        # Write text at the "center"
        svg += f"""
            <text
                x="{(x1 + x2) / 2}"
                y="{(y1 + y2) / 2}"
                dominant-baseline="middle"
                text-anchor="middle">
                {content}
            </text>
        """
        return svg
