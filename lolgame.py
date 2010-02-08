#!/usr/bin/env python

import sys
import pygame
import pygame.locals

WIDTH = 16
HEIGHT = 14
screenw = 400
screenh = 240
screenf = 0
times = 2
oldtimes = 2
mapx = 0
mapy = 1

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
    tiles = ('?2#T14','t Cw.','sh@3H')
    temp = [[(j,(x,y)) for (x,j) in enumerate(i)] for (y,i) in enumerate(tiles)]
    return dict(flatten(temp))[c]

def gettile(symbol):
    try:
        tilecoord = translate(symbol)
    except:
        tilecoord = (0,0)

    return loltiles[tilecoord]

pygame.init()
screen = pygame.display.set_mode((2**(times-1)*screenw, 2**(times-1)*screenh), screenf)
background = pygame.Surface((screenw, screenh))
mix = pygame.Surface((screenw, screenh))
loltiles = dict(tiles('lolgame5.png', 24, 16))

background.fill((15, 15, 15))
[background.blit(gettile(bl[y][x]), coord((x, y))) for x in range(WIDTH) for y in range(HEIGHT)]
overlays = pygame.sprite.RenderUpdates()
overlay = pygame.sprite.Sprite(overlays)
image = loltiles[translate('@')]
overlay.image = image
overlay.rect = image.get_rect().move(coord((2, 2)))
mix.blit(background, (0, 0))
overlays.draw(mix)

clock = pygame.time.Clock()
#clock.tick(1)

homerun = True
x=2
y=2
while homerun:
    overlay.rect = image.get_rect().move(coord((x, y)))
    overlays.draw(mix)
    (cw, ch) = screen.get_size()
    screen.blit(double(mix, times - 1), ((cw-((2**(times-1))*screenw))/2,(ch-((2**(times-1))*screenh))/2 ))
    clock.tick(30)
    pygame.display.flip()
    overlays.clear(mix, background)
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
             homerun = False
        elif event.type == pygame.locals.KEYDOWN:
             key = event.key
             if key == pygame.locals.K_DOWN:
                 if y < HEIGHT - 1:
                     y += 1
             elif key == pygame.locals.K_UP:
                 if y > 0:
                     y -= 1
             elif key == pygame.locals.K_LEFT:
                 if x > 0:
                     x -= 1
             elif key == pygame.locals.K_RIGHT:
                 if x < WIDTH - 1:
                     x += 1
             elif key == pygame.locals.K_PLUS:
                 if times < 5:
                         if screenf != pygame.FULLSCREEN:
                             times += 1
                             screen = pygame.display.set_mode((2**(times-1)*screenw, 2**(times-1)*screenh), screenf)
             elif key == pygame.locals.K_MINUS:
                 if times > 1:
                         if screenf != pygame.FULLSCREEN:
                             times -= 1
                             screen = pygame.display.set_mode((2**(times-1)*screenw, 2**(times-1)*screenh), screenf)
             elif key == pygame.locals.K_0:
                 if screenf != pygame.FULLSCREEN:
                     times = 2
                     screen = pygame.display.set_mode((2**(times-1)*screenw, 2**(times-1)*screenh), screenf)
             elif key == pygame.locals.K_q:
                 homerun = False
             elif key == pygame.locals.K_F11:
                 if screenf != 0:
                     screenf = 0
                     times = oldtimes
                 else:
                     def dunno(a, b):
                         n = 0
                         while b < a:
                             b *= 2
                             n += 1
                         return n
                     oldtimes = times
                     screenf = pygame.FULLSCREEN
                     modes = pygame.display.list_modes()
                     modetimes = [min(dunno(w,screenw), dunno(h,screenh)) for (w, h) in modes]
                     mtmax = max(modetimes)
                     (times, _) = min([(mt, m) for (mt, m) in zip(modetimes, modes) if mt == mtmax])

                 screen = pygame.display.set_mode((2**(times-1)*screenw, 2**(times-1)*screenh), screenf)

