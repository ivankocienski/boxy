
from OpenGL.GL import *

class Box:
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.width = 100
        self.height = 100

    def draw(self):
        x1 = self.xpos
        y1 = self.ypos
        x2 = x1 + self.width
        y2 = y1 + self.height
  
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
  
        glVertex2f( x1, y1 )
        glVertex2f( x2, y1 )
        glVertex2f( x2, y2 )
        glVertex2f( x1, y2 )
  
        glEnd()
  
