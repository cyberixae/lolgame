#!/usr/bin/env python

import sys
import pygame
import pygame.locals

WIDTH = 16
HEIGHT = 14
screenw = 400
screenh = 240
times = 2

def double(surf, n):
    if n < 1:
         return surf
    else:
         return double(pygame.transform.scale2x(surf), n - 1)

def tiles(filename, w, h):
    image = pygame.image.load(filename).convert()
    wlimit, hlimit = image.get_size()
    rows = hlimit / h
    columns = wlimit / w
    for r in range(rows):
        for c in range(columns):
            (x, y) = (c * w, r * h)
            yield ((c, r), image.subsurface((x, y, w, h)))

def coord((c, r)):
    return (c * 24, r * 16)

def submaps(wmap,(subw, subh)):
    def cut(position, wm):
        return (wm[:position],wm[position:])
    wm = wmap.split('\n')[:2*subh]
    (top, bottom) = cut(HEIGHT, wm)
    (tl, tr) = [j for j in zip(*[cut(subw, i) for i in top])]
    (bl, br) = [j for j in zip(*[cut(subw, i) for i in bottom])]
    return ((tl, tr),(bl, br))

((tl, tr),(bl, br)) = submaps(open('world.map').read(), (WIDTH, HEIGHT))

def flatten(lists):
    flat = []
    for list in lists:
        flat.extend(list)
    return flat

def translate(c):
    tiles = ('2#T1','t Cw.','sh')
    temp = [[(j,(x,y)) for (x,j) in enumerate(i)] for (y,i) in enumerate(tiles)]
    return dict(flatten(temp))[c]

pygame.init()
screen = pygame.display.set_mode((2**(times-1)*screenw, 2**(times-1)*screenh))
background = pygame.Surface((screenw, screenh))
loltiles = dict(tiles('lolgame5.png', 24, 16))

background.fill((0, 0, 0))
[background.blit(loltiles[translate(bl[y][x])], coord((x, y))) for x in range(WIDTH) for y in range(HEIGHT)]
background.blit(loltiles[(2,2)], coord((5, 5)))
screen.blit(double(background, times - 1), (0, 0))

clock = pygame.time.Clock()
#clock.tick(1)

pygame.display.flip()
homerun = True
while homerun:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
             homerun = False
        elif event.type == pygame.locals.KEYDOWN:
             key = event.key
             if key == pygame.locals.K_PLUS:
                 print '+'
             elif key == pygame.locals.K_MINUS:
                 print '-'
             elif key == pygame.locals.K_q:
                 homerun = False
