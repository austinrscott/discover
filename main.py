#!/usr/bin/python

# Import pygame
import pygame
from pygame.locals import *
# Import map class
from widget import ContainerWidget, MapWidget, Button


def main():
    # Initialize screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Discover')

    # Initialize FPS clock
    fps_clock = pygame.time.Clock()

    # Initialize root widget
    root = ContainerWidget(screen.get_rect())

    # Initialize map
    root.add(MapWidget(pos=[25, 25]))
    root.add(Button(pos=[600, 25]))

    # Event loop
    while 1:
        # Tick the game clock and capture FPS data to the window caption
        fps_clock.tick()
        pygame.display.set_caption('Discover — FPS: {:.2f}'.format(fps_clock.get_fps()))
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
