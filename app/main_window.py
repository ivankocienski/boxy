
import pygame as pg
from OpenGL.GL import *

from .box import Box
from .map import Map
from .player import Player


class Cursor:
    def __init__(self, spacing, app):
        self.spacing = spacing
        self.app = app
        self.step_x = 0
        self.step_y = 0
        self.real_x = 0
        self.real_y = 0

    def move(self, to_x, to_y):
        self.real_x = to_x
        self.real_y = to_y

        new_x = int((self.real_x + self.spacing * 0.5) / self.spacing) * self.spacing
        new_y = int((self.real_y + self.spacing * 0.5) / self.spacing) * self.spacing

        if new_x != self.step_x:
            self.app.repaint()
            self.step_x = new_x

        if new_y != self.step_y:
            self.app.repaint()
            self.step_y = new_y

    def draw(self):
        x1 = self.step_x - 2
        y1 = self.step_y - 2
        x2 = x1 + 4
        y2 = y1 + 4
  
        glColor3f(0.7, 0.7, 1)
        glBegin(GL_LINE_LOOP)
  
        glVertex2f( x1, y1 )
        glVertex2f( x2, y1 )
        glVertex2f( x2, y2 )
        glVertex2f( x1, y2 )
  
        glEnd()

class ModeCommon:
    def __init__(self, win, name):
        self.name = name
        self.win = win
        self.app = win.app
        self.cursor = win.cursor
        self.map = win.map
        self.player = win.player
        self.dir_keys = [False, False, False, False]

    def activate(self):
        print("activating mode '%s'" % self.name)
        pass

    def draw(self):
        pass

    def tick(self): 
        self.player.move(self.map, self.dir_keys)

    def mouse_move(self, xp, yp):
        self.cursor.move(xp, yp) 

    def mouse_down(self, btn):
        pass

    def mouse_up(self, btn):
        pass

    def key_down(self, key):
        if key == pg.K_q: 
            self.app.stop_loop()
            return

        if key == pg.K_RETURN:
            if self.win.mode.name == 'plot':
                self.win.set_mode('walk')
            else:
                self.win.set_mode('plot')

                
        if key == pg.K_c:
            self.player.bump_box_color()
            return

        if key == pg.K_UP:
            self.dir_keys[0] = True
            return

        if key == pg.K_DOWN:
            self.dir_keys[1] = True
            return

        if key == pg.K_LEFT:
            self.dir_keys[2] = True
            return

        if key == pg.K_RIGHT:
            self.dir_keys[3] = True
            return
        pass

    def key_up(self, key):
        if key == pg.K_UP:
            self.dir_keys[0] = False
            return

        if key == pg.K_DOWN:
            self.dir_keys[1] = False
            return

        if key == pg.K_LEFT:
            self.dir_keys[2] = False
            return

        if key == pg.K_RIGHT:
            self.dir_keys[3] = False
            return
        pass

class PlotMode(ModeCommon):

    def __init__(self, win):
        super().__init__(win, 'plot') 
        self.plot_box = None
        self.select_box = None

    def draw(self):
        super().draw()
        self.map.draw()

        if self.plot_box:
            self.plot_box.draw()

        self.cursor.draw() 
        self.player.draw()

    def activate(self):
        super().activate()
        self.app.setup2d()


    def is_idle(self):
        #return (self.select_box is None) and (self.plot_box is None)
        return self.plot_box is None
    
    def mouse_move(self, x, y):
        super().mouse_move(x, y)
        if self.plot_box:
            self.plot_box.set_size_from(self.cursor.step_x, self.cursor.step_y)
            self.app.repaint()

    def mouse_down(self, btn):
        super().mouse_down(btn)

        if btn == 1:
            box = self.map.box_at_point(self.cursor.step_x, self.cursor.step_y)
            if box:
                self.select_box = box
                self.map.clear_highlight()
                box.highlight = True
                self.app.repaint()

        if btn == 2:
            self.player.set_pos(
                    self.cursor.step_x,
                    self.cursor.step_y)
        pass

    def key_down(self, key):
        super().key_down(key)

        if key == pg.K_SPACE and self.is_idle():
            if self.plot_box:
                if not self.plot_box.parent:
                    self.plot_box.set_size_from(self.cursor.step_x, self.cursor.step_y)

                    if self.plot_box.is_valid():
                        self.map.append_box(self.plot_box)
                        self.plot_box = None
                        self.map.link_boxes()

                    self.app.repaint()

            else:
                self.plot_box = Box()
                self.plot_box.set_pos_from(self.cursor.step_x, self.cursor.step_y)
                self.app.repaint()

            return

        if key == pg.K_h and self.is_idle(): # holes
            
            cur_x = self.cursor.step_x
            cur_y = self.cursor.step_y

            if self.plot_box:
                p_box = self.plot_box.parent
                if p_box and p_box.contains_point(cur_x, cur_x):
                    print("plot hole end")
                    p_box.finish_plot_sub_box(self.plot_box)
                    self.plot_box = None
                    self.app.repaint()
                    

            else:
                print("plot hole start")
                box = self.map.box_at_point(cur_x, cur_y)
                if box:
                    if True: #box.contains_point(cur_x, cur_y):
                        self.plot_box = box.start_plot_sub_box(cur_x, cur_y)
                        self.select_box = box



            return

        if key == pg.K_BACKSPACE and self.is_idle() and self.select_box:
            self.map.remove_box(self.select_box)
            self.select_box = None
            self.app.repaint()
            self.map.link_boxes()
            return

        if key == pg.K_F2 and self.is_idle():
            self.map.save('map.txt')
            print("map saved to map.txt")
            return
            
        if key == pg.K_F4 and self.is_idle():
            self.map.clear()
            print("map cleared")
            self.select_box = None
            self.plot_box = None
            self.app.repaint()
            return

        if key == pg.K_HOME and self.is_idle():
            self.map.set_player_start(self.player.xpos, self.player.ypos)
            self.app.repaint()
            return

    #def key_up(self, key):
    #    super().key_up(key)

class WalkMode(ModeCommon):

    def __init__(self, win):
        super().__init__(win, 'walk')

    def activate(self):
        super().activate()
        self.app.setup3d()

    def draw(self):
        super().draw
        self.player.look()
        self.map.draw3d()

    #def mouse_move(self. x, y):
    #    pass

    #def mouse_down(self, x, y):
    #    pass

    #def key_down(self, key):
    #    pass
    
class MainWindow:

    def __init__(self, app):
        self.app = app
        self.map = Map()
        self.cursor = Cursor(20, app)
        self.player = Player(400, 300)

        try:
            self.map.load('map.txt')

        except FileNotFoundError:
            print("map.txt not found, using blank")

        self.player.set_pos(
                self.map.player_start_xpos,
                self.map.player_start_ypos)

        self.walk_mode = WalkMode(self)
        self.plot_mode = PlotMode(self)
        self.mode_name = ''

        self.set_mode("plot")

        print("Press Q to quit")
        #print("Move mouse about. Press SPACE-BAR to start / end plotting of box")

    def set_mode(self, name):
        if name == 'plot':
            self.mode = self.plot_mode
            
        elif name == 'walk':
            self.mode = self.walk_mode

        else:
            raise StandardError("Could not find mode %s" % name)

        self.mode.activate()

    def mouse_move(self, xp, yp):
        self.mode.mouse_move(xp, yp) 

    def mouse_down(self, btn): 
        self.mode.mouse_down(btn)

    def mouse_up(self, btn): 
        self.mode.mouse_up(btn)

    def tick(self):
        self.mode.tick()

    def key_down(self, key):
        self.mode.key_down(key)

    def key_up(self, key):
        self.mode.key_up(key) 

    def draw(self):
        self.mode.draw()





