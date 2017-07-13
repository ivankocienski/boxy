
from OpenGL.GL import *

OR_HORZ = 1
OR_VERT = 2

class Box:
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.width = 100
        self.height = 100
        self.highlight = False 
        self.wall_lines = []

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

    def is_touching(self, orientation, pos, min_, max_):
        if orientation == OR_HORZ: 
            # horizontal
            if max_ <= self.xpos:
                return False

            if min_ >= self.xpos + self.width:
                return False

            if pos == self.ypos or pos == self.ypos + self.height:
                return True
            
            return False

        # vertical
        if max_ <= self.ypos:
            return False

        if min_ >= self.ypos + self.height:
            return False

        if pos == self.xpos or pos == self.xpos + self.width:
            return True

        return False

    def link_horz(self, other_boxes, ypos):
        if len(other_boxes) == 0:
            self.wall_lines.append((self.xpos, ypos, self.xpos + self.width, ypos))
            return

        out_lines = [(self.xpos, self.width)]

        for box in other_boxes:
            box_pos = box.xpos
            box_len = box.width

            # clip incoming box to wall boundaries,
            #  ignore it if it is completly outside
            if box_pos < self.xpos:
                diff = self.xpos - box_pos
                box_pos = self.xpos
                box_len -= diff
                if box_len <= 0: continue

            if box_pos+box_len > self.xpos+self.width:
                diff = (self.xpos + self.width) - (box_pos + box_len)
                box_len -= diff
                if box_len <= 0: continue

            # now compute new line segments
            new_lines = []

            for line in out_lines:
                l_pos, l_len = line
                # skip if box out of line bounds?
                if box_pos + box_len < l_pos or l_pos + l_len < box_pos:
                    new_lines.append((l_pos, l_len))
                    continue

                # front bit
                if box_pos > l_pos:
                    f_len = box_pos - l_pos
                    if f_len > 0:
                        new_lines.append((l_pos, f_len))

                # tail bit
                if box_pos + box_len < l_pos + l_len:
                    f_pos = box_pos + box_len
                    f_len = (l_pos + l_len) - f_pos
                    if f_len > 0:
                        new_lines.append((f_pos, f_len))

            out_lines = new_lines

        for line in out_lines:
            l_pos, l_len = line
            self.wall_lines.append((l_pos, ypos, l_pos + l_len, ypos))

    def link_vert(self, other_boxes, xpos):
        if len(other_boxes) == 0:
            self.wall_lines.append((xpos, self.ypos, xpos, self.ypos + self.height))
            return

        out_lines = [(self.ypos, self.height)]

        for box in other_boxes:
            box_pos = box.ypos
            box_len = box.height

            # clip incoming box to wall boundaries,
            #  ignore it if it is completly outside
            if box_pos < self.ypos:
                diff = self.ypos - box_pos
                box_pos = self.ypos
                box_len -= diff
                if box_len <= 0: continue

            if box_pos+box_len > self.ypos+self.height:
                diff = (self.ypos + self.height) - (box_pos + box_len)
                box_len -= diff
                if box_len <= 0: continue

            # now compute new line segments
            new_lines = []

            for line in out_lines:
                l_pos, l_len = line
                # skip if box out of line bounds?
                if box_pos + box_len < l_pos or l_pos + l_len < box_pos:
                    new_lines.append((l_pos, l_len))
                    continue

                # front bit
                if box_pos > l_pos:
                    f_len = box_pos - l_pos
                    if f_len > 0:
                        new_lines.append((l_pos, f_len))

                # tail bit
                if box_pos + box_len < l_pos + l_len:
                    f_pos = box_pos + box_len
                    f_len = (l_pos + l_len) - f_pos
                    if f_len > 0:
                        new_lines.append((f_pos, f_len))

            out_lines = new_lines

        for line in out_lines:
            l_pos, l_len = line
            self.wall_lines.append((xpos, l_pos, xpos, l_pos + l_len))

    def link_walls(self, map_):

        # north
        other_boxes = map_.find_boxes_touching(
                OR_HORZ,
                self.ypos, 
                self.xpos,
                self.xpos + self.width,
                self)

        self.link_horz(other_boxes, self.ypos)
        

        # east
        other_boxes = map_.find_boxes_touching(
                OR_VERT,
                self.xpos + self.width,
                self.ypos,
                self.ypos + self.height,
                self)
        
        self.link_vert(other_boxes, self.xpos + self.width)


        # south
        other_boxes = map_.find_boxes_touching(
                OR_HORZ, 
                self.ypos + self.height, 
                self.xpos, 
                self.xpos + self.width, 
                self)
        
        self.link_horz(other_boxes, self.ypos + self.height)
        

        # west
        other_boxes = map_.find_boxes_touching(
                OR_VERT, 
                self.xpos, 
                self.ypos, 
                self.ypos + self.height, 
                self)

        self.link_vert(other_boxes, self.xpos)

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
            glColor3f(0.1, 0.1, 0.1)
            glBegin(GL_QUADS)
      
            glVertex2f( x1, y1 )
            glVertex2f( x2, y1 )
            glVertex2f( x2, y2 )
            glVertex2f( x1, y2 )
      
            glEnd()
  
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_LINE_LOOP)
  
        glVertex2f( x1, y1 )
        glVertex2f( x2, y1 )
        glVertex2f( x2, y2 )
        glVertex2f( x1, y2 )
  
        glEnd()

        glColor3f(1, 1, 1)
        glBegin(GL_LINES)

        for wl in self.wall_lines:

            x1, y1, x2, y2 = wl
      
            glVertex2f( x1, y1 )
            glVertex2f( x2, y2 )
      
        glEnd()

    def draw_player_bit(self):
        x1 = self.xpos+1
        y1 = self.ypos+1
        x2 = x1 + self.width-2
        y2 = y1 + self.height-2
  
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_LINE_LOOP)
  
        glVertex2f( x1, y1 )
        glVertex2f( x2, y1 )
        glVertex2f( x2, y2 )
        glVertex2f( x1, y2 )
  
        glEnd()
