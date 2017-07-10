
from OpenGL.GL import *

from .box import Box

class Map:
    def __init__(self):
        self.boxes = []

    def box_at_point(self, px, py):
        for b in self.boxes: 
            if b.contains_point(px, py):
                return b

        return None

    def clear_highlight(self):
        for b in self.boxes: 
            b.highlight = False

    def remove_box(self, box):
        self.boxes.remove(box)


    def append_box(self, b):
        self.boxes.append(b)

    def draw(self):
        for b in self.boxes: 
            b.draw()

    
