import pygame as pg
import sys
pg.init()

RESOLUTION: tuple = (400, 500)

pg.display.set_mode(RESOLUTION)
pg.display.set_caption("Combat & Dodge")

running: bool = True
while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

    pg.display.flip()

pg.quit()
sys.exit()
