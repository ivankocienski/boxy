
from OpenGL.GL import *

class Box:
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.width = 100
        self.height = 100
        self.highlight = False 

    def set_pos_from(self, x, y):
        self.xpos = x
        self.ypos = y
        self.width = 0 
        self.height = 0

    def set_size_from(self, x, y):
        self.width  = x - self.xpos
        self.height = y - self.ypos
        if self.width  < 0: self.width  = 0
        if self.height < 0: self.height = 0

    def is_valid(self):
        return self.width > 0 and self.height > 0

    def clear_walls(self):
        self.walls = [] 

    def link_walls(self, map_):
        pass

    def to_save_string(self):
        return "%d %d %d %d" % (self.xpos, self.ypos, self.width, self.height)

    def from_save_strings(self, px, py, w, h):
        self.xpos   = px
        self.ypos   = py
        self.width  = w
        self.height = h

    def contains_point(self, px, py):
        if px < self.xpos: return False
        if py < self.ypos: return False

        px -= self.xpos
        if px > self.width: return False

        py -= self.ypos
        if py > self.height: return False

        return True

    def set_highlight(self, hl=True):
        self.highlight = hl

    def draw(self):
        x1 = self.xpos
        y1 = self.ypos
        x2 = x1 + self.width
        y2 = y1 + self.height
  
        if self.highlight:
            glColor3f(0.2, 0.2, 0.2)
            glBegin(GL_QUADS)
      
            glVertex2f( x1, y1 )
            glVertex2f( x2, y1 )
            glVertex2f( x2, y2 )
            glVertex2f( x1, y2 )
      
            glEnd()
  
        glColor3f(1, 1, 1)
        glBegin(GL_LINE_LOOP)
  
        glVertex2f( x1, y1 )
        glVertex2f( x2, y1 )
        glVertex2f( x2, y2 )
        glVertex2f( x1, y2 )
  
        glEnd()
