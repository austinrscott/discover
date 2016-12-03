#!/usr/bin/python

# Import pygame
import pygame
from pygame.locals import *


def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption('Discover')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Draw a test box
    box = draw_box(width=screen.get_width()*0.9,
                   height=screen.get_height()/10,
                   fillcolor=(240,240,240),
                   bordercolor=(40,40,40))
    box_spacing = (screen.get_width() - box.get_width()) / 2
    background.blit(box,
                    (box_spacing, screen.get_height() - box.get_height() - box_spacing))

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    quit()

        screen.blit(background, (0, 0))
        pygame.display.flip()


def draw_box(width, height, borderwidth=3, fillcolor=(255, 255, 255), bordercolor=(25,25,25)):
    new_surface = pygame.Surface((width, height))
    new_surface.fill(fillcolor)
    pygame.draw.rect(new_surface, bordercolor, new_surface.get_rect(), borderwidth)
    return new_surface


if __name__ == '__main__':
    main()