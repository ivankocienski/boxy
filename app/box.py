
from OpenGL.GL import *
from math import sqrt

OR_HORZ = 1
OR_VERT = 2

COLORS = [
        (1, 1, 1), # white
        (0.75, 0.75, 0.75), # grey
        (1, 0.2, 0.2), # red
        (1, 0.8, 0.0), # yellow
        (0.2, 1, 0.3), # green
        (0.2, 0.1, 1)] # blu


class Line:

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def nearest_distance_to(self, px, py):
        
        # this is a bit hacky, but works because
        #   walls can only be in one of two
        #   orientations

        nx = px
        ny = py

        # horizontal
        if self.x1 == self.x2:
            nx = self.x1
            ny = py
            if ny < self.y1: ny = self.y1
            if ny > self.y2: ny = self.y2

        # vertical
        else:
            ny = self.y1
            nx = px
            if nx < self.x1: nx = self.x1
            if nx > self.x2: nx = self.x2 

        dx = px - nx
        dy = py - ny
        return (sqrt(dx*dx + dy*dy), nx, ny)

    def draw(self): 
        glVertex2f( self.x1, self.y1 )
        glVertex2f( self.x2, self.y2 )

    def draw3d(self, color):
        mult = 0.7

        if self.x1 == self.x2: mult = 0.8

        glColor3f(color[0] * mult, color[1] * mult, color[2] * mult)

        glBegin(GL_TRIANGLE_FAN);

        glVertex3f(self.x1, -20, self.y1);
        glVertex3f(self.x1,  20, self.y1);
        glVertex3f(self.x2,  20, self.y2);
        glVertex3f(self.x2, -20, self.y2); 

        glEnd();
        


class Box:
    def __init__(self, parent=None):
        self.parent = parent
        self.xpos = 0
        self.ypos = 0
        self.width = 100
        self.height = 100
        self.highlight = False 
        self.wall_lines = []
        self.color = COLORS[0]
        self.color_num = 0
        self.sub_boxes = []

    def __str__(self):
        return "<Box xpos=%d ypos=%d width=%d height=%d" % (self.xpos, self.ypos, self.width, self.height)

    def set_pos_from(self, x, y):
        self.xpos = x
        self.ypos = y
        self.width = 0 
        self.height = 0

    def set_size_from(self, x, y):
        if self.parent is not None:
            if not self.parent.contains_point(x, y):
                return

        self.width  = x - self.xpos
        self.height = y - self.ypos
        print("  set size from %d %d %d %d %d %d" % (x, y, self.xpos, self.ypos, self.width, self.height))

        if self.width  < 0: self.width  = 0
        if self.height < 0: self.height = 0

    def next_color(self):
        self.color_num = (self.color_num + 1) % len(COLORS)
        self.color = COLORS[self.color_num]

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
            self.wall_lines.append(Line(self.xpos, ypos, self.xpos + self.width, ypos))
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
            self.wall_lines.append(Line(l_pos, ypos, l_pos + l_len, ypos))

    def link_vert(self, other_boxes, xpos):
        if len(other_boxes) == 0:
            self.wall_lines.append(Line(xpos, self.ypos, xpos, self.ypos + self.height))
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
            self.wall_lines.append(Line(xpos, l_pos, xpos, l_pos + l_len))

    def link_walls(self, map_):

        self.wall_lines = []
        other_boxes = []

        # north
        if map_ is None:
            other_boxes = []

        else:
            other_boxes = map_.find_boxes_touching(
                    OR_HORZ,
                    self.ypos, 
                    self.xpos,
                    self.xpos + self.width,
                    self)

        self.link_horz(other_boxes, self.ypos)
        
        other_boxes = []

        # east
        if map_ is None:
            other_boxes = []

        else: 
            other_boxes = map_.find_boxes_touching(
                    OR_VERT,
                    self.xpos + self.width,
                    self.ypos,
                    self.ypos + self.height,
                    self)
        
        self.link_vert(other_boxes, self.xpos + self.width)

        other_boxes = []

        # south
        if map_ is None:
            other_boxes = []

        else: 
            other_boxes = map_.find_boxes_touching(
                    OR_HORZ, 
                    self.ypos + self.height, 
                    self.xpos, 
                    self.xpos + self.width, 
                    self)
        
        self.link_horz(other_boxes, self.ypos + self.height)
        
        other_boxes = []

        # west
        if map_ is None:
            other_boxes = []

        else: 
            other_boxes = map_.find_boxes_touching(
                    OR_VERT, 
                    self.xpos, 
                    self.ypos, 
                    self.ypos + self.height, 
                    self)

        self.link_vert(other_boxes, self.xpos)

    def to_save_string(self):
        return "%d %d %d %d %d" % (self.xpos, self.ypos, self.width, self.height, self.color_num)

    def find_closest_point(self, px, py):
        out_dist = 99999
        out_hx = 0
        out_hy = 0

        for wl in self.wall_lines:
            wd, wx, wy = wl.nearest_distance_to(px, py)
            if wd >= out_dist: continue
            out_dist = wd
            out_hx = wx
            out_hy = wy

        return (out_dist, out_hx, out_hy)

    def from_save_strings(self, px, py, w, h, c):
        self.xpos   = px
        self.ypos   = py
        self.width  = w
        self.height = h
        self.color_num = c
        self.color = COLORS[self.color_num]

    def contains_point(self, px, py):
        if px < self.xpos: return False
        if py < self.ypos: return False

        px -= self.xpos
        if px > self.width: return False

        py -= self.ypos
        if py > self.height: return False

        return True

    def start_plot_sub_box(self, px, py):
        b = Box(self)
        b.xpos = px
        b.ypos = py

        return b

    def finish_plot_sub_box(self, box):
        print("finish_plot_sub_box %s" % box)
        box.link_walls(None)
        self.sub_boxes.append(box)

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

        for l in self.wall_lines:
            l.draw()

        glEnd()

        glColor3f(1, 1, 0)

        for sb in self.sub_boxes:
            sb.draw_partial_2d()


    def draw_partial_2d(self):
        x1 = self.xpos
        y1 = self.ypos
        x2 = x1 + self.width
        y2 = y1 + self.height
  
        glBegin(GL_LINE_LOOP)
  
        glVertex2f( x1, y1 )
        glVertex2f( x2, y1 )
        glVertex2f( x2, y2 )
        glVertex2f( x1, y2 )
  
        glEnd()

    def draw3d(self):

        x1 = self.xpos
        y1 = self.ypos
        x2 = x1 + self.width
        y2 = y1 + self.height

        # floor
        glColor3f(self.color[0] * 0.9, self.color[1] * 0.9, self.color[2] * 0.9)

        glBegin(GL_TRIANGLE_FAN);

        glVertex3f(x1, -20, y1);
        glVertex3f(x2, -20, y1);
        glVertex3f(x2, -20, y2);
        glVertex3f(x1, -20, y2); 

        glEnd();

        # cieling
        glColor3f(self.color[0] * 1, self.color[1] * 1, self.color[2] * 1)

        glBegin(GL_TRIANGLE_FAN);

        glVertex3f(x1, 20, y1);
        glVertex3f(x2, 20, y1);
        glVertex3f(x2, 20, y2);
        glVertex3f(x1, 20, y2); 

        glEnd();

        for l in self.wall_lines:
            l.draw3d(self.color)

        for sb in self.sub_boxes:
            sb.draw_partial_3d(self.color)

    def draw_partial_3d(self, color):
        for l in self.wall_lines:
            l.draw3d(color)


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
