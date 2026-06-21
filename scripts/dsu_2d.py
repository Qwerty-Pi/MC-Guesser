import numpy as np
from boundbox import BoundBox

class DSU_2D:
    def __init__(self, width, height, black_cells):
        self.width = width
        self.height = height
        self.parent = np.array([i for i in range(width * height)], dtype=np.uint32)
        self.bboxes = {}
        for x, y in black_cells:
            self.bboxes[y * width + x] = BoundBox(width, height)
            self.bboxes[y * width + x].add(x, y)
    
    def join(self, a, b):
        a, b = self.find_root(a), self.find_root(b)
        if a == b: return False
        self.parent[a] = b
        self.bboxes[b].add_rect(self.bboxes[a])
        assert self.bboxes[b].width() <= 1
        return True

    def find_root(self, x):
        root = x
        while root != self.parent[root]:
            root = self.parent[root]
        
        curr = x
        while curr != root:
            nxt = self.parent[curr]
            self.parent[curr] = root
            curr = nxt
            
        return root
