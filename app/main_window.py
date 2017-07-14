
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

    
class MainWindow:

    def __init__(self, app):
        self.app = app
        self.map = Map()
        self.cursor = Cursor(20, app)
        self.player = Player(400, 300)
        self.dir_keys = [False, False, False, False]
        self.walk_mode = False # 3D

        self.plot_box = None
        self.select_box = None

        try:
            self.map.load('map.txt')

        except FileNotFoundError:
            print("map.txt not found, using blank")

        self.player.set_pos(
                self.map.player_start_xpos,
                self.map.player_start_ypos)

        print("Press Q to quit")
        #print("Move mouse about. Press SPACE-BAR to start / end plotting of box")

    def mouse_move(self, xp, yp):
        self.cursor.move(xp, yp)
        if self.plot_box:
            self.plot_box.set_size_from(self.cursor.step_x, self.cursor.step_y)
            self.app.repaint()

        #self.app.repaint()
        pass

    def mouse_down(self, btn): 
        #print("mouse_down=%s" % btn)
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


    def mouse_up(self, btn): 
        #print("mouse_up=%s" % btn)
        pass

    def is_idle(self):
        return (self.select_box is None) and (self.plot_box is None)

    def tick(self):
        self.player.move(self.map, self.dir_keys)

    def key_down(self, key):
        #print("key=%s" % key)
        if key == pg.K_q: 
            self.app.stop_loop()
            return

        if self.walk_mode == False:
            if key == pg.K_SPACE:
                if self.plot_box:
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


            if key == pg.K_BACKSPACE and self.select_box:
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

            if key == pg.K_HOME:
                self.map.set_player_start(self.player.xpos, self.player.ypos)
                self.app.repaint()
                return
                
        if key == pg.K_RETURN:
            self.walk_mode = not self.walk_mode
            if self.walk_mode:
                self.app.setup3d()
            else:
                self.app.setup2d()

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


    def draw(self):
        if self.walk_mode == False:
            self.map.draw()

            if self.plot_box:
                self.plot_box.draw()

            self.cursor.draw() 
            self.player.draw()

        else:
            self.player.look()
            self.map.draw3d()



