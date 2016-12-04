#!/usr/bin/python

# Import pygame
import pygame
from pygame.locals import *

# Import map class
from widget import ContainerWidget, Map


def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Discover')

    # Initialize root widget
    root = ContainerWidget(screen.get_rect())

    # Initialize map
    root.add(Map(pos=[25, 25]))

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                quit()
            elif event.type == MOUSEBUTTONDOWN:
                root.event(event)
        root.render()
        screen.blit(root.get_surface(), (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    main()
