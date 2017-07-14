
from OpenGL.GL import *
from math import pi, sin, cos

class Player:
    def __init__(self, x = 0, y = 0):
        self.xpos = x
        self.ypos = y
        self.xinc = 0
        self.yinc = 0
        self.angle = 0
        self.box = None

    def find_box_in(self, map_):
        self.box = map_.box_at_point(self.xpos, self.ypos)

    def move(self, map_, dir_keys):

        def try_move(box, to_x, to_y):

            if box:
                dist, hit_x, hit_y = box.find_closest_point(to_x, to_y)
                self.near_x = hit_x
                self.near_y = hit_y
                if dist > 10:
                    self.xpos = to_x
                    self.ypos = to_y

        if dir_keys[2]: self.angle -= 0.2
        if dir_keys[3]: self.angle += 0.2

        moving = False
        new_xpos = self.xpos
        new_ypos = self.ypos

        if dir_keys[0]:
            new_xpos += self.xinc
            new_ypos += self.yinc
            moving = True

        if dir_keys[1]:
            new_xpos -= self.xinc
            new_ypos -= self.yinc
            moving = True

        self.xinc = cos(self.angle)
        self.yinc = sin(self.angle)

        if moving:
            
            # inside a box
            if self.box:

                # staying in this box?
                if self.box.contains_point(new_xpos, new_ypos):
                    try_move(self.box, new_xpos, new_ypos)

                # moving to another box?
                else:
                    self.box = map_.box_at_point(self.xpos, self.ypos)
                    try_move(self.box, new_xpos, new_ypos)



            # outside of all boxes?
            else: 
                self.box = map_.box_at_point(self.xpos, self.ypos)
                try_move(self.box, new_xpos, new_ypos)


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

        if self.box:
            self.box.draw_player_bit()
