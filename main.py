import pygame, sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1024, 768))
mapSurface = DISPLAYSURF.convert_alpha()
DISPLAYSURF.fill((255,255,255))
pygame.display.set_caption('Discover')
while True: # main game loop
    for event in pygame.event.get():
       if event.type == QUIT:
           pygame.quit()
           sys.exit()
    pygame.display.update()