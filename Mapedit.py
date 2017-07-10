
import os
import random
import pygame as pg
from pygame.locals import *
from OpenGL.GL import *

from app.main_window import MainWindow

class Loader:
    def __init__(self, base, sound_capable):
        self.base_dir = base
        self.sound_capable = sound_capable

    def load_image(self, path):
        print("load_image: %s" % path)
        img = pg.image.load(os.path.join(self.base_dir, path))
        img.set_colorkey((255, 0, 255))
        return img
        #return .convert_alpha(self.screen)

    def load_ttf(self, path, size):
        print("load_font: %s" % path)
        fnt = pg.font.Font(os.path.join(self.base_dir, path), size)
        return fnt

    def load_wav(self, path):
        print("load_wav: %s" % path)
        if not self.sound_capable:
            return None

        snd = pg.mixer.Sound(os.path.join(self.base_dir, path))
        return snd

class App:

    def __init__(self):
        random.seed()
        print("pygame ver=%s"%pg.version.ver)
        pg.init()
        pg.font.init()

        self.run_loop = True
        self.loader = Loader(os.getcwd() + "/data", False)

        self.screen = pg.display.set_mode([800, 600], HWSURFACE | OPENGL | DOUBLEBUF, 24)
        glViewport(0, 0, 800, 600)

        pg.display.set_caption('Map edit')

        self.setup2d()
        self.repaint()

    def draw_text( self, font, x, y, text, color ):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def setup2d(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, 800.0, 600.0, 0.0, -1.0, 1.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def setup3d(self):
        pass

    def repaint(self):
        self.do_repaint = True

    def stop_loop(self):
        self.run_loop = False

    def main(self):

        win = MainWindow(self)

        while(self.run_loop):
            pg.time.delay(10)

            for event in pg.event.get():

                if event.type == QUIT:
                    return 

                elif event.type == MOUSEMOTION:
                    win.mouse_move(event.pos[0], event.pos[1])

                elif event.type == MOUSEBUTTONDOWN:
                    win.mouse_down(event.button)

                elif event.type == MOUSEBUTTONUP:
                    win.mouse_up(event.button)

                elif event.type == KEYDOWN:
                    win.key_down(event.key)

            if self.do_repaint:
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                self.do_repaint = False
                win.draw()
                pg.display.flip()

if __name__ == "__main__": App().main()
