
from OpenGL.GL import *

from .box import Box

class Map:
    def __init__(self):
        self.boxes = []
        self.set_player_start(0, 0)

    def clear(self):
        self.boxes = []

    def box_at_point(self, px, py):
        for b in self.boxes: 
            if b.contains_point(px, py):
                return b

        return None

    def save(self, filename):
        with open(filename, 'wt') as f:
            f.write("start %d %d\n" % (self.player_start_xpos, self.player_start_ypos))

            for b in self.boxes:
                f.write("box %s\n" % b.to_save_string())

    def load(self, filename):
        loaded_boxes = []

        # this would be a lot nicer with a regex
        with open(filename, 'rt') as f:
            for line in f.readlines():
                parts = line.split()

                if parts[0] == 'box':
                    int_parts = [int(p) for p in parts[1:]]
                    b = Box()
                    b.from_save_strings(int_parts[0], int_parts[1], int_parts[2], int_parts[3])
                    loaded_boxes.append(b)
                    continue

                if parts[0] == 'start':
                    px = int(parts[1])
                    py = int(parts[2])
                    self.set_player_start(px, py)
                    continue
                
                print("warning: unrecognized line in map!")

        self.boxes = loaded_boxes
        self.link_boxes()

    
    def find_boxes_touching(self, orientation, pos, min_, max_, not_box):
        other_boxes = []
        for b in self.boxes:
            if b == not_box: continue

            if b.is_touching(orientation, pos, min_, max_):
                other_boxes.append(b)

        return other_boxes

    def set_player_start(self, xpos, ypos):
        self.player_start_xpos = xpos
        self.player_start_ypos = ypos

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

        x = self.player_start_xpos
        y = self.player_start_ypos
  
        glColor3f(0.0, 0.7, 0)
        glBegin(GL_LINE_LOOP)
  
        glVertex2f( x,   y-4 )
        glVertex2f( x+4, y )
        glVertex2f( x,   y+4 )
        glVertex2f( x-4, y )
  
        glEnd()


    def draw3d(self):
        for b in self.boxes: 
            b.draw3d()



    
