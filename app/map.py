
from OpenGL.GL import *

from .box import Box

class Map:
    def __init__(self):
        self.boxes = []

    def clear(self):
        self.boxes = []

    def box_at_point(self, px, py):
        for b in self.boxes: 
            if b.contains_point(px, py):
                return b

        return None

    def save(self, filename):
        with open(filename, 'wt') as f:
            for b in self.boxes:
                f.write("box %s\n" % b.to_save_string())

    def load(self, filename):
        loaded_boxes = []

        # this would be a lot nicer with a regex
        with open(filename, 'rt') as f:
            for line in f.readlines():
                parts = [int(p) for p in line.split()[1:]]
                b = Box()
                b.from_save_strings(parts[0], parts[1], parts[2], parts[3])
                loaded_boxes.append(b)

        self.boxes = loaded_boxes
        self.link_boxes()

    
    def find_boxes_touching(self, orientation, pos, min_, max_, not_box):
        other_boxes = []
        for b in self.boxes:
            if b == not_box: continue

            if b.is_touching(orientation, pos, min_, max_):
                other_boxes.append(b)

        return other_boxes

    def link_boxes(self):
        #for b in self.boxes: 
        #    b.clear_walls()

        for b in self.boxes: 
            b.link_walls(self)


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


    
