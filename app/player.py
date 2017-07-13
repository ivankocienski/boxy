
from OpenGL.GL import *
from math import pi, sin, cos

class Player:
    def __init__(self, x = 0, y = 0):
        self.xpos = x
        self.ypos = y
        self.xinc = 0
        self.yinc = 0
        self.angle = 0

    def move(self, dir_keys):

        if dir_keys[2]: self.angle -= 0.2
        if dir_keys[3]: self.angle += 0.2

        if dir_keys[0]:
            self.xpos += self.xinc
            self.ypos += self.yinc

        if dir_keys[1]:
            self.xpos -= self.xinc
            self.ypos -= self.yinc

        self.xinc = cos(self.angle)
        self.yinc = sin(self.angle)
        pass

    def draw(self): 

        glColor3f(1, 1, 1)

        # border
        glBegin(GL_LINE_LOOP)

        for i in range(0, 10):
          a = (2.0 * pi) * (float(i) / 10.0);

          glVertex2f(
              self.xpos + 10 * cos(a),
              self.ypos + 10 * sin(a)
              )


        glEnd()

        # direction
        glBegin(GL_LINES)

        glVertex2d(self.xpos, self.ypos)
        glVertex2d(self.xpos + 12 * self.xinc, self.ypos + 12 * self.yinc)

        glEnd(); 
