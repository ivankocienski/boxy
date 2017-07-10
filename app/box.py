
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
